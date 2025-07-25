from django.shortcuts import render

# Create your views here.

def hotel_page(request):
    return render(request, 'hotels/hotel.html')
