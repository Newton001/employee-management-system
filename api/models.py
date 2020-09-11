from django.db import models

class Duty(models.Model):
    """Duty model class."""
    code = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=30, blank=False, unique=True)

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    """Employee model class."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duty = models.ForeignKey(Duty, related_name='employees', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
