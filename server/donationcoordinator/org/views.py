from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import *
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from donationcoordinator.views import CreateOrUpdateView
from donator.models import User, Home
from org.forms import OrgForm, HomeSearchForm
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

    @login_required
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

    @login_required
    def get_success_url(self):
        return reverse('org:org_detail', kwargs={'pk': self.object.id})


class OrgDetail(DetailView):
    model = Org
    template_name = 'org/org_detail.html'


class OrgCreate(OrgCreateOrUpdate):
    def form_valid(self, form: OrgForm):
        user: User = self.request.user
        org: Org = user.org_or_none()

        if org is not None:
            raise ValidationError('You already have an Org, you cannot make multiple ones!')

        form.save()

        User.objects.filter(pk=user.pk).update(org=form.instance)

        return super(OrgCreateOrUpdate, self).form_valid(form)

def searchHomeList(request: HttpRequest):
    template_name = 'org/home_list.html'
    context = {}

    form = HomeSearchForm(request.GET or None)  # create form from GET data

    if form.is_valid():  # if valid
        context['form'] = form  # create form from that data
    else:
        context['form'] = HomeSearchForm()  # create blank form

    miles = HomeSearchForm.Meta.default_miles
    if 'miles' in request.GET:
        miles = request.GET['miles']

    org: Org = request.user.org_or_none()

    if org is None:
        return render(request, 'index.html', 'You need an Org to view a list of homes!')

    homesResults = Home.get_homes_locations_near(
        radius=miles,
        lat=org.location.lat(),
        lon=org.location.lon(),
    )
    homesResults = sorted(homesResults, key=lambda d: d['distance'])  # sort by closest

    context['homes_results'] = homesResults

    if len(request.GET.keys()) == 0:  # they did not give us any arguments
        context['message'] = 'hi org! You didn\'t give this view any arguments! Here\'s a default view!'
    elif 'miles' in request.GET:
        context['message'] = 'OH SO U WANT ' + str(request.GET['miles'] + "MILES DO U??")


    return render(request, template_name, context)
