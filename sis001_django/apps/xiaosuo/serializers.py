# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import *


class VisitHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitHistory
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = "__all__"


class ClassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classification
        fields = "__all__"


class PlateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plate
        fields = "__all__"


class UserToVisitHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToVisitHistory
        fields = "__all__"


class CollectionCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionCount
        fields = "__all__"
