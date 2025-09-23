from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms

# settings.py에서 AUTH_USER_MODEL로 지정된 User 모델을 가져온다.
User = get_user_model()


class SignupForm(UserCreationForm):
    # UserCreationForm을 상속받아 사용자 정의 회원가입 폼을 생성
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 비밀번호 필드에 대한 커스텀 설정을 적용
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            if field == 'password1':
                # 비밀번호 필드의 라벨을 '비밀번호'로 변경
                self.fields[field].label = '비밀번호'
                # 부트스트랩 스타일을 위한 CSS 클래스 추가
                self.fields[field].widget.attrs['class'] = 'form-control'
                # 입력창에 힌트를 제공하는 placeholder 추가
                self.fields[field].widget.attrs['placeholder'] = '비밀번호를 입력해주세요.'
            if field == 'password2':
                # 비밀번호 확인 필드 설정
                self.fields[field].label = '비밀번호 확인'
                self.fields[field].widget.attrs['class'] = 'form-control'
                self.fields[field].widget.attrs['placeholder'] = '비밀번호를 다시 입력해주세요.'

    class Meta(UserCreationForm.Meta):
        # 폼이 사용할 모델을 User로 지정
        model = User
        # 폼에 표시할 필드를 지정
        fields = ('name', 'email', 'password1', 'password2')
        # 필드 라벨을 한글로 설정
        labels = {
            'name': '이름',
            'email': '이메일',
        }
        # 필드에 HTML 위젯을 적용하고 속성(attrs)을 추가
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '이름을 입력해주세요.', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@example.com.', 'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    # AuthenticationForm을 상속받아 사용자 정의 로그인 폼 생성
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # username 필드의 라벨과 위젯을 '이메일'에 맞게 수정
        self.fields['username'].label = '이메일'
        self.fields['password'].label = '비밀번호'
        # CSS 클래스와 placeholder 추가
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = '이메일을 입력해주세요.'
        self.fields['password'].widget.attrs['placeholder'] = '비밀번호를 입력해주세요.'