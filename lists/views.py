from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.utils.text import slugify

from .models import UserList
from .mixins import OwnerRequiredMixin


class UserListListView(ListView):
    model = UserList


class UserListDetailView(DetailView):
    model = UserList
    slug_field = 'name'
    slug_url_kwarg = 'name'

    # def get_queryset(self):
    # TODO get all books on list


class UserListCreateView(CreateView):
    model = UserList
    fields = ['name']
    success_url = reverse_lazy('lists-view')

    def form_valid(self, form):
        form.instance.name = slugify(form.instance.name)
        new_value = form.cleaned_data['name']
        if UserList.objects.filter(name=new_value).count() > 0:
            form.add_error('name', 'You already have this list')
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserListUpdateView(OwnerRequiredMixin, UpdateView):
    model = UserList
    fields = ['name']
    success_url = reverse_lazy('lists-view')

    def form_valid(self, form):
        form.instance.name = slugify(form.instance.name)
        old_value = UserList.objects.get(pk=self.object.pk).name
        new_value = form.cleaned_data['name']
        # this if is there in case user saves existing value without change
        if old_value != new_value:
            if UserList.objects.filter(name=new_value).count() > 0:
                form.add_error('name', 'You already have this list')
                return self.form_invalid(form)
        return super().form_valid(form)


class UserListDeleteView(OwnerRequiredMixin, DeleteView):
    model = UserList
    success_url = reverse_lazy('lists-view')
