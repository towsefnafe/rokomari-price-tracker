from django.db import models

# Create your models here.
class Book(models.Model):
	link = models.CharField(max_length=300)

	def __str__(self):
		return self.link