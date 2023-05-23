import json
from urllib.parse import parse_qs

from django.shortcuts import render
from apartments.models import Apartment, FavoriteApartment
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.http import JsonResponse

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

@api_view(['POST'])
def add_to_favorites(request):
    if request.method == 'POST':
        apartament_id = request.data['apartament_id']

        # Sprawdź, czy oferta istnieje
        try:
            apartment = Apartment.objects.get(apartament_id=apartament_id)
        except Apartment.DoesNotExist:
            return JsonResponse({'message': 'Apartment not found.'}, status=404)


        if FavoriteApartment.objects.filter(apartament=apartment).exists():
            message = 'This apartment is already in favorites.'
        else:
            FavoriteApartment.objects.create(apartament=apartment)
            message = 'Apartment added to favorites.'

        return JsonResponse({'message': message})
    else:
        return JsonResponse({'message': 'Invalid request method.'})

@api_view(['POST'])
def remove_from_favorites(request):
    if request.method == 'POST':
        id = request.data['id']
        print('id')
        print(id)
        # Odczytaj inne potrzebne dane z request.POST

        # Sprawdź, czy apartament istnieje w ulubionych
        try:
            favorite_apartment = FavoriteApartment.objects.get(id=id)
        except FavoriteApartment.DoesNotExist:
            return JsonResponse({'message': 'Apartment not found in favorites.'})

        # Usuń apartament z ulubionych
        print('favorite_apartment.id')
        print(favorite_apartment.id)
        favorite_apartment.delete()

        # Zwróć odpowiedź JSON
        return JsonResponse({'message': 'Apartment removed from favorites.'})

    # Zwróć odpowiedź JSON dla innych metod niż POST
    return JsonResponse({'message': 'Invalid request method.'})

@api_view(['POST'])
def send_favorite_details(request):
    if request.method == 'POST':
        id = request.data['id']
        email = request.data['email']

        # Pobierz szczegóły ulubionego apartamentu
        try:
            favorite_apartment = FavoriteApartment.objects.get(id=id)
            apartment = favorite_apartment.apartament
        except FavoriteApartment.DoesNotExist:
            return JsonResponse({'message': 'Apartment not found in favorites.'})

        # Przygotuj treść wiadomości e-mail
        subject = 'Favorite Apartment Details'
        message = f'Place: {apartment.place}\nDescription: {apartment.description}\nPrice: {apartment.price}\nArea: {apartment.area}\nPrice per sqm: {apartment.price_per_m}\nRooms: {apartment.rooms}\nOffer URL: {apartment.offer_url}'
        recipient_list = [email]

        # Wyślij e-mail
        send_mail(subject, message, from_email=None, recipient_list=recipient_list)

        # Zwróć odpowiedź JSON
        return JsonResponse({'message': 'Apartment details sent to email.'})

    # Zwróć odpowiedź JSON dla innych metod niż POST
    return JsonResponse({'message': 'Invalid request method.'})
