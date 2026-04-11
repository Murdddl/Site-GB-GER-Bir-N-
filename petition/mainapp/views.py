from django.shortcuts import render, redirect
from .models import Signature
from .forms import SignatureForm
from .models import Signature, Review
import os
from django.conf import settings

def index(request):
    already_signed = False
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    
    if request.method == 'POST':
        if Signature.objects.filter(ip_address=ip).exists():
            already_signed = True
        else:
            form = SignatureForm(request.POST)
            if form.is_valid():
                Signature.objects.create(
                    name=form.cleaned_data['name'] or 'Аноним',
                    signed=True,
                    ip_address=ip
                )
                return redirect('index')
    else:
        form = SignatureForm()

    count = Signature.objects.count()
    already_signed = Signature.objects.filter(ip_address=ip).exists()

    # размер файла
    file_path = os.path.join(settings.MEDIA_ROOT, 'Appell.pdf')
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        size_mb = round(size_bytes / (1024 * 1024), 1)
        file_size = f"{size_mb} МБ"
    else:
        file_size = "—"

    return render(request, 'index.html', {
        'form': form,
        'count': count,
        'file_size': file_size,
        'already_signed': already_signed
    })

def reviews(request):
    return render(request, 'reviews.html')

def reviews(request):
    if request.method == 'POST':
        name = request.POST.get('name') or 'Anonym'
        text = request.POST.get('text')
        if text:
            Review.objects.create(name=name, text=text)
            return redirect('reviews')
    
    latest_reviews = Review.objects.order_by('-date')[:10]
    total_count = Review.objects.count()
    return render(request, 'reviews.html', {
        'reviews': latest_reviews,
        'total_count': total_count
    })

def all_reviews(request):
    reviews = Review.objects.order_by('-date')
    return render(request, 'all_reviews.html', {'reviews': reviews})
