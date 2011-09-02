from madas.repository.models import RunSample, RUN_STATES, SampleNotInClassException, InstrumentSOP
from django.http import HttpResponse
import random

class RunBuilderException(Exception):
    pass

class RunBuilder(object):
    def __init__(self, run):
        self.run = run

    def validate(self):
        for sample in self.run.samples.all():
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
   
        # TODO - put re-enable this!!!
        #if self.run.state == RUN_STATES.NEW[0]:
        #    self.layout()
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
        items = self.add_sweeps(items)

        self.save_items(items)

    def delete_nonsample_run_samples(self):
        # Deletes all the RunSamples that aren't Samples (ie. Standards, Blanks etc.)
        RunSample.objects.filter(run=self.run, component__id__gt=0).delete()
       
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
        samples = list(self.run.runsample_set.filter(component__id=0))
        insert_after = {}
        for rule in self.run.rule_generator.sample_block_rules:
            sample_count = rule.sample_count
            start_idxs = range(0, len(samples), sample_count)
            end_idxs = range(sample_count, len(samples), sample_count) + [len(samples)]
            for start,end in zip(start_idxs, end_idxs):
                position = end
                if rule.in_random_position:
                    position = random.randint(start+1, end)
                arr = insert_after.setdefault(position, [])
                for i in range(rule.count):
                    arr.append(RunSample.create(self.run, rule.component)) 

        sample_block = []
        for i, sample in enumerate(samples):
            sample_block.append(sample)
            items = insert_after.get(i+1)
            if items:
                sample_block.extend(items)
                
        return sample_block

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
