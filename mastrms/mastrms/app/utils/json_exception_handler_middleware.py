from django.http import HttpResponse
import json
import logging

logger = logging.getLogger('mastrms.general')

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
