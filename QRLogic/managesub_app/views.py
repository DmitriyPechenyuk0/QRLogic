from django.shortcuts import render
from user_app.models import Profile
from createqr_app.models import QrCode
from django.http import HttpRequest
# from django.contrib import messages

# Create your views here.


def render_managesub_app(request: HttpRequest):
    context = {'page': 'managesub'}

    if request.user.is_authenticated:

        count_of_cells = request.user.profile.commerce_cells
        qr_codess = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').count()

        avaible_cells = count_of_cells - qr_codess

        if request.method == 'POST':
            action = request.POST.get('action')
            subscribe = request.POST.get('subscribe')
            slot_count = request.POST.get('slot')
            if action == 'killsub' and request.user.profile.subscription != 'free':
                request.user.profile.subscription = 'free'
            if subscribe == 'free':
                request.user.profile.subscription = 'free'
            if subscribe == 'standart':
                request.user.profile.subscription = 'standart'
            if subscribe == 'pro':
                request.user.profile.subscription = 'pro'
            if subscribe == 'commerce':
                request.user.profile.commerce = True
            if slot_count != '':
                
                slot_count = int(slot_count)
                request.user.profile.commerce_cells = request.user.profile.commerce_cells + slot_count

                count_of_cells = request.user.profile.commerce_cells
                qr_codess = QrCode.objects.filter(owner=request.user.profile, type_qr = 'commerce').count()

                avaible_cells = count_of_cells - qr_codess

            request.user.profile.save()


        context = {
                'page': 'managesub',
                'avaible_cells': avaible_cells}
        return render(request, 'managesub_app/managesub.html', context=context)
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)


