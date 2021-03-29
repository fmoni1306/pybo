from django import forms
from pybo.models import Question, Answer, Comment


# 이같은 클래스를 장고폼이라고 한다.
# forms.Form 을 상속받으면 폼, forms.ModelForm 을 상속받으면 모델 폼이라 부른다.
class QuestionForm(forms.ModelForm):  # 파라미터가아니라 () 안에 상속이다.

    class Meta:
        model = Question  # Question 모델과 연결되어 있으며
        fields = ['subject', 'content', 'category']  # 필드로 subject, content 를 사용한다고 정의했다.
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})  # required id 는 어느코드에서 채워주는걸까? // a: 템플릿에서 해줬음
        # }
        labels = {
            'subject': '제목',
            'content': '내용'
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
