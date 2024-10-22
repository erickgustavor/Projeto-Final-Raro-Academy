from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.FileField()
    begin = models.DateField()
    end = models.DateField()

    def __str__(self,):
        return f"#{self.id}|{self.name}"