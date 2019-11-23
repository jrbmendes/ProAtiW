from app.models import *
from django.contrib.auth.models import User, Group
from django.db.models import Q

 # Used in forms 
 # Coments on popover instead of on screen
def popover(fields):
   
    for field in fields:
        help_text = fields[field].help_text
        fields[field].help_text = None
        if help_text != '':
            fields[field].widget.attrs.update({'class':'has-popover', 'data-content':help_text, 'data-placement':'right', 'data-container':'body'})
    return 0


# Persists the state of an HTML input on session
def get_persisted_html(request, key, default, *args, **kwargs):

    # Get the value on the session, using a default if its is not on the session
    value = request.session.get(key, default)

    # See if the value was updated by the user and update the session value
    if request.method == 'GET' and key in request.GET:
        value = request.GET.get(key,default=default);
        request.session[key] = value

    # See if the value was updated by the user and update the session value
    if request.method == 'POST' and key in request.POST:
        value = request.POST.get(key,default=default);
        request.session[key] = value

    if 'cast' in kwargs:
        if kwargs['cast'] == 'int':
            value = int(value)

    return value