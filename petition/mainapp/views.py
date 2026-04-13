from django.shortcuts import render, redirect
from .models import Signature
from .forms import SignatureForm
from .models import Signature, Review
import os
from django.conf import settings
from .models import Signature, Review, Question
from django.contrib.auth.decorators import login_required

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

def faq(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            Question.objects.create(question=question)
            return redirect('faq')
    
    questions = Question.objects.filter(status='approved').order_by('-date')
    return render(request, 'faq.html', {'questions': questions})

@login_required
def moderation(request):
    if request.method == 'POST' and 'new_question' in request.POST:
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        if question and answer:
            Question.objects.create(
                question=question,
                answer=answer,
                status='approved'
            )
            return redirect('moderation')

    pending = Question.objects.filter(status='pending').order_by('date')
    my_questions = Question.objects.filter(status='approved').order_by('-date')
    return render(request, 'moderation.html', {
        'questions': pending,
        'my_questions': my_questions
    })

@login_required
def delete_question(request, question_id):
    if request.method == 'POST':
        Question.objects.filter(id=question_id).delete()
    return redirect('moderation')

@login_required
def answer_question(request, question_id):
    if request.method == 'POST':
        q = Question.objects.get(id=question_id)
        q.answer = request.POST.get('answer', '')
        q.status = request.POST.get('action', 'pending')
        q.save()
    return redirect('moderation')