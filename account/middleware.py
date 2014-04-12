from django.http import HttpResponseForbidden
from account.views import forbidden

class Custom403Middleware(object):
      """Catches 403 responses and renders 403.html"""

      def process_response(self, request, response):
          if isinstance(response, HttpResponseForbidden):
             return forbidden(request)
          else:
             return response