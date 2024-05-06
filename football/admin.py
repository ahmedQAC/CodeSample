from django.contrib import admin
from .models import (Session,
                     Team,
                     Standby,
                     Player)

# Register your models here.
admin.site.register(Session)
admin.site.register(Team)
admin.site.register(Standby)
admin.site.register(Player)