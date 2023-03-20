from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Такая почта уже существует!')
            else:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                activateEmail(request, user, form.cleaned_data.get('email'))
                return redirect('signup')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activete_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Дорогой {user}, пожалуйста перейдите на вашу электронную почту {to_email} входящие и нажмите \
             получена ссылка активации для подтверждения и завершения регистрации. Примечание: Посмотрите папку спам.')
    else:
        messages.error(request,
                       f'Проблема с отправкой письма с подтверждением на {to_email}, посмотрите всели вы написали коректно.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Спасибо за ваше подтверждение почты. Сейчас можете зайти в свой аккаунт.')
        return redirect('signin')
    else:
        messages.error(request, 'Ссылка не коректна!')

    return redirect('signup')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'signin.html', {'form': form})


def account(request):
    return render(request, 'account.html')
