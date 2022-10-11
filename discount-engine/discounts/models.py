import uuid
from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Discount(models.Model):
    DISCOUNT_TYPES = (
        ('percent', 'Percent off'),
        ('fixed', 'Dollars off'),
        ('bogo', 'Buy one get one'),
    )
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=10)
    active = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    usage_max = models.IntegerField(default=0)
    usage_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def is_valid(self):
        #Check if dates are valid and usage max
        if self.active == True and self.start_date <= date.today() and self.end_date >= date.today() and (self.usage_max == 0 or self.usage_count < self.usage_max):
            return True
        return False


class Percent(Discount):
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def save(self, *args, **kwargs):
        self.type = 'percent'
        super().save(*args, **kwargs)

    def apply(self, cart):
        if self.is_valid:
            discount_total = round((float(cart['subtotal']) * float(self.value/100)), 2)
            if self.usage_max:
                self.usage_count += 1
                self.save()
            return discount_total
        return 0


class Fixed(Discount):
    value = models.IntegerField()

    def save(self, *args, **kwargs):
        self.type = 'fixed'
        super().save(*args, **kwargs)

    def apply(self, cart):
        if self.is_valid:
            discount_total = self.value
            if self.usage_max:
                self.usage_count += 1
                self.save()
            return discount_total
        return 0


class Product(Discount):
    bo = models.CharField(max_length=10)
    go = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.type = 'product'
        super().save(*args, **kwargs)

    def apply(self, cart):
        if self.is_valid:
            product_ids = [item['id'] for item in cart['products']]
            if self.bo in product_ids and self.go in product_ids:
                discount_total = [item for item in cart['products'] if item['id'] == self.go][0]['price']
                if self.usage_max:
                    self.usage_count += 1
                    self.save()
                return discount_total
        return 0
