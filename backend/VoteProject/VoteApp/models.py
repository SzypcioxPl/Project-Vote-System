from django.db import models
from django.contrib.auth.hashers import make_password, check_password  # Import hash functions


class User(models.Model):
    UID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    password = models.CharField(max_length=255)  # hashed
    login = models.CharField(max_length=100, unique=True)

    def set_hash_password(self, raw_password):
        ''' set a hashed password '''
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} {self.surname}"


class Project(models.Model):
    PID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    date_start = models.DateField()
    date_end = models.DateField()
    description = models.TextField()
    vote_scale = models.IntegerField()

    def __str__(self):
        return self.name


class Votes(models.Model):
    VID = models.AutoField(primary_key=True)
    PID = models.ForeignKey(Project, on_delete=models.CASCADE)
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField() 
    vote_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote {self.VID} for Project {self.PID.name}"
