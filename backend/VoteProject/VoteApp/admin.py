from django.contrib import admin
from .models import User, Project, Votes


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('UID', 'name', 'surname', 'role', 'login') 
    search_fields = ('name', 'surname', 'login')  
    list_filter = ('role',)  


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('PID', 'name', 'date_start', 'date_end', 'vote_scale')
    search_fields = ('name',)
    list_filter = ('date_start', 'date_end')


@admin.register(Votes)
class VotesAdmin(admin.ModelAdmin):
    list_display = ('VID', 'PID', 'UID', 'value', 'vote_timestamp')
    search_fields = ('project__name', 'user__name')  
    list_filter = ('vote_timestamp',)
