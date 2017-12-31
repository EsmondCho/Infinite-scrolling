from django.db import models


class Goods(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    genre2 = models.IntegerField()
    cate1 = models.IntegerField()
    url = models.TextField()
    img = models.TextField()
    price = models.IntegerField()
    org_price = models.IntegerField()

    @property
    def discount_rate(self):
        if self.org_price is not 0:
            return round((self.org_price - self.price)/self.org_price, 3)
        else:
            return 0

class Broadcasting(models.Model):
    goods = models.OneToOneField(Goods)
    date = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()


class Company(models.Model):
    genre2 = models.CharField(max_length=20)


class Category(models.Model):
    cate1 = models.CharField(max_length=10)