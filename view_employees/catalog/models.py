from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from enum import Enum


class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f'{self.name}'


class Employee(models.Model):
    class STATUS(Enum):
        ADMIN = ('admin', 'Administrator')
        BACKEND = ('backend', 'back-end dev')
        FRONTEND = ('frontend', 'Front-end dev')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    first_name = models.CharField(max_length=32)
    second_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=120, null=True, blank=True)
    phone_number = PhoneNumberField()
    start_date = models.DateField()
    stop_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=32, choices=[x.value for x in STATUS], default=STATUS.get_value('ADMIN'))
    departament = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.second_name}. {self.start_date}. {self.role}'

    class Meta:
        ordering = ["last_name"]
