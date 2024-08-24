# import django.contrib.sessions.models as s
from django.contrib import admin

import authjs.models as m

admin.site.register(m.User)
admin.site.register(m.Account)
# admin.site.register(m.Session)
# admin.site.register(m.VerificationToken)
# admin.site.register(s.Session)
