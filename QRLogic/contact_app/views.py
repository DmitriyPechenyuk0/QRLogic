from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpRequest
# Create your views here.

# Creating render function to contact page. | Створення функції рендерингу для сторінки contact.
def render_contact_app(request: HttpRequest):
    # Passes the page name to the context. | Передається в context назва сторінки.
    context = {'page': 'contacts'}
    # Checking the method with which the request was sent. | Перевірка на те з яким методом надійшов запит.
    if request.method == 'POST':
        # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        # Store in a variable the layout of the message that will be sent to the email. | Записуємо у змінну макет повідомлення яке буде відправлене до пошти
        msg= f'Feedback from {name} ({email})\n\n {description}'
        # Send the customer's feedback to the email. | Відсилаємо відгук клієнта до пошти      
        send_mail(
            'Feedback',
            f'{msg}',
            'qrlogic.practice@gmail.com',
            ['dmitriypechenyuk0@gmail.com'],
            fail_silently=False            
        )
    # Display the contact page to the user. | Відображаємо сторінку contact користувачу.
    return render(request, 'contact_app/contact.html', context=context)

