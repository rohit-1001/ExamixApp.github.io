from django.contrib import admin
from .models import user_data
from .models import student
from .models import teacher
from .models import question
from .models import result

# Register your models here.
admin.site.register(user_data)
admin.site.register(student)
admin.site.register(teacher)
admin.site.register(question)
admin.site.register(result)