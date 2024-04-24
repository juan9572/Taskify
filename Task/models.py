from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)

    title = models.CharField(max_length=200,
                             unique=True)

    description = models.TextField(blank=True, max_length=500)

    complete = models.BooleanField(default=False)

    create = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['complete']
