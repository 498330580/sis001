from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import mail
from django.utils.translation import gettext_lazy as _


# Create your models here.

# 用户注册验证
class UserManager(BaseUserManager):
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not email:
            raise ValueError("请传入邮箱地址！")
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, **kwargs)


# 用户模型
class Users(AbstractBaseUser, PermissionsMixin):  # 继承AbstractBaseUser，PermissionsMixin
    GENDER_TYPE = (
        (0, "男"),
        (2, "女")
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name="用户名",
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(verbose_name="邮箱", blank=True)
    nickname = models.CharField(max_length=15, verbose_name="昵称", null=True, blank=True)
    gender = models.IntegerField(max_length=2, choices=GENDER_TYPE, verbose_name="性别", null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d',
                               default='avatar/default.png',
                               blank=True,
                               null=True,
                               verbose_name='用户头像')
    is_active = models.BooleanField(default=True, verbose_name="激活状态", help_text="用来表示是否允许登陆账号")
    is_staff = models.BooleanField(default=True, verbose_name="是否删除", help_text="标记删除（伪删除）")

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="账号创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['is_superuser', 'is_active', 'is_staff', '-date_joined']
        abstract = True

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        mail.send_mail(subject, message, from_email, [self.email], **kwargs)
