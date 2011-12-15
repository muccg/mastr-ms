from django.utils import simplejson as json
from django.http import HttpResponse


class JSONExceptionHandlerMiddleware(object):

    def process_exception(self, request, exception):
        if not request.is_ajax():
            return 

        err_response = {
            'success': False,
            'msg': str(exception)
        }

        return HttpResponse(json.dumps(err_response), mimetype='application/json')

