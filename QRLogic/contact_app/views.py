from django.shortcuts import render

# Create your views here.

def render_contact_app(request):
    return render(request, 'contact_app/contact.html')

