from django.shortcuts import render
# TODO:Replce dropdown with Category and make it dynamic from the backend
# TODO:Each news --> Title Cat write up date picture
# TODO:Create a page for read only where the link of an article leads to
#  that page so that a user can read the news
# TODO: The hompage will only show the picture and title with link embedded leading to the article
# TODO: Homepage will have a section that shows the news under various cat using a slider


# Create your views here.sss

from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')
