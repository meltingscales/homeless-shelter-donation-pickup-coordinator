from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import *
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from donationcoordinator.views import CreateOrUpdateView
from donator.models import User
from org.forms import OrgForm
from org.models import Org


# Create your views here.

def index(request: HttpRequest):
    template_name = 'org/index.html'
    context = {}
    return render(request, template_name, context)


@login_required
def my_org(request: HttpRequest, context={}):
    template_name = 'org/org_detail.html'
    user: User = request.user

    if user.org is not None:
        return HttpResponse("U GOT AN ORG!!!")
    else:
        return HttpResponseRedirect(reverse('org:org_list'))


def org_list(request: HttpRequest, context={}):
    template_name = "org/org_list.html"

    orgs = Org.objects.filter()

    context['orgs_list'] = orgs

    return render(request, template_name, context)


class OrgDetail(DetailView):
    model = Org
    template_name = 'org/org_detail.html'


class OrgCreateOrUpdate(CreateOrUpdateView):
    model = Org
    template_name = 'org/org_edit.html'
    form_class = OrgForm

    def form_valid(self, form):
        form.instance.user = User.objects.get(username=self.request.user.username)

        print("user:")
        print(form.instance.user)

        if (form.instance.user.org is not None):
            self.object = form.instance.user.org

        return super(OrgCreateOrUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('org:org_detail', kwargs={'pk': self.object.id})


class OrgCreate(OrgCreateOrUpdate):
    def form_valid(self, form: OrgForm):
        form.instance.user = User.objects.get(username=self.request.user.username)

        org = form.instance.user.org

        print("Checking if OrgCreate is valid.")

        if org is not None:
            raise ValidationError('You already have an Org, you cannot make multiple ones!')

        return super(OrgCreateOrUpdate, self).form_valid(form)
