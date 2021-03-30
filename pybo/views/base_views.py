from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from ..models import Question, Answer
import logging

logger = logging.getLogger('pybo')


def index(request):
    """
            pybo 목록 출력
    """
    logger.info("INFO 레벨로 출력")

    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준
    ca = request.GET.get('ca', 'question')

    if ca == 'class':
        category = 'C'
    elif ca == 'free':
        category = 'F'
    else:
        category = 'Q'

    # 딕셔너리에 넣고 get 으로 가져오기

    if so == 'recommend':
        question_list = Question.objects.filter(category=category).annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.filter(category=category).annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.filter(category=category).order_by('-create_date')

    # question_list = Question.objects.order_by('-create_date')  # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 최근 답변 처리, 최근글 5개

    recent_question = Question.objects.filter().order_by('-create_date')[:5]  # slice 냐 페이지네이터 처리하냐
    recent_answer = Answer.objects.filter().order_by('-create_date')[:5]

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    paginator = Paginator(recent_question, 5)
    page_question = paginator.get_page(1)

    paginator = Paginator(recent_answer, 5)
    page_answer = paginator.get_page(1)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'ca': ca,
               'recent_question': page_question, 'recent_answer': page_answer}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
            pybo 목록 출력
    """
    so = request.GET.get('so', 'recommend')  # 정렬기준
    page = request.GET.get('page', 1)

    question = get_object_or_404(Question, pk=question_id)

    question.update_count

    if so == 'recommend':
        answer_list = Answer.objects.annotate(num_voter=Count('voter')).filter(question_id=question_id).order_by(
            '-num_voter', '-create_date')
    elif so == 'recent':
        answer_list = Answer.objects.filter(question_id=question_id).order_by('-create_date')

    paginator = Paginator(answer_list, 2)
    answer_obj = paginator.get_page(page)

    context = {"question": question, "answer_list": answer_obj, 'page': page, 'so': so}
    return render(request, 'pybo/question_detail.html', context)
