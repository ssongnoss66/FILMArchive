from django import forms
from .models import Movie, MoviePeople

class MovieForm(forms.ModelForm):
    title = forms.CharField(
        label = '영화 제목',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '영화 제목을 입력하세요',
            }
        )
    )
    original_title = forms.CharField(
        label = '영화 원제',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '영화 원제를 입력하세요',
            }
        )
    )
    poster = forms.ImageField(
        label = '포스터',
        widget = forms.ClearableFileInput(
            attrs = {
                'class': 'form-control',
                'multiple': True,
            },
        ),
        required = False,
    )
    release_date = forms.DateField(
        label = '개봉일',
        widget = forms.DateInput(
            attrs = {
                'type': 'date'
            }
        ),
    )
    genre = forms.CharField(
        label = '영화 장르',
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
            },
        choices = [
            ("드라마", "드라마"),
            ("판타지", "판타지"),
            ("서부", "서부"),
            ("공포", "공포"),
            ("로맨스", "로맨스"),
            ("모험", "모험"),
            ("스릴러", "스릴러"),
            ("느와르", "느와르"),
            ("컬트", "컬트"),
            ("다큐멘터리", "다큐멘터리"),
            ("코미디", "코미디"),
            ("가족", "가족"),
            ("미스터리", "미스터리"),
            ("전쟁", "전쟁"),
            ("애니메이션", "애니메이션"),
            ("범죄", "범죄"),
            ("뮤지컬", "뮤지컬"),
            ("SF", "SF"),
            ("액션", "액션"),
            ("무협", "무협"),
            ("에로", "에로"),
            ("서스펜스", "서스펜스"),
            ("서사", "서사"),
            ("블랙코미디", "블랙코미디"),
            ("실험", "실험"),
            ("영화카툰", "영화카툰"),
            ("영화음악", "영화음악"),
            ("영화패러디포스터", "영화패러디포스터"),
        ]
        ),
    )
    country = forms.CharField(
        label = '영화 국가',
        widget = forms.Select(
            attrs = {
                'class': 'form-control',
            },
        choices = [
            ("프랑스", "프랑스"),
            ("영국", "영국"),
            ("홍콩", "홍콩"),
            ("일본", "일본"),
            ("한국", "한국"),
            ("미국", "미국"),
            ("기타", "기타"),
        ]
        ),
    )
    running_time  = forms.CharField(
        label = '러닝 타임',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '러닝 타임을 입력하세요',
            }
        )
    )
    age = forms.CharField(
        label = '연령',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '연령을 입력하세요',
            }
        )
    )
    class Meta:
        model = Movie
        fields = ('title', 'original_title', 'release_date', 'genre', 'country', 'running_time', 'age', 'poster')

class MoviePeopleForm(forms.ModelForm):
    person_name = forms.CharField(
        label = '이름',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '이름을 입력하세요',
            }
        )
    )
    part = forms.CharField(
        label = '역할',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '역할을 입력하세요',
            }
        )
    )
    character_name = forms.CharField(
        label = '캐릭터명',
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder' : '캐릭터명을 입력하세요',
            }
        ),
        required=False,
    )
    person_photo = forms.ImageField(
        label = '프로필 사진',
        widget = forms.ClearableFileInput(
            attrs = {
                'class': 'form-control',
                'multiple': True,
            },
        ),
        required = False,
    )
    class Meta:
        model = MoviePeople
        fields = ('person_name', 'part', 'character_name', 'person_photo')