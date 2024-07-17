from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	mobile=models.PositiveIntegerField()
	email=models.EmailField(unique=True)
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_picture=models.ImageField(upload_to='profile_picture/')
	usertype=models.CharField(max_length=100,default="doctor")

	def __str__(self):
		return self.fname+" "+self.lname

class Patient(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	mobile=models.PositiveIntegerField()
	email=models.EmailField(unique=True)
	message=models.TextField()
	doctortype=models.CharField(max_length=100,default="None")

	def __str__(self):
		return self.fname+" "+self.lname