from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Question, Answer


@login_required(login_url='common:login')
def vote_question(request, question_id):
    """
    pybo 질문 추천 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, "본인 글 추천 불가!!!!!!")
    else:
        question.voter.add(request.user)  # ManyToManyField 는 중복을 허락하지 않는다!
    return redirect('pybo:detail', question_id=question_id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
    pybo 질문 추천 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, "본인 글 추천 불가!!!!!!")
    else:
        answer.voter.add(request.user)  # ManyToManyField 는 중복을 허락하지 않는다!
    return redirect('pybo:detail', question_id=answer.question.id)
