from madas.repository.models import RunSample, SampleNotInClassException

class RunBuilder(object):
    def __init__(self, run):
        self.run = run

    def validate(self):
        for sample in self.run.samples.all():
            sample.run_filename(self.run)
            
        return True
        
    def generate(self, request):
        try:
            self.validate()
            #if the validate fails we throw an exception
            
            from mako.template import Template
            
            mytemplate = Template(self.run.method.template)
            
            #create the variables to insert
            render_vars = {'username':request.user.username,'run':self.run}
            
            #write filenames into DB
            for rs in RunSample.objects.filter(run=self.run):
                rs.filename = rs.sample.run_filename(self.run)
                rs.save()
            
            #render
            return mytemplate.render(**render_vars)
        except SampleNotInClassException, e:
            return 'Samples in the run need to be in sample classes before they can be used in a run'
        except Exception, e:
            return 'Run validation error ' + str(e)
        