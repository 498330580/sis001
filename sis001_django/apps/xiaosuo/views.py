from django.shortcuts import render

# Create your views here.

from .serializers import *
from .filters import *
from .models import *

# from django.http import HttpResponse
# from django.views.generic.base import View

from rest_framework import viewsets, mixins, permissions, filters, views
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.views import APIView
from rest_framework.response import Response


# from rest_framework import status


class PanDuan(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # 权限

    def get(self, request, format=None):
        type_str = request.GET.get("type")
        url_str = request.GET.get("url")
        if not type_str:
            return Response({"mess": "未传递类型"})

        if not url_str:
            return Response({"mess": "错误，未传递URL"})

        if type_str == "xiaosuo":
            xiaosuo = False
            lishi = False

            if UserToVisitHistory.objects.filter(user=request.user, lishi__url=url_str):
                lishi = True

            # if VisitHistory.objects.filter(url=url_str):
            #     lishi = True

            if CollectionCount.objects.filter(user=request.user, collect=True, collection__chapter__url=url_str):
                xiaosuo = True

            # if Chapter.objects.filter(url=url_str):
            #     xiaosuo = True
            data = {
                "mess": "成功",
                "data": {
                    "xiaosuo": xiaosuo,
                    "lishi": lishi
                }
            }
            return Response(data)
        else:
            return Response({"mess": "该类型未开发"})


class ListSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class VisitHistoryViewsSet(viewsets.ModelViewSet):
    queryset = VisitHistory.objects.all()
    serializer_class = VisitHistorySerializer  # 控制显示字段
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = VisitHistoryFilter  # 控制可以筛选的字段
    search_fields = ['user__username', 'url']
    ordering_fields = ['user', 'url', 'date_joined', 'update_time']

    # 超级管理员显示全部，其他显示自己的数据
    def get_queryset(self):
        if self.request is not None:
            if self.request.user.is_superuser:
                return self.queryset
            else:
                return self.queryset.filter(user=self.request.user)
        return self.queryset.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionViewsSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    # serializer_class = CollectionSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = CollectionFilter
    search_fields = ['user__username', 'name', 'authur', 'introduction']
    ordering_fields = ['user', 'name', 'category', 'classification', 'plate', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return CollectionGetSerializer
        return CollectionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_look_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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


class UserToVisitHistoryViewsSet(viewsets.ModelViewSet):
    queryset = UserToVisitHistory.objects.all()
    serializer_class = UserToVisitHistorySerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = UserToVisitHistoryFilter
    search_fields = ['user__username', 'lishi__url']
    ordering_fields = ['user', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request is not None:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.all()


class CollectionCountViewsSet(viewsets.ModelViewSet):
    queryset = CollectionCount.objects.all()
    # serializer_class = CollectionCountSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = CollectionCountFilter
    search_fields = ['user__username', 'collection__name']
    ordering_fields = ['user', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # print(self.request.method == "GET")
        if self.request is not None:
            return self.queryset.filter(user=self.request.user, collect=True)
        return self.queryset.all()

    def get_serializer_class(self):
        if self.request is not None:
            if self.request.method == "GET":
                return CollectionCountGetSerializer
        return CollectionCountSerializer


class ChapterCodeViewsSet(viewsets.ModelViewSet):
    queryset = ChapterCode.objects.all()
    serializer_class = ChapterCodeSerializer
    pagination_class = ListSetPagination  # 分页器
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]  # 权限
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]  # 过滤器（过滤、搜索、排序）
    filter_class = ChapterCodeFilter
    search_fields = ['user__username', 'chapter__name']
    ordering_fields = ['user', 'chapter', 'date_joined', 'update_time']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # print(self.request.method == "GET")
        if self.request is not None:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.all()

    # def get_serializer_class(self):
    #     if self.request is not None:
    #         if self.request.method == "GET":
    #             return CollectionCountGetSerializer
    #     return CollectionCountSerializer