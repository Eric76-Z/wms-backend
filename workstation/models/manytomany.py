from django.db import models
from workstation.models.parts_models import Parts
from myuser.models import UserProfile



class Part2User(models.Model):
    part = models.ForeignKey(Parts, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    create_time = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (('part', 'user'),)
