from django.shortcuts import render
import segno, os
from django.contrib.auth.models import User

# Create your views here.


def render_ceateqr_app(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        qr = segno.make_qr(
            content=url
        )
        qr.save(
            out = os.path.abspath(__file__ + f'/../../media/qrcode.png'),
            kind='png'
        )

        return render(request, 'createqr_app/createqrr.html')
    return render(request, 'createqr_app/createqrr.html')