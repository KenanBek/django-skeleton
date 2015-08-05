from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def index(request, template='moderator/common/index.html'):
    context = {}
    return render(request, template, context)

