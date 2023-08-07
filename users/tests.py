from django.test import TestCase

from users.models import Profile
from django.contrib.auth.models import User

admin = User.objects.all().first()
g = Profile.objects.create(user=admin, phone='+79313661220')
g.save()