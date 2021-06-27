# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
from rest_framework import filters
# from django.db.models import Q
# from rest_framework.response import Response

from .models import *


class VisitHistoryFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = VisitHistory
        fields = ['user', 'url']


class CollectionFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Collection
        fields = ['category', 'name', 'classification', 'plate', 'category']


class ChapterFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Chapter
        fields = ['name', 'url', 'classification', 'plate', 'category', 'crawling_status']


class ClassificationFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Classification
        fields = ['user__username', 'name']


class PlateFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Plate
        fields = ['user__username', 'name']