import googlemaps
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.utils.translation import gettext as _

from donationcoordinator.views import CreateOrUpdateView
from .forms import *
from .libs import ItemList
from .models import User, Home, HomeLocation


# Create your views here.

def index(request: HttpRequest):
    template_name = 'donator/index.html'
    context = {}
    return render(request, template_name, context)


def signup(request):
    template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, template_name, {'form': form})


def my_homes(request, context={}):
    """A User wants a list of their Homes."""
    template_name = "donator/home_list.html"
    user: User = request.user

    if not user.is_authenticated:
        context["message"] = "You must be logged in to view a list of your homes!"
        return render(request, template_name, context)

    homes = Home.objects.filter(user=user)

    context["homes_list"] = homes

    return render(request, template_name, context)

# see https://stackoverflow.com/questions/17833117/djangos-createview-is-not-saving-an-object
class HomeCreateOrUpdate(CreateOrUpdateView):
    model = Home
    template_name = 'donator/home_edit.html'
    form_class = HomeForm
    geo_result = {}
    gmaps_json = {}

    def save_location(self, form: HomeForm):

        loc = self.geo_result[0]['geometry']['location']
        lat = loc['lat']
        lng = loc['lng']

        location = HomeLocation.from_lat_lon(lat=lat, lng=lng, data=self.geo_result)

        self.object.location = location
        self.object.save()

    def get_success_url(self):
        return reverse('donator:home_detail', kwargs={'pk': self.object.id})

    def post(self, request: HttpRequest, *args, **kwargs):
        return super().post(self, request, *args, **kwargs)

    def form_valid(self, form: HomeForm):

        form.instance.user = User.objects.get(username=self.request.user.username)

        print(form.data)

        locs = form.get_loc_data_as_string()

        if self.geo_result == {}:  # if it's empty
            gm = googlemaps.Client(key=settings.GEOPOSITION_GOOGLE_MAPS_API_KEY)

            self.geo_result = gm.geocode(locs)

        if self.geo_result == {}:  # they entered 'moon cheese base' or 'nowheresville tenessee'
            raise ValidationError(
                _("Location could not be understood by Google Maps!")
            )

        ret = super(HomeCreateOrUpdate, self).form_valid(form)

        if ret:
            self.save_location(form)

        return ret


class HomeDetail(DetailView):
    model = Home
    template_name = 'donator/home_detail.html'

    def get_object(self, queryset=None) -> Home:
        """ Hook to ensure object is owned by request.user. """

        obj = super(HomeDetail, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super(HomeDetail, self).get_context_data(**kwargs)
        return context


class HomeDelete(DeleteView):
    model = Home
    template_name = 'donator/home_delete.html'

    def get_object(self, queryset=None) -> Home:
        """ Hook to ensure object is owned by request.user. """

        obj = super(HomeDelete, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse('donator:home_list')

    def form_valid(self, request: HttpRequest):

        if 'home_name' not in request.POST:
            return False

        form_name = request.POST['home_name']
        home_name = self.get_object().name

        return form_name == home_name  # make sure they type the name to confirm

    def post(self, request: HttpRequest, *args, **kwargs):

        if self.form_valid(request):
            print("Form is valid for delete!")
            self.get_object().delete()
            return HttpResponseRedirect(self.get_success_url())
        else:  # they can't delete
            context = {
                'error_message': 'Cannot delete! You must type in the home\'s name to confirm!',
                'home': self.get_object(),
            }

            return render(request, self.template_name, context)


class ItemsUpdate(UpdateView):
    slug_field = \
        slug_url_kwarg = 'pk'

    model = Items
    template_name = 'donator/form.html'
    form_class = ItemsForm
    illegal_keys = [  # keys we do NOT want in our form
        'csrfmiddlewaretoken'
    ]

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def clean_form(self) -> dict:
        """Remove anything that isn't an {'item':number} value in
        this form's POST data."""
        d = {}

        for key, val in self.request.POST.items():
            if key not in self.illegal_keys:
                try:
                    key = key.replace(ItemList.space_replacer, ' ')
                    val = int(val)

                    d[key] = val
                except:
                    pass

        return d

    def form_valid(self, form):
        user = self.request.user

        homeid = self.kwargs['pk']
        self.home = Home.objects.get(pk=homeid)  # TODO is this a risk? idk.

        if not self.home.user == user:  # make sure they own the home
            raise PermissionDenied

        return True

    def post(self, request: HttpRequest, *args, **kwargs):

        if self.form_valid(request):
            il = ItemList()

            formDict = self.clean_form()
            # print("Flattened data")
            # print(formDict)

            il.apply_flat_dict(formDict)
            # print("Final data:")
            # print(il.data)

            self.home.items.data = il.data
            self.home.items.save()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponse("ur items ar bad :(")
