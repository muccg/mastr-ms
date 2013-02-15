from django.utils import simplejson as json
from django.http import HttpResponse
import logging

logger = logging.getLogger('madas_log')

class JSONExceptionHandlerMiddleware(object):

    def process_exception(self, request, exception):
        if not request.is_ajax():
            return 

        err_response = {
            'success': False,
            'msg': str(exception)
        }

        logger.exception(exception)

        return HttpResponse(json.dumps(err_response), mimetype='application/json')

