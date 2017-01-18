from django.utils.deprecation import MiddlewareMixin
from stronghold.middleware import LoginRequiredMiddleware

class LoginRequiredShimMiddleware(MiddlewareMixin, LoginRequiredMiddleware):
    pass
