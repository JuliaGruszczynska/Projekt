import json
from urllib.parse import parse_qs

from django.shortcuts import render
from apartments.models import Apartment, FavoriteApartment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def hello_word_view(request):
    apartments = Apartment.objects.all()
    return render(request, "apartments/index.html", {
        "apartments": apartments
    })

def favourites_view(request):
    favourite_apartments = FavoriteApartment.objects.select_related('apartament')
    return render(request, "apartments/favourites.html", {
        "favourite_apartments": favourite_apartments
    })


def add_to_favorites(request):
    if request.method == 'POST':
        apartament_id = request.POST.get('apartament_id')
        body = parse_qs(request.body)
        param_value = body.get('param_name')
        print('apartament_id')
        print(request)


        # Sprawdź, czy oferta istnieje
        try:
            apartment = Apartment.objects.get(apartament_id=apartament_id)
        except Apartment.DoesNotExist:
            return JsonResponse({'message': 'Apartment not found.'}, status=404)


        if FavoriteApartment.objects.filter(apartment=apartment).exists():
            message = 'This apartment is already in favorites.'
        else:
            FavoriteApartment.objects.create(apartment=apartment)
            message = 'Apartment added to favorites.'

        return JsonResponse({'message': message})
    else:
        return JsonResponse({'message': 'Invalid request method.'})