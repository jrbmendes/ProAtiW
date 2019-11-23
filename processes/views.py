import os
from datetime import datetime

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.template import loader, Context, RequestContext

from app.utils import get_persisted_html
from app.models import *


# Create your views here.


@login_required
def structureView(request, activity_id):


    # Get a session value for the active contract, setting a default if it is not present
    #focus_activity = get_persisted_html(request, 'focus_activity', 
    #                                    activity_id, 
    #                                    cast='int')

    focus_activity = Activity.objects.get(id=activity_id)

    tree_list = focus_activity.get_activity_path

    descendant_list = Activity.objects.filter(parent=activity_id).all()
    

    return render(request,'processes/structureView.html',{
                                                            'focus_activity': focus_activity,
                                                            'tree_list': tree_list,
                                                            'descendant_list' : descendant_list
                                                          });