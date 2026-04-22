from django.contrib import admin

from presencial.models import PresencialSession

from presencial.models import Booking

# Register your models here.
admin.site.register(PresencialSession)
admin.site.register(Booking)