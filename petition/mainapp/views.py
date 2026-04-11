from django.shortcuts import render, redirect
from .models import Signature
from .forms import SignatureForm
from .models import Signature, Review
import os
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = SignatureForm(request.POST)
        if form.is_valid():
            Signature.objects.create(
                name=form.cleaned_data['name'] or 'Anonym',
                signed=True
            )
            return redirect('index')
    else:
        form = SignatureForm()
    
    count = Signature.objects.count()

    file_path = os.path.join(settings.MEDIA_ROOT, 'petition.pdf')  # замени на имя своего файла
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        size_mb = round(size_bytes / (1024 * 1024), 1)
        file_size = f"{size_mb} MB"
    else:
        file_size = "—"

    return render(request, 'index.html', {
        'form': form,
        'count': count,
        'file_size': file_size
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
