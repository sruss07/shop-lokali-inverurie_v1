from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Bike, Brand
from .forms import BikeForm


def all_bikes(request):
    """ Show all bikes, including sorting and search queries """

    bikes = Bike.objects.all()
    query = None
    bike_brands = None
    bike_name = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                bikes = bikes.annotate(lower_name=Lower('name'))
            if sortkey == 'brand':
                sortkey = 'brand__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            bikes = bikes.order_by(sortkey)
      
        if 'brand' in request.GET:
            bike_brands = request.GET["brand"].split(',')
            bikes = bikes.filter(brand__name__in=bike_brands)
            bike_brands = Brand.objects.filter(name__in=bike_brands)

        if 'bike' in request.GET:
            bike_name = request.GET['bike']
            bikes = bikes.filter(name=bike_name)
          

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search details!")
                return redirect(reverse('bikes'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            bikes = bikes.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'bikes': bikes,
        'search_term': query,
        'current_brands': bike_brands,
        'current_bike': bike_name,
        'current_sorting': current_sorting,
    }

    return render(request, 'bikes/bikes.html', context)


def bike_detail(request, bike_id):
    """ Show individual bike details """

    bike = get_object_or_404(Bike, pk=bike_id)

    context = {
        'bike': bike,
    }

    return render(request, 'bikes/bike_detail.html', context)


@login_required
def add_bike(request):
    """ Add a bike to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can add new bikes!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = BikeForm(request.POST, request.FILES)
        if form.is_valid():
            bike = form.save()
            messages.success(request, 'Successfully added new bike!')
            return redirect(reverse('bike_detail', args=[bike.id]))
        else:
            messages.error(
                request,
                'Failed to add a new bike. Please ensure the form is valid!')
    else:
        form = BikeForm()

    template = 'bikes/add_bike.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_bike(request, bike_id):
    """ Edit a bike in the store """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners can edit existing bikes!')
        return redirect(reverse('home'))

    bike = get_object_or_404(Bike, pk=bike_id)
    if request.method == 'POST':
        form = BikeForm(request.POST, request.FILES, instance=bike)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated an existing bike!')
            return redirect(reverse('bike_detail', args=[bike.id]))
        else:
            messages.error(
                request, 'Failed to update existing bike. Please ensure the form is valid!')
    else:
        form = BikeForm(instance=bike)
        messages.info(request, f'You are editing {bike.name}')

    template = 'bikes/edit_bike.html'
    context = {
        'form': form,
        'bike': bike,
    }

    return render(request, template, context)


@login_required
def delete_bike(request, bike_id):
    """ Delete a bike from the store """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners can delete existing bikes!')
        return redirect(reverse('home'))

    bike = get_object_or_404(Bike, pk=bike_id)
    bike.delete()
    messages.success(request, 'Existing bike deleted successfully!')
    return redirect(reverse('bikes'))
