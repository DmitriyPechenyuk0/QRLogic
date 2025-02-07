from django.shortcuts import render

# Create your views here.

def render_managesub_app(request):
    context = {'page': 'managesub'}
    if request.user.is_authenticated:
        return render(request, 'managesub_app/managesub.html', context=context)
    else:
        return render(request, 'createqr_app/authentication_required.html', context=context)


