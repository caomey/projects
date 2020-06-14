from django.db import models

# Create your models here.


class AsinInfo(models.Model):
    asin = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=250, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    merchant = models.CharField(max_length=20, blank=True, null=True)
    sellers = models.CharField(max_length=5, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    review = models.CharField(max_length=10, blank=True, null=True)
    star = models.CharField(max_length=10, blank=True, null=True)
    delivery = models.CharField(max_length=32, blank=True, null=True)
    build_time = models.CharField(max_length=32, blank=True, null=True)
    update_time = models.CharField(max_length=32, blank=True, null=True)
    collection = models.CharField(max_length=1, blank=True, null=True)
    alibaba_link = models.CharField(max_length=200, blank=True, null=True)
    monitor = models.CharField(max_length=32, blank=True, null=True)
    readinfo = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asin_info'


class GmMonitor(models.Model):
    asin = models.CharField(max_length=15, blank=True, null=True)
    update_time = models.CharField(primary_key=True, max_length=20)
    brand = models.CharField(max_length=30, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    img = models.CharField(max_length=200, blank=True, null=True)
    ranks = models.CharField(max_length=20, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    seller = models.CharField(max_length=20, blank=True, null=True)
    price1 = models.CharField(max_length=20, blank=True, null=True)
    seller1 = models.CharField(max_length=20, blank=True, null=True)
    registered = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gm_monitor'

    # def __str__(self):
    #     return self.asin


class MonitorAsin(models.Model):
    asin = models.CharField(primary_key=True, max_length=32)
    update_time = models.CharField(max_length=32, blank=True, null=True)
    alibaba_link = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitor_asin'