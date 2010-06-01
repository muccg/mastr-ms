from madas.repository.models import RunSample

class RunValidationException(Exception):
    pass

class RunBuilder(object):
    def __init__(self, run):
        self.run = run

    def validate(self):
        for sample in self.run.samples.all():
            try:
                sample.run_filename(self.run)
            except:
                return False
            
        return True
        
    def generate(self, request):
        if self.validate():
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
        else:
            raise RunValidationException
        