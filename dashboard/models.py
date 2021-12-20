from django.db import models
from django.contrib.auth.models import User




class Uploads(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=50,blank=True,null=True)
	file = models.FileField(upload_to='files')
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.title}'


