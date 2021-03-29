from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    CATEGORY_CHOICES =(
        ('F', '자유게시판'),
        ('Q', '질문게시판'),
        ('C', '강좌게시판')
    )
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    readcount = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    modify_date = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')  # voter 추가

    # 특정 사용자가 작성한 질문을 얻기 위해 some_user.author_question.all() 추천한 질문은 some_user.voter_question.all()

    def __str__(self):
        return self.subject

    @property
    def update_count(self):
        self.readcount = self.readcount + 1
        self.save()


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_answer')

    def __str__(self):
        return self.content


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
