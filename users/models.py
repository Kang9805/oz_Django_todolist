from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManger(BaseUserManager):
    """
    사용자 모델 생성 관리 커스텀 매니저
    create_user, create_superuser 메서드 정의하여 사용자 생성 방식 제어
    """
    def create_user(self, email, password, *args, **kwargs):
        # 이메일은 필수 입력 필드, 없으면 오류 발생
        if not email:
            raise ValueError('Users must have an email address')
        # user 모델 인스턴스 생성
        user = self.create(email=email, *args, **kwargs)
        # 비밀번호 해시 처리하여 저장
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, *args, **kwargs):
        # create_user 메서드를 호출하여 기본 사용자 객체 생성
        user = self.create_user(email, password, *args, **kwargs)
        # 관리자 권한 부여
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    django 기본 user 모델을 대체하는 사용자 정의 모델
    이메일을 사용자 이름으로 사용하도록 설정
    """
    name = models.CharField(max_length=100)
    # 이메일을 고유한 값으로 설정, 로그인 필드로 사용
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # 사용자 정의 매니저를 이 모델의 objects로 지정
    objects = UserManger()

    # 로그인에 사용할 필드 = email
    USERNAME_FIELD = 'email'
    # 이메일 관련 필드 = email
    EMAIL_FIELD = 'email'

    def __str__(self):
        # Django의 내부 시스템 호환성을 위해 name 필드를 username 속성으로 제공
        return self.name

    @property
    def username(self):
        return self.name
