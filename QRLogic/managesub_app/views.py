from django.shortcuts import render
from user_app.models import Profile
# from django.contrib import messages

# Create your views here.


def render_managesub_app(request):
    context = {'page': 'managesub'}

    if request.user.is_authenticated:
        # if request.method == 'POST':
            # action = request.POST.get('action')
            # plans = request.POST.get('plans')
            # if action == 'killsub' and plans != 'free':
            #     request.user.profile.subscription = 'free'
            
            # if plans == 'free':
            #     request.user.profile.subscription = 'free'
            # if plans == 'standart':
            #     request.user.profile.subscription = 'standart'
            # if plans == 'pro':
            #     request.user.profile.subscription = 'pro'
            
            # request.user.profile.save()
        return render(request, 'managesub_app/managesub.html', context=context)
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)


