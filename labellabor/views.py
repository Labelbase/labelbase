from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, resolve_url
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from two_factor.views import OTPRequiredMixin
from two_factor.views.utils import class_view_decorator

from labelbase.models import Label, Labelbase
from labelbase.forms import LabelForm, LabelbaseForm
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token

class HomeView(TemplateView):
    template_name = 'home.html'

class LabelbaseDeleteView(DeleteView):
    model = Labelbase
    success_url = "/"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != self.request.user:
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class LabelbaseView(ListView):
    template_name = 'labelbase.html'
    context_object_name = 'label_list'

    def get_queryset(self):
        qs = Label.objects.filter(labelbase__user_id=self.request.user.id,
                                    labelbase_id=self.kwargs['labelbase_id'])
        return qs.order_by("id")

    def get_context_data(self, **kwargs):
        labelbase_id = self.kwargs['labelbase_id']
        context = super(LabelbaseView, self).get_context_data(**kwargs)
        context['labelbase'] = Labelbase.objects.filter(id=labelbase_id, user_id=self.request.user.id).first()
        context['labelform'] = LabelForm(request=self.request, labelbase_id=labelbase_id)
        context['api_token'] = Token.objects.get(user_id=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        labelbase_id = self.kwargs['labelbase_id']
        labelform = LabelForm(request.POST, request=request, labelbase_id=labelbase_id)
        if labelform.is_valid():
            label = labelform.save()
            #TODO: Add success massage
            return HttpResponseRedirect(label.labelbase.get_absolute_url())
        return HttpResponseRedirect("/?error")


class LabelbaseUpdateView(UpdateView):
    model = Labelbase
    fields = ['name', 'fingerprint', 'about']
    form_class = LabelbaseForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(form.instance.get_absolute_url())

class LabelbaseFormView(FormView):
    template_name = 'labelbase_new.html'
    form_class = LabelbaseForm

    def get(self, request, *args, **kwargs):
        return redirect(resolve_url('home'))

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect(form.instance.get_absolute_url())


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        form.save()
        return redirect('registration_complete')


class RegistrationCompleteView(TemplateView):
    template_name = 'registration_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


@class_view_decorator(never_cache)
class ExampleSecretView(OTPRequiredMixin, TemplateView):
    template_name = 'secret.html'
