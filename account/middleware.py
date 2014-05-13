from django.http import HttpResponseForbidden, HttpResponseNotFound
from account.views import forbidden, not_found

class Custom403Middleware(object):
      """Catches 403 responses and renders 403.html"""

      def process_response(self, request, response):
          if isinstance(response, HttpResponseForbidden):
             return forbidden(request)
          else:
             return response

class Custom404Middleware(object):
      """Catches 404 responses and renders error_page.html"""

      def process_response(self, request, response):
          if isinstance(response, HttpResponseNotFound):
             return not_found(request)
          else:
             return response    
         
         
from django.conf import settings
from django_cas.decorators import login_required

class LoginRequiredMiddleware(object):
    def __init__(self):
        self.public_views = [self.get_view(v) for v in [
            "account.views.login",
            "django_cas.views.logout",
            "account.views.product_index"
            ]]
    
    def get_view(self, view_path):
        i = view_path.rfind('.')
        module_path, view_name = view_path[:i], view_path[i+1:]
        module = __import__(module_path, globals(), locals(), [view_name])
        return getattr(module, view_name)

    def matches_public_view(self, view):
        for public_view in self.public_views:
            if view == public_view:
                return True
        return False

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Substitute for daemon
        from buy.utils import notify_users_closed_auctions
        notify_users_closed_auctions()
        if request.user.is_authenticated() or self.matches_public_view(view_func):
            return None
        else:
            return login_required(view_func)(request, *view_args, **view_kwargs)
      
        