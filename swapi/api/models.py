from django.db import models


class People(models.Model):
    HAIR_COLOR_CHOICES = (
        ('blond', 'Blond'),
        ('black', 'Black'),
        ('brown', 'Brown'),
        ('red', 'Red'),
    )
    name = models.CharField(max_length=255)
    height = models.IntegerField(null=True, blank=True)
    mass = models.IntegerField(null=True, blank=True)
    hair_color = models.CharField(
        max_length=10, choices=HAIR_COLOR_CHOICES, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
