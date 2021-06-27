from django.shortcuts import render

# Create your views here.

from .models import *
from .serializers import VisitHistorySerializer, CollectionSerializer, ChapterSerializer, ClassificationSerializer, PlateSerializer
from .filters import VisitHistoryFilter, CollectionFilter, ChapterFilter, ClassificationFilter, PlateFilter

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View

from rest_framework import viewsets, mixins, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
import json


class PanDuan(View):
    def get(self, request):
        type_str = request.GET.get("type")
        url_str = request.GET.get("url")
        if not type_str:
            return HttpResponse(json.dumps({"mess": "未传递类型"}), content_type="application/json")

        if not url_str:
            return HttpResponse(json.dumps({"mess": "错误，未传递URL"}), content_type="application/json")

        if type_str == "xiaosuo":
            xiaosuo = False
            lishi = False
            if VisitHistory.objects.filter(url=url_str):
                lishi = True
            if Chapter.objects.filter(url=url_str):
                xiaosuo = True
            data = {
                "mess": "成功",
                "data": {
                    "xiaosuo": xiaosuo,
                    "lishi": lishi
                }
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"mess": "该类型未开发"}), content_type="application/json")


class ListSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class VisitHistoryViewsSet(viewsets.ModelViewSet):
    queryset = VisitHistory.objects.all()
    serializer_class = VisitHistorySerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = VisitHistoryFilter
    search_fields = ['user__username', 'url']
    ordering_fields = ['user', 'url', 'date_joined', 'update_time']

    # 超级管理员显示全部，其他显示自己的数据
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        else:
            return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionViewsSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = CollectionFilter
    search_fields = ['user__username', 'name', 'authur', 'introduction']
    ordering_fields = ['user', 'name', 'category', 'classification', 'plate', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChapterViewsSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = ChapterFilter
    search_fields = ['user__username', 'name', 'authur', 'introduction', 'content']
    ordering_fields = ['user', 'name', 'category', 'classification', 'plate', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClassificationViewsSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = ClassificationFilter
    search_fields = ['user__username', 'name']
    ordering_fields = ['user', 'name', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlateViewsSet(viewsets.ModelViewSet):
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = PlateFilter
    search_fields = ['user__username', 'name']
    ordering_fields = ['user', 'name', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

