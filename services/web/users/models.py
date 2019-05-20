from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)

    @property
    def fullname(self):
        return self.fname + ' ' + self.lname

    def calculate_age(self):
        today = date.today()

        try:
            birthday = self.dob.replace(year=today.year)
            # raised when birth date is February 29 and the current year is not a leap year
        except ValueError:
            birthday = self.dob.replace(year=today.year, day=born.day-1)

        if birthday > today:
            return today.year - self.dob.year - 1
        else:
            return today.year - self.dob.year

    def __str__(self):
        return "{} - {}".format(self.username, self.email, self.dob, self.calculate_age)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
