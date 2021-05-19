from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    email = models.EmailField(verbose_name='Логин')
    password = models.CharField(max_length=150, verbose_name='Пароль')

    class Meta:
        ordering = ['-name']


class Search(models.Model):
    url = models.URLField(verbose_name='Ссылка для парсинга')
    pages = models.PositiveIntegerField(default=1)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class Product(models.Model):
    search = models.ForeignKey(to=Search, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Заголовок', db_index=True)
    description = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    name_seller = models.CharField(max_length=100, verbose_name='Имя продавца')
    phone_number = PhoneNumberField(verbose_name='Номер продавца')
    image = models.ImageField()
    url = models.URLField(verbose_name='Ссылка на объявление')

    def __str__(self):
        return f'{self.title} - {self.name_seller} - {self.phone_number}'

    def get_absolute_url(self):
        return reverse('product_list', kwargs={'slug': self.url})

    class Meta:
        ordering = ['-title']
