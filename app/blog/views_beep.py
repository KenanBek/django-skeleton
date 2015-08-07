from django.views.generic import ListView, DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from core import abstracts

from . import models


class BeepList(abstracts.NeverCacheMixin, ListView):
    template_name = "user/blog/beep_list.html"
    model = models.Beep
    paginate_by = 20

    def get_queryset(self):
        return models.Beep.objects.order_by('-modified_at').all()


class BeepCreate(abstracts.NeverCacheMixin, CreateView):
    model = models.Beep
    fields = ['text', ]
    template_name = "user/blog/beep_form.html"
    success_url = reverse_lazy('blog_beep_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BeepCreate, self).form_valid(form)


class BeepUpdate(abstracts.NeverCacheMixin, UpdateView):
    model = models.Beep
    fields = ['text', ]
    template_name = "user/blog/beep_form.html"
    success_url = reverse_lazy('blog_beep_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BeepUpdate, self).form_valid(form)


class BeepDetail(abstracts.NeverCacheMixin, DetailView):
    model = models.Beep
    template_name = "user/blog/beep_detail.html"


class BeepDelete(abstracts.NeverCacheMixin, DeleteView):
    model = models.Beep
    template_name = "user/blog/beep_confirm_delete.html"
    success_url = reverse_lazy('blog_beep_list')

