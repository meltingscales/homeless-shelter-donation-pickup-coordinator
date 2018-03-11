from django.http import *
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import RestaurantForm, DishForm
from .models import RestaurantReview, Restaurant, Dish


# Create your views here.


def index(request: HttpRequest):
    template_name = 'restaurantapp/index.html'
    context = {}
    return render(request, template_name, context)


class RestaurantDetail(DetailView):
    model = Restaurant
    template_name = 'restaurantapp/restaurant_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = RestaurantReview.RATING_CHOICES
        return context


class RestaurantCreate(CreateView):
    model = Restaurant
    template_name = 'restaurantapp/form.html'
    # success_url = reverse_lazy('restaurant_detail')
    form_class = RestaurantForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RestaurantCreate, self).form_valid(form)


class DishCreate(CreateView):
    model = Dish
    template_name = 'restaurantapp/form.html'
    form_class = DishForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = Restaurant.objects.get(id=self.kwargs['pk'])
        return super(DishCreate, self).form_valid(form)


def review(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    review = RestaurantReview(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        restaurant=restaurant)
    review.save()
    return HttpResponseRedirect(reverse('restaurantapp:restaurant_detail', args=(restaurant.id,)))
