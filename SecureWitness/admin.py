from django.contrib import admin

# Register your models here.
from django.contrib import admin
from SecureWitness.models import report
from SecureWitness.models import user, group

admin.site.register(report)
admin.site.register(user)
admin.site.register(group)