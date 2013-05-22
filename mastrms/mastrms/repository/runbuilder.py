from mastrms.repository.models import RunSample, RUN_STATES, SampleNotInClassException, InstrumentSOP
from django.http import HttpResponse
import random

class RunBuilderException(Exception):
    pass

class RunBuilder(object):
    def __init__(self, run):
        self.run = run

    def validate(self):
        for sample in self.run.samples.distinct():
            sample.run_filename(self.run)

    def layout(self):
        #validate first, this will throw an exception if failed
        self.validate()

        layout = RunLayout(self.run)
        layout.perform_layout()
        #end result of a perform_layout is new RunSample entries to represent all other line items

    def generate(self):
        try:
            self.validate()
        except Exception, e:
            raise RunBuilderException('Run validation error ' + str(e))
        except SampleNotInClassException, e:
            raise RunBuilderException('Samples in the run need to be in sample classes before they can be used in a run')

        if self.run.state == RUN_STATES.NEW[0]:
            self.layout()

        #write filenames into DB
        for rs in RunSample.objects.filter(run=self.run):
            rs.filename = rs.generate_filename()
            rs.save()

        #mark the run as in-progress and save it
        if self.run.state == RUN_STATES.NEW[0]:
            self.run.state = RUN_STATES.IN_PROGRESS[0]
            self.run.save()

class RunLayout(object):
    def __init__(self, run):
        self.run = run

    def perform_layout(self):
        self.delete_nonsample_run_samples()

        start_block = self.create_start_block()
        sample_block = self.create_sample_block()
        end_block = self.create_end_block()

        items = start_block + sample_block + end_block
        if self.run.rule_generator.apply_sweep_rule:
            items = self.add_sweeps(items)

        self.save_items(items)

    def delete_nonsample_run_samples(self):
        # Deletes all the RunSamples that aren't Samples (ie. Standards, Blanks etc.)
        RunSample.objects.filter(run=self.run, component__id__gt=0).delete()
        # TODO another reason the generator should generate a clean worklist in a different DB table
        # We have to ensure that only method 1 Samples are kept and method_number is resetted to None
        RunSample.objects.filter(run=self.run, method_number__gt=1).delete()
        RunSample.objects.filter(run=self.run, method_number=1).update(method_number=None)

    def create_start_block(self):
        start_block = []
        for rule in self.run.rule_generator.start_block_rules:
            for i in range(rule.count):
                start_block.append(RunSample.create(self.run, rule.component))
        return start_block

    def create_end_block(self):
        end_block = []
        for rule in self.run.rule_generator.end_block_rules:
            for i in range(rule.count):
                end_block.append(RunSample.create(self.run, rule.component))
        return end_block

    def create_sample_block(self):
        samples = list(self.run.runsample_set.filter(component__id=0).order_by('sequence'))
        insertion_map = self.create_insertion_map(samples, self.run.rule_generator.sample_block_rules)
        sample_block = self.combine(samples, insertion_map)
        sample_block = self.apply_method_rules(sample_block)
        return sample_block

    def create_insertion_map(self, samples, rules):
        '''Returns a dict: keys are positions in the sample_list, values an array of items to insert at that position'''
        insertion_map = {}
        for rule in rules:
            sample_count = rule.sample_count
            start_idxs = range(0, len(samples), sample_count)
            end_idxs = range(sample_count, len(samples), sample_count) + [len(samples)]
            for start,end in zip(start_idxs, end_idxs):
                position = end
                if rule.in_random_position:
                    position = random.randint(start+1, end)
                arr = insertion_map.setdefault(position, [])
                for i in range(rule.count):
                    arr.append(RunSample.create(self.run, rule.component))
        return insertion_map

    def combine(self, samples, insertion_map):
        sample_block = []
        for i, sample in enumerate(samples):
            sample_block.append(sample)
            items = insertion_map.get(i+1)
            if items:
                # if anything to insert at position i+1 insert it
                sample_block.extend(items)
        return sample_block

    def apply_method_rules(self, sample_block):
        number_of_methods = self.run.number_of_methods or 1
        if number_of_methods <= 1:
            return sample_block

        for sample in sample_block:
            sample.method_number = 1
            sample.save()

        extended_sample_block = []
        if self.run.is_method_type_individual_vial():
            extended_sample_block = sample_block[:]
            for method_number in range(2, number_of_methods+1):
                for sample in sample_block:
                    extended_sample_block.append(RunSample.create_copy(sample, method_number))
        else:
            for sample in sample_block:
                extended_sample_block.append(sample)
                for method_number in range(2, number_of_methods+1):
                    extended_sample_block.append(RunSample.create_copy(sample, method_number))

        return extended_sample_block

    def add_sweeps(self, items):
        items_with_sweeps = []
        for item in items:
            items_with_sweeps.append(item)
            if not item.is_blank():
                items_with_sweeps.append(RunSample.create_sweep(self.run))
        return items_with_sweeps

    def save_items(self, items):
        for seq, item in enumerate(items):
            item.sequence = seq+1
            item.save()
