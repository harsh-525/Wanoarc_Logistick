from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# question = Fquestion.objects.create(question_one="What is your first name?", answer_one="John", question_two="What is your last name?", answer_Two="Doe", username="harsha1", password="vardhan1234")
# question.set_password('vardhan1234')
# from logistick.models import Fquestion
class Fquestion(User):
    question_one = models.CharField(max_length=200, blank=False)
    answer_one = models.CharField(max_length=50, blank=False)
    question_two = models.CharField(max_length=200, blank=False)
    answer_two = models.CharField(max_length=50, blank=False)
    is_vendor = models.BooleanField(default=True)

    class Meta:
        verbose_name = ("F_user_detail")


class Stock(models.Model):
    v_id = models.ForeignKey(Fquestion, related_name='stock_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    by = models.CharField(max_length=50, default="test", blank=False)
    description = models.TextField(max_length=500, default="")
    details = models.TextField(max_length=1000, default="")
    quantity = models.PositiveIntegerField(blank=False)
    price = models.DecimalField(blank=False, decimal_places=2, max_digits=10)
    last_updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    c_id = models.ForeignKey(Fquestion, related_name='user_id', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.c_id.first_name + ' ordered on ' + str(self.date)


class OrderDetail(models.Model):
    order_id = models.ForeignKey(Order, related_name='orderid_relation', on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stock, related_name='ordered_item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False)
    price = models.DecimalField(blank=False, decimal_places=2, max_digits=10)


class Bag(models.Model):
    stock_id = models.ForeignKey(Stock, related_name='stock_id', on_delete=models.CASCADE)
    c_id = models.ForeignKey(Fquestion, related_name='stock_user', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

