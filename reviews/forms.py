from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        label = '리뷰 내용을 입력하세요',
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows': 10,
            }
        ),
    )
    class Meta:
        model = Review
        fields = ('content',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label = '댓글 내용을 입력하세요',
        widget = forms.Textarea(
            attrs = {
                'class': 'form-control',
                'rows': 5,
            }
        ),
    )
    class Meta:
        model = Comment
        fields = ('content',)