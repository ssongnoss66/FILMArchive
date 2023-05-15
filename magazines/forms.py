from .models import Magazine, MagazineMovie
from movies.models import Movie
from django import forms

class MagazineForm(forms.ModelForm):
    mgzn_title = forms.CharField(
        label = '잡지명',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '잡지명을 입력하세요',
            }
        )
    )
    cover = forms.ImageField(
        label = '잡지커버',
        widget = forms.ClearableFileInput(
            attrs = {
                'class': 'form-control',
                'multiple': True,
            },
        ),
        required = False,
    )
    publish_date = forms.DateField(
        label = '발행일',
        widget = forms.DateInput(
            attrs = {
                'class': 'form-control',
                'type': 'date'
            }
        ),
    )
    official = forms.URLField(
        label = '공식 사이트',
        required = False,
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    where_to_buy = forms.URLField(
        label = '구매처',
        required = False,
        widget = forms.URLInput(
            attrs = {
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model = Magazine
        fields = ('mgzn_title', 'cover', 'publish_date','official', 'where_to_buy')

class MagazineMovieForm(forms.ModelForm):
    movie = forms.ModelChoiceField(
        queryset=Movie.objects.all(),
        to_field_name='title'
    )
    class Meta:
        model = MagazineMovie
        fields = ('movie',)