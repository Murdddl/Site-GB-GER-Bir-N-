from django.shortcuts import render, redirect, get_object_or_404
from .models import Signature, Review, Question
from .forms import SignatureForm
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q # Для сложного поиска
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    already_signed_cookie = request.COOKIES.get('signed_petition')
    already_signed_ip = Signature.objects.filter(ip_address=ip).exists()

    if request.method == 'POST':
        if already_signed_cookie or already_signed_ip:
            return redirect('index')

        form = SignatureForm(request.POST)
        if form.is_valid():
            response = redirect('index')

            Signature.objects.create(
                name=form.cleaned_data.get('name') or 'Аноним',
                signed=True,
                ip_address=ip
            )

            # 🍪 Ставим cookie на год
            response.set_cookie(
                'signed_petition',
                'true',
                max_age=60 * 60 * 24 * 365,
                httponly=True,
                samesite='Lax'
            )

            return response
    else:
        form = SignatureForm()

    count = Signature.objects.count()

    already_signed = already_signed_cookie or already_signed_ip

    # Размер файла
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
            Review.objects.create(name=name, text=text, status='pending')
            
            # 1. Email уведомление админу о новом отзыве
            send_mail(
                'Новый отзыв на сайте',
                f'Пользователь {name} оставил отзыв: {text}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL], # Добавьте это в settings.py
                fail_silently=True,
            )
            all_reviews = Review.objects.filter(status='approved').order_by('-date')
            return render(request, 'reviews.html', {'reviews': all_reviews})
    
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

def donate(request):
    return render(request, 'donate.html')

@staff_member_required
def moderation(request):
    # Логика добавления нового вопроса (из вашей первой версии)
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

    # Логика отображения списков
    pending = Question.objects.filter(status='pending').order_by('date')
    my_questions = Question.objects.filter(status='approved').order_by('-date')
    
    return render(request, 'moderation.html', {
        'questions': pending,
        'my_questions': my_questions
    })

@staff_member_required
def delete_question(request, question_id):
    if request.method == 'POST':
        Question.objects.filter(id=question_id).delete()
    return redirect('moderation')

@staff_member_required
def answer_question(request, question_id):
    if request.method == 'POST':
        # Используем get_object_or_404 для безопасности
        q = get_object_or_404(Question, id=question_id)
        q.answer = request.POST.get('answer', '')
        q.status = request.POST.get('action', 'pending')
        q.save()
    return redirect('moderation')

@staff_member_required
def moderation_rev(request):
    pending_reviews = Review.objects.filter(status='pending').order_by('-date')
    
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        action = request.POST.get('action')
        
        # Если здесь ошибка, проверьте, что в модели Review есть поле 'status'
        review = get_object_or_404(Review, id=review_id)
        
        if action == 'approve':
            review.status = 'approved'
            review.save()
        elif action == 'delete':
            review.delete()
            
        return redirect('moderation_rev')

    return render(request, 'moderation_rev.html', {'reviews': pending_reviews})

@staff_member_required
def admin_panel(request):
    signatures = Signature.objects.order_by('-id')[:10]
    reviews = Review.objects.order_by('-date')[:10]
    questions = Question.objects.order_by('-date')[:10]

    return render(request, 'admin_panel.html', {
        'signatures': signatures,
        'reviews': reviews,
        'questions': questions,
    })

@staff_member_required
def approve_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        review.status = 'approved'
        review.save()
    return redirect('admin_panel')

@staff_member_required
def delete_review(request, review_id):
    if request.method == 'POST':
        Review.objects.filter(id=review_id).delete()
    return redirect('admin_panel')


