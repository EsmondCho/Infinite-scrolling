from django.contrib import admin
from .models import *


class GoodsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'genre2',
        'cate1',
        'url',
        'img',
        'price',
        'org_price',
    )


class BroadcastingAdmin(admin.ModelAdmin):
    list_diaplay = (
        'goods',
        'date',
        'start_time',
        'end_time',
    )


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'genre2',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'cate1',
    )

admin.site.register(Goods, GoodsAdmin)
admin.site.register(Broadcasting, BroadcastingAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Category, CategoryAdmin)
