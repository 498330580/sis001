"""sis001_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework import routers

from rest_framework.authtoken import views

from users.views import *
from xiaosuo.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'lishi', VisitHistoryViewsSet)
router.register(r'book', CollectionViewsSet)
router.register(r'zhangjie', ChapterViewsSet)
router.register(r'fenlei', ClassificationViewsSet)
router.register(r'bankuai', PlateViewsSet)
router.register(r'user_url', UserToVisitHistoryViewsSet)
router.register(r'user_coll', CollectionCountViewsSet)
router.register(r'user_zj', ChapterCodeViewsSet)

from xiaosuo.views import PanDuan

urlpatterns = [
    path('admin', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # path('api-token-auth/', views.obtain_auth_token),
    path('panduan', PanDuan.as_view(), name="panduan"),
    path(r'doc/', include_docs_urls(title='API_DOC')),     # api测试接口
    path('api-auth/', include('rest_framework.urls')),
    path(r'login', Login.as_view()),  # drf自带token登录验证
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# handler404 = "accounts.views.page_not_found"
# handler500 = "accounts.views.error"
