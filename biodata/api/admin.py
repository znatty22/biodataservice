from django.contrib import admin
from biodata.api import models as m

# Register your models here.
admin.site.register(m.Study)
admin.site.register(m.Participant)
admin.site.register(m.Biospecimen)
