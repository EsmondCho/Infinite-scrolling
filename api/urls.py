from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^date/(?P<date>[0-9]+)/schedule$', GoodsList.as_view()),
    url(r'^goods/(?P<gid>[0-9]+)$', GoodsDetail.as_view()),

]