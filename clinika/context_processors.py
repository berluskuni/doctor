__author__ = 'berluskuni'
from .models import Contact


def contact_processors(request):
    return {'contact': Contact.objects.all()}
