from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.
# Creating render function to home page. | Створення функції рендерингу для сторінки home.
def render_home_app(request: HttpRequest):
    # Passes the page name to the context. | Передається в context назва сторінки.
    context = {'page': 'home'}
    # Display the home page to the user. | Відображаємо сторінку home користувачу.
    return render(request, 'home_app/home.html', context=context)