from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import *
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from donationcoordinator.views import CreateOrUpdateView
from donator.models import User, Home
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
    org: Org = user.org

    if org is not None:
        return render(request, OrgDetail.template_name, {'org': org, 'can_edit_org': True})
    else:
        return HttpResponseRedirect(reverse('org:org_list'))


def org_list(request: HttpRequest, context={}):
    template_name = "org/org_list.html"

    orgs = Org.objects.filter()

    context['orgs_list'] = orgs

    return render(request, template_name, context)


class OrgCreateOrUpdate(CreateOrUpdateView):
    model = Org
    template_name = 'org/org_edit.html'
    form_class = OrgForm

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)

        # print("user:")
        # print(user)
        # print("user's org:")
        # print(user.org)

        # print("Current Org being edited:")
        # print(form.instance)

        if user.org.pk != form.instance.pk:
            raise ValidationError("You do not own this Org and cannot edit it!")

        return super(OrgCreateOrUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('org:org_detail', kwargs={'pk': self.object.id})


class OrgDetail(DetailView):
    model = Org
    template_name = 'org/org_detail.html'


class OrgCreate(OrgCreateOrUpdate):
    def form_valid(self, form: OrgForm):
        user: User = self.request.user
        org: Org = user.org_or_none()

        # print("Checking if OrgCreate is valid.")

        # print("User:")
        # print(user)

        if org is not None:
            raise ValidationError('You already have an Org, you cannot make multiple ones!')

        # print("User apparently does not have an Org.")

        form.save()

        User.objects.filter(pk=user.pk).update(org=form.instance)

        return super(OrgCreateOrUpdate, self).form_valid(form)


class HomeList(ListView):
    model = Home
    template_name = 'org/home_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        GET = self.request.GET

        if 'miles' in GET:
            homesResults = Home.get_homes_locations_near(radius=GET['miles'])
        else:
            homesResults = Home.get_homes_locations_near()  # get near locations

        homesResults = sorted(homesResults, key=lambda d: d['distance'])  # sort by closest

        if len(self.request.GET.keys()) == 0:  # they did not give us any arguments
            context['message'] = 'hi org! You did\'nt give this view any arguments! Here\'s a default view!'
        elif 'miles' in self.request.GET:
            context['message'] = 'OH SO U WANT ' + str(self.request.GET['miles'] + "MILES DO U??")

        context['homes_results'] = homesResults

        return context
