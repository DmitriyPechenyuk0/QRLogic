from django.shortcuts import render
from user_app.models import Profile
# from django.contrib import messages

# Create your views here.


def render_managesub_app(request):
    context = {'page': 'managesub'}

    if request.user.is_authenticated:
        if request.method == 'POST':
            action = request.POST.get('action')
            subscribe = request.POST.get('subscribe')
            if action == 'killsub' and request.user.profile.subscription != 'free':
                request.user.profile.subscription = 'free'
            if subscribe == 'free':
                request.user.profile.subscription = 'free'
            if subscribe == 'standart':
                request.user.profile.subscription = 'standart'
            if subscribe == 'pro':
                request.user.profile.subscription = 'pro'
            
            request.user.profile.save()
        return render(request, 'managesub_app/managesub.html', context=context)
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)


