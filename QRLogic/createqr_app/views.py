from django.shortcuts import render, redirect
import segno, os
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import QrCode
from .form import QRCodeForm

# Create your views here.


#def render_ceateqr_app(request):
    # if request.method == 'POST':
    #     url = request.POST.get('url')
    #     qr = segno.make_qr(
    #         content=url
    #     )
    #     qr.save(
    #         out = os.path.abspath(__file__ + f'/../../media/qrcode.png', kind='png'),
    #         )
        
    #     return render(request, 'createqr_app/createqrr.html')
@login_required
def create_qr(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            qr_instance = form.save(commit=False)
            qr_instance.owner = request.owner
            qr_instance.save()
            return redirect('qr_list')
    else:
        form = QRCodeForm()
    return render(request, 'createqrr.html', {'form': form})

    
@login_required
def qr_list(request):
    qrcodes = QrCode.objects.filter(user=request.user) 
    return render(request, 'yourqrr.html', {'qrcodes': qrcodes})
