from django.shortcuts import render, redirect, get_object_or_404
from .models import Signature, Review, Question
from .forms import SignatureForm
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q # Для сложного поиска
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

def index(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    
    if request.method == 'POST':
        if not Signature.objects.filter(ip_address=ip).exists():
            form = SignatureForm(request.POST)
            if form.is_valid():
                Signature.objects.create(
                    name=form.cleaned_data.get('name') or 'Аноним',
                    signed=True,
                    ip_address=ip
                )
                return redirect('index')
        else:
            form = SignatureForm()
    else:
        form = SignatureForm()

    count = Signature.objects.count()
    already_signed = Signature.objects.filter(ip_address=ip).exists()

    # Оптимизация: расчет размера файла
    file_path = os.path.join(settings.MEDIA_ROOT, 'Appell.pdf')
    file_size = "—"
    if os.path.exists(file_path):
        size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 1)
        file_size = f"{size_mb} МБ"

    goal = 1000
    percent = min(round((count / goal) * 100), 100)

    return render(request, 'index.html', {
        'form': form,
        'count': count,
        'file_size': file_size,
        'already_signed': already_signed,
        'percent': percent,
    })

def reviews(request):
    if request.method == 'POST':
        name = request.POST.get('name') or 'Anonym'
        text = request.POST.get('text')
        if text:
            Review.objects.create(name=name, text=text)
            
            # 1. Email уведомление админу о новом отзыве
            send_mail(
                'Новый отзыв на сайте',
                f'Пользователь {name} оставил отзыв: {text}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL], # Добавьте это в settings.py
                fail_silently=True,
            )
            return redirect('reviews')
    
    latest_reviews = Review.objects.order_by('-date')[:10]
    total_count = Review.objects.count()
    return render(request, 'reviews.html', {
        'reviews': latest_reviews,
        'total_count': total_count
    })

def all_reviews(request):
    # 2. Пагинация (10 отзывов на страницу)
    reviews_list = Review.objects.order_by('-date')
    paginator = Paginator(reviews_list, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'all_reviews.html', {'page_obj': page_obj})

def faq(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    already_asked = False
    if request.method == 'POST':
        already_asked = Question.objects.filter(ip_address=ip, status='pending').exists()
        if not already_asked:
            question = request.POST.get('question')
            if question:
                Question.objects.create(question=question, ip_address=ip)
                return redirect('faq')
    
    # Важно: эта переменная должна быть определена ДО рендера
    already_asked = Question.objects.filter(ip_address=ip, status='pending').exists()
    questions = Question.objects.filter(status='approved').order_by('-date')
    
    return render(request, 'faq.html', {
        'questions': questions, 
        'already_asked': already_asked
    })

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
        # Используем get_object_or_404 для безопасности
        q = get_object_or_404(Question, id=question_id)
        q.answer = request.POST.get('answer', '')
        q.status = request.POST.get('action', 'pending')
        q.save()
    return redirect('moderation')

def donate(request):
    return render(request, 'donate.html')

@login_required # Этот "декоратор" выкинет любого анонима на страницу логина
def moderation(request):
    # Ваш код отображения вопросов для одобрения
    return render(request, 'moderation.html', context)