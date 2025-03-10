from django.shortcuts import render
from user_app.models import Profile
from createqr_app.models import QrCode
from django.http import HttpRequest
# from django.contrib import messages

# Create your views here.

# Creating render function to managesub page. | Створення функції рендерингу для сторінки managesub.
def render_managesub_app(request: HttpRequest):
    # Passes the page name to the context. | Передається в context назва сторінки.
    context = {'page': 'managesub'}
    # Checking if the user is registered. | Перевірка на те чи зареєстрований користувач.
    if request.user.is_authenticated:
        # Creating a variable with the value of the number of commercial cells. | Створюємо змінну зі значенням кількості комерційних комірок.
        count_of_cells = request.user.profile.commerce_cells
        # Create a variable with the number of created QR codes. | Створюємо змінну з кількістю створених qr кодів.
        qr_codess = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').count()
        # Create a variable with the number of available commercial cells. | Створюємо змінну з кількістю вільних комерціхних комірок.
        avaible_cells = count_of_cells - qr_codess
        # Checking the method with which the request was sent. | Перевірка на те з яким методом надійшов запит.
        if request.method == 'POST':
            # Creating variables by retrieving data from the request. | Створення зміних з отримуванням даних з запиту.
            action = request.POST.get('action')
            subscribe = request.POST.get('subscribe')
            slot_count = request.POST.get('slot')
            # Condition: "If the user has requested to delete their subscription and their current subscription is not 'free'." | Умова "Якщо користувач зробив запит видалити його підписку та його поточна підписку не є 'free'".
            if action == 'killsub' and request.user.profile.subscription != 'free':
                # The current user is granted a "free" subscription. | Поточному користувачеві видаєтся 'free' підписка.
                request.user.profile.subscription = 'free'

            # Condition: "If the subscription type is 'free', the user is granted the subscription." | Умова "якщо тип обраної підписки 'free' користувачу видаєтся підписка".
            if subscribe == 'free':
                # The current user is granted a "free" subscription. | Поточному користувачеві видаєтся 'free' підписка.
                request.user.profile.subscription = 'free'

            # Condition: "If the subscription type is 'standart', the user is granted the subscription." | Умова "якщо тип обраної підписки 'standart' користувачу видаєтся підписка".
            if subscribe == 'standart':
                # The current user is granted a 'standart' subscription. | Поточному користувачеві видаєтся 'standart' підписка.
                request.user.profile.subscription = 'standart'

            # Condition: "If the subscription type is 'pro', the user is granted the subscription." | Умова "якщо тип обраної підписки 'pro' користувачу видаєтся підписка".
            if subscribe == 'pro':
                # The current user is granted a 'standart' subscription. | Поточному користувачеві видаєтся 'pro' підписка.
                request.user.profile.subscription = 'pro'

            # Condition: "If the subscription type is 'commerce', the user is granted the subscription." | Умова "якщо тип обраної підписки 'commerce' користувачу видаєтся підписка".
            if subscribe == 'commerce':
                # The current user is granted a commercial subscription. | Поточному користувачеві видаєтся комерсійна підписка.
                request.user.profile.commerce = True
            # Condition: "If the number of cell slots is not an empty string." | Умова "Якщо кількість слотів комірок не є пустою строкою".
            if slot_count != '':
                # Overwrite the variable with strict typing as an integer. | Перезаписуємо змінну з суворою типізацією цілого числа.
                slot_count = int(slot_count)
                # Add cells to the current user. | Додаємо поточному користувачу комірки.
                request.user.profile.commerce_cells = request.user.profile.commerce_cells + slot_count
                # Overwrite the variable with the number of cells after adding. | Перезаписуємо у змінну кількість комірок після додавання
                count_of_cells = request.user.profile.commerce_cells
                # Store the number of QR codes created by the user with the "commerce" type in a variable. | Записуємо у змінну кількість qr кодів створених користувачем з типом "commerce".
                qr_codess = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').count()
                # Store the number of available cells in a variable. | Записуємо у змінну кількість вільних комірок
                avaible_cells = count_of_cells - qr_codess
            # Saving all changes to the database. | Зберігаємо усі зміни до бази
            request.user.profile.save()

        # Passing the number of available cells to the context. | Передання кількості вільних комірок до контексту
        context = {
                'page': 'managesub',
                'avaible_cells': avaible_cells}
        # Display the managesub page to the user. | Відображаємо сторінку managesub користувачу.
        return render(request, 'managesub_app/managesub.html', context=context)
    # Condition: "if the user has not passed the registration verification". | Умова "якщо користувач не пройшов перевірку на реєстрацію".
    else:
        # A page is displayed with the message "You need to log in to your account". | Відображаєтся сторінка з написом "Ви маєте увійти в аккаунт".
        return render(request, 'createqr_app/authentication_required.html', context=context)


