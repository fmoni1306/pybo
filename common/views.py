from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from common.forms import UserForm, ChangeForm
from django.contrib.auth.models import User
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from pybo.forms import QuestionForm
from pybo.models import Question, Answer


def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 회원가입후 바로 로그인을 위한 함수
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})


@csrf_exempt
def find(request):
    """
    비밀번호 찾기
    """
    if request.method == 'POST':
        if request.POST['num_check'] == request.POST['num']:
            context = {"result": "success"}
        else:
            context = {"result": "fail"}

        return JsonResponse(context, safe=False)
    else:
        return render(request, 'common/find_password.html')


@csrf_exempt
def send(request):
    """
    이메일 인증번호 보내기
    """
    if request.method == 'POST':
        if request.is_ajax():
            mail = request.POST['email']
            print(mail)
            ran_num = randint(1000, 9999)
            if User.objects.filter(email=mail):  # get 은 조회되는 데이터가 2개 이상일 경우 에러 발생 get 으로 조회할때 결과없을때 예외뜨는거 확인
                send_mail(
                    'Pybo 인증',
                    '인증번호는[%d]' % ran_num,
                    'fmoni1306@gmail.com',
                    [mail],
                    fail_silently=False,
                )
                user = User.objects.values().get(email=mail)
                context = {'result': 'success', 'num': ran_num, 'id': user['id']}
            else:
                context = {'result': 'fail'}
        return JsonResponse(context)  # safe = default = True 로서 변환할 데이터의 타입이 dict 인지 확인합니다. dict 가 아닐 경우에는 False 로 설정해주어야 합니다.


@csrf_exempt
def change(request, user_id):
    """
    비밀번호바꾸기
    """
    # 접근 제한 걸어야함
    changer = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=changer)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)  # 회원가입후 바로 로그인을 위한 함수
            # login(request, user)
            return redirect('index')
        else:
            return render(request, 'common/change_form.html', {'form': form})
    else:
        form = ChangeForm(instance=changer)
        return render(request, 'common/change_form.html', {'form': form})


@csrf_exempt
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # 여러개를 받아와야 하기 떄문에 get 이 아닌 filter 를 사용 * null 인 경우도 있기 때문에 404함수 사용 못함
    question = Question.objects.filter(author_id=user.id)
    answer = Answer.objects.filter(author_id=user.id)  # 여러개를 받아와야 하기 떄문에 get 이 아닌 filter 를 사용

    return render(request, "common/profile.html", {"user": user, "question": question, "answer": answer})

def page_not_found(request, exception):
    """
    404 Page not found
    """

    return render(request, 'common/404.html', {})