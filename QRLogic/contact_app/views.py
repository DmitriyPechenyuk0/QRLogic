from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpRequest
# Create your views here.

def render_contact_app(request: HttpRequest):
    context = {'page': 'contacts'}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        
        msg= f'Feedback from {name} ({email})\n\n {description}'

        send_mail(
            'Feedback',
            f'{msg}',
            'qrlogic.practice@gmail.com',
            ['dmitriypechenyuk0@gmail.com'],
            fail_silently=False            
        )



    
    return render(request, 'contact_app/contact.html', context=context)

