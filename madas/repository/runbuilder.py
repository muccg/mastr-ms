from madas.repository.models import RunSample, SampleNotInClassException

class RunBuilder(object):
    def __init__(self, run):
        self.run = run

    def validate(self):
        for sample in self.run.samples.all():
            sample.run_filename(self.run)
            
        return True
        
    def layout(self):
        #validate first, this will throw an exception if failed
        self.validate()
        
        layout = GCRunLayout(self.run)
        layout.perform_layout()
        print layout.layout
        #end result of a perform_layout is new RunSample entries to represent all other line items
        
    def generate(self, request):
        try:
            self.validate()
            #if the validate fails we throw an exception
            
            # TODO : remove and re-generate blanks and quality controls
            
            from mako.template import Template
            
            mytemplate = Template(self.run.method.template)
            
            #create the variables to insert
            render_vars = {'username':request.user.username,'run':self.run,'runsamples':RunSample.objects.filter(run=self.run)}
            
            #write filenames into DB
            for rs in RunSample.objects.filter(run=self.run):
                if rs.type == 0:
                    rs.filename = rs.sample.run_filename(self.run)
                    rs.save()
            
            #render
            return mytemplate.render(**render_vars)
        except SampleNotInClassException, e:
            return 'Samples in the run need to be in sample classes before they can be used in a run'
        except Exception, e:
            return 'Run validation error ' + str(e)
        
        
class RunGroup(object):
    def __init__(self):
        self.samples = []
        self._layout = []
        self.sweeps = []
        self.pooled_qcs = []
        
    def add_pooled_QCs(self):
        #add pooled QCs into group
        if len(self.samples) >= 10:
            print 'add pbqc randomly'
            pb = 'PBQC'
            self.pooled_qcs = [pb]
            import random
            randloc = random.randint(0,len(self.samples))
            self.samples.insert(randloc,pb)
        
    def interleave_sweeps(self):
        #insert sweeps after each sample
        self._layout = []
        
        for counter in range(len(self.samples)):
            self._layout.append(self.samples[counter])
            #create a sweep entry
            sweep = 'sweep'
            self.sweeps.append(sweep)
            self._layout.append(sweep)
            
    def layout(self):
        if len(self._layout) == 0:
            return self.samples
        else:
            return self._layout

        
class GenericRunLayout(object):
    def __init__(self, run):
        self.run = run
        samples = self.run.samples.all()
        self.samples = []
        for sample in samples:
            self.samples.append(sample)
        
    def clear(self):
        self.groups = []
        self.layout = []
        self.solvents = []
        self.reagents = []
        self.intrument_qcs = []
        self.pooled_qcs = []
        # and purge these meta samples from the RunSample table for this run
        RunSample.objects.filter(run=self.run,type__gt=0).delete()
        
    def perform_layout(self):
        print 'perform_layout'
        #process self.samples, following general rules to layout the rest
        self.clear()
        
        self.randomize()
        self.split(10)
        map(RunGroup.add_pooled_QCs, self.groups)
        self.interleave_solvents()
        self.add_pooled_QC_padding()
        self.add_reagent_blank()
        self.add_solvent_padding()
        
    def randomize(self):
        #randomizes all items in the layout
        print 'randomize'
        import random
        random.shuffle(self.samples)
        self.layout = self.samples
        
    def split(self, length):
        print 'split'
        #if 20 or less samples, do not split
        if len(self.samples) <= 20:
            b = RunGroup()
            b.samples = self.samples[:]
            self.groups = [b]
        else:
            #split samples into groups
            f = lambda A, n=length: [A[i:i+n] for i in range(0, len(A), n)]
            grps = f(self.samples)
            
            self.groups = []
            for a in grps:
                b = RunGroup()
                b.samples = a
                self.groups.append(b)

    def interleave_solvents(self):
        print 'interleave solvents'
        #adds solvents between groups in layout
        self.layout = []
        
        for counter in range(len(self.groups) - 1):
            self.layout.extend(self.groups[counter].layout())
            #create a solvent entry
            solvent = 'solvent'
            self.solvents.append(solvent)
            self.layout.append(solvent)
            
        self.layout.extend(self.groups[len(self.groups) - 1].layout())
        
    def add_pooled_QC_padding(self):
        #add PBQCs at beginning and end of layout
        qc = 'PBQC'
        self.layout.insert(0,qc)
        end_qc = 'PBQC'
        self.layout.append(end_qc)
        
    def add_reagent_blank(self):
        #add a blank to the beginning of the layout
        rb = 'reagent'
        self.layout.insert(0,rb)
        
    def add_solvent_padding(self):
        #add 1 solvent at beginning, 2 at end
        solvent = 'solvent'
        self.layout.insert(0,solvent)
        self.layout.append(solvent)
        self.layout.append(solvent)
        
class GCRunLayout(GenericRunLayout):
    def perform_layout(self):
        #override generic layout to add instrument QC padding and sweeps
        self.clear()
                
        self.randomize()
        self.split(10)
        map(RunGroup.add_pooled_QCs, self.groups)
        map(RunGroup.interleave_sweeps, self.groups)
        self.interleave_solvents()
        self.add_pooled_QC_padding()
        self.add_instrument_QC_padding()
        self.add_reagent_blank()
        self.add_solvent_padding()

    def add_instrument_QC_padding(self):
        qc = 'IQC'
        self.layout.insert(0,qc)
        self.layout.append(qc)