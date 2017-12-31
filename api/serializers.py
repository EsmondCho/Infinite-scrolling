from rest_framework import serializers
from .models import *


class GoodsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    genre2 = serializers.CharField(max_length=20)
    date = serializers.IntegerField()
    start_time = serializers.IntegerField()
    end_time = serializers.IntegerField()
    cate1 = serializers.CharField(max_length=20)
    url = serializers.CharField()
    img = serializers.CharField()
    price = serializers.IntegerField()
    org_price = serializers.IntegerField()
    discount_rate = serializers.FloatField()


    def create(self, validated_data):
        return Goods.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.genre2 = validated_data.get('genre2', instance.genre2)
        instance.date = validated_data.get('date', instance.date)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.cate1 = validated_data.get('cate1', instance.cate1)
        instance.url = validated_data.get('url', instance.url)
        instance.img = validated_data.get('img', instance.img)
        instance.price = validated_data.get('price', instance.price)
        instance.org_price = validated_data.get('org_price', instance.org_price)
        instance.save()
        return instance