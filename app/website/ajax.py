from django.contrib.auth.decorators import login_required
from core.decorators import json

from website import logic


@login_required
@json
def post(request, post_id, post_slug):
    post_item = logic.get_post(post_id, post_slug)
    return post_item

