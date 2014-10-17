from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
import jsonpickle

from core.decorators import convert_to_json, anonymous_required


@anonymous_required
@convert_to_json
@ensure_csrf_cookie
def login(request):
    if request.is_ajax():
        result = jsonpickle.decode(request.body)
        username = result.username
        password = result.password
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return _('You have successfully logged in.')
            else:
                raise Exception(_('Non active user.'))
        else:
            raise Exception(_('Wrong username or password.'))

    raise Exception(_("Support only AJAX (JSON format)."))

