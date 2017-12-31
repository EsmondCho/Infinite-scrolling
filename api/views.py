import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GoodsSerializer
from .models import *
# from ratelimit.mixins import RatelimitMixin
from django.http import HttpResponse

from django.core.cache import cache

class GoodsList(APIView):

    _GENRE2_NAME_DIC = {
        1:'cjmall', 2:'gsshop',
        3:'lottemall', 4:'hmall'
    }

    _CATE1_NAME_DIC = {
        1:'생활·주방', 2:'가전·디지털',
        3:'화장품·미용', 4:'패션·잡화',
        5:'유아·아동', 6:'여행·레저',
        7:'식품·건강', 8:'보험',
        0:''
    }

    def get(self, request, date, format=None):

        # url parameters
        query_dict = request.GET

        # checking parameters correct
        if "tz" and "companys" and "cates" in query_dict:
            tz = int(query_dict['tz'])
            hour_after = tz*400
            hour_before = (tz+1)*400-1

            if query_dict['companys'] and query_dict['cates']:
                # querying data of Broadcasting joined with Goods objects
                brc_list = Broadcasting.objects.select_related("goods") \
                    .filter(date=date) \
                    .filter(start_time__gte=hour_after) \
                    .filter(start_time__lte=hour_before) \
                    .filter(goods__genre2__in=query_dict['companys'].split(',')) \
                    .filter(goods__cate1__in=query_dict['cates'].split(','))

            elif query_dict['companys']:
                # querying data of Broadcasting joined with Goods objects
                brc_list = Broadcasting.objects.select_related("goods") \
                    .filter(date=date) \
                    .filter(start_time__gte=hour_after) \
                    .filter(start_time__lte=hour_before) \
                    .filter(goods__genre2__in=query_dict['companys'].split(','))

            elif query_dict['cates']:
                # querying data of Broadcasting joined with Goods objects
                brc_list = Broadcasting.objects.select_related("goods") \
                    .filter(date=date) \
                    .filter(start_time__gte=hour_after) \
                    .filter(start_time__lte=hour_before) \
                    .filter(goods__genre2__in=query_dict['cates'].split(','))

            else:
                # querying data of Broadcasting joined with Goods objects
                brc_list = Broadcasting.objects.select_related("goods") \
                    .filter(date=date) \
                    .filter(start_time__gte=hour_after) \
                    .filter(start_time__lte=hour_before)

        elif "tz" in query_dict:
            tz = int(query_dict['tz'])
            hour_after = tz*400
            hour_before = (tz+1)*400-1

            # querying data of Broadcasting joined with Goods objects
            brc_list = Broadcasting.objects.select_related("goods")\
                .filter(date=date)\
                .filter(start_time__gte=hour_after)\
                .filter(start_time__lte=hour_before)\

        elif not query_dict:

            # querying data of Broadcasting joined with Goods objects
            brc_list = Broadcasting.objects.select_related("goods")\
                .filter(date=date)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


        response_data = []

        ex_tz = -1
        temp_brc = {}

        for brc in brc_list:
            date = brc.date
            tz = brc.start_time // 400  # tz: 0, 1, 2, 3, 4, 5
            goods = brc.goods

            broadcasting = {}
            broadcasting['start_time'] = brc.start_time
            broadcasting['end_time'] = brc.end_time
            broadcasting['name'] = goods.name
            broadcasting['genre2'] = self._GENRE2_NAME_DIC[goods.genre2]
            broadcasting['cate1'] = self._CATE1_NAME_DIC[goods.cate1]
            broadcasting['url'] = goods.url
            broadcasting['img'] = goods.img
            broadcasting['price'] = goods.price
            broadcasting['org_price'] = goods.org_price
            broadcasting['discount_rate'] = goods.discount_rate
            broadcasting['gid'] = goods.id


            # first iteration of new tz
            if ex_tz == -1:

                dic = {}
                dic['date'] = date
                dic['tz'] = tz

                broadcasting_list = []

                if temp_brc:
                    temp_broadcasting = {}
                    temp_broadcasting['start_time'] = temp_brc.start_time
                    temp_broadcasting['end_time'] = temp_brc.end_time
                    temp_broadcasting['name'] = temp_brc.goods.name
                    temp_broadcasting['genre2'] = self._GENRE2_NAME_DIC[temp_brc.goods.genre2]
                    temp_broadcasting['cate1'] = self._CATE1_NAME_DIC[temp_brc.goods.cate1]
                    temp_broadcasting['url'] = temp_brc.goods.url
                    temp_broadcasting['img'] = temp_brc.goods.img
                    temp_broadcasting['price'] = temp_brc.goods.price
                    temp_broadcasting['org_price'] = temp_brc.goods.org_price
                    temp_broadcasting['discount_rate'] = temp_brc.goods.discount_rate
                    temp_broadcasting['gid'] = temp_brc.goods.id

                    broadcasting_list.append(temp_broadcasting.copy())
                    temp_brc = {}

                broadcasting_list.append(broadcasting.copy())

                ex_tz = tz

            elif ex_tz == tz:
                broadcasting_list.append(broadcasting.copy())
                ex_tz = tz

            # when tz changed
            elif ex_tz != tz:
                dic['broadcasting_list'] = broadcasting_list
                response_data.append(dic.copy())

                ex_tz = -1
                temp_brc = brc

        # append item_list to last dictionary
        if ex_tz != -1:
            dic['broadcasting_list'] = broadcasting_list
            response_data.append(dic.copy())
            ex_tz = -1


        for data in response_data:
            broadcasting_list = data['broadcasting_list']

            new_broadcasting_list = []

            ex_genre2 = ""
            ex_start_time = -1
            ex_end_time = -1
            temp_broadcasting = {}

            for broadcasting in broadcasting_list:

                item = {}
                item['name'] = broadcasting['name']
                item['cate1'] = broadcasting['cate1']
                item['price'] = broadcasting['price']
                item['org_price'] = broadcasting['org_price']
                item['img'] = broadcasting['img']
                item['url'] = broadcasting['url']
                item['discount_rate'] = broadcasting['discount_rate']
                item['gid'] = broadcasting['gid']

                if ex_genre2 == "":
                    new_broadcasting = {}
                    new_broadcasting['genre2'] = broadcasting['genre2']
                    new_broadcasting['start_time'] = broadcasting['start_time']
                    new_broadcasting['end_time'] = broadcasting['end_time']

                    item_list = []

                    if temp_broadcasting:
                        temp_item = {}
                        temp_item['name'] = temp_broadcasting['name']
                        temp_item['cate1'] = temp_broadcasting['cate1']
                        temp_item['price'] = temp_broadcasting['price']
                        temp_item['org_price'] = temp_broadcasting['org_price']
                        temp_item['img'] = temp_broadcasting['img']
                        temp_item['url'] = temp_broadcasting['url']
                        temp_item['discount_rate'] = temp_broadcasting['discount_rate']
                        temp_item['gid'] = temp_broadcasting['gid']

                        item_list.append(temp_item.copy())
                        temp_broadcasting = {}

                    item_list.append(item.copy())

                    ex_genre2 = broadcasting['genre2']
                    ex_start_time = broadcasting['start_time']
                    ex_end_time = broadcasting['end_time']

                elif ex_genre2 == broadcasting['genre2'] \
                        and ex_start_time == broadcasting['start_time'] \
                        and ex_end_time == broadcasting['end_time']:

                    item_list.append(item.copy())

                    ex_genre2 = broadcasting['genre2']
                    ex_start_time = broadcasting['start_time']
                    ex_end_time = broadcasting['end_time']

                elif ex_genre2 != broadcasting['genre2'] \
                        or ex_start_time != broadcasting['start_time'] \
                        or ex_end_time != broadcasting['end_time']:

                    new_broadcasting['item_list'] = item_list
                    new_broadcasting_list.append(new_broadcasting.copy())

                    ex_genre2 = ""
                    ex_start_time = -1
                    ex_end_time = -1

                    temp_broadcasting = broadcasting

            if ex_genre2 != "":
                new_broadcasting['item_list'] = item_list
                new_broadcasting_list.append(new_broadcasting.copy())

            data['broadcasting_list'] = new_broadcasting_list

        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)


class GoodsDetail(APIView):

    # get Goods object
    def get_object(self, gid):
        try:
            return Goods.objects.get(id=gid)
        except Goods.DoesNotExist:
            raise Http404

    def get(self, request, gid, format=None):
        goods = self.get_object(gid)
        serializer = GoodsSerializer(goods)
        return Response(serializer.data)

