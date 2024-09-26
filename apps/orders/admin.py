from django.contrib import admin
from background_task.models import Task, CompletedTask
from unfold.admin import ModelAdmin

# Ваши действия для изменения приоритета
def inc_priority(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority += 1
        obj.save()
inc_priority.short_description = "priority += 1"

def dec_priority(modeladmin, request, queryset):
    for obj in queryset:
        obj.priority -= 1
        obj.save()
dec_priority.short_description = "priority -= 1"

# Ваши классы администратора
class TaskAdmin(ModelAdmin):
    display_filter = ['task_name']
    search_fields = ['task_name', 'task_params']
    list_display = ['task_name', 'task_params', 'run_at', 'priority', 'attempts', 'has_error', 'locked_by', 'locked_by_pid_running']
    actions = [inc_priority, dec_priority]

class CompletedTaskAdmin(ModelAdmin):
    display_filter = ['task_name']
    search_fields = ['task_name', 'task_params']
    list_display = ['task_name', 'task_params', 'run_at', 'priority', 'attempts', 'has_error', 'locked_by', 'locked_by_pid_running']

# Функция для безопасной отмены регистрации модели
def unregister_model(admin_site, model):
    try:
        admin_site.unregister(model)
    except admin.sites.NotRegistered:
        pass

# Отменяем регистрацию моделей
unregister_model(admin.site, Task)
unregister_model(admin.site, CompletedTask)

# Регистрируем модели с вашими классами администратора
admin.site.register(Task, TaskAdmin)
admin.site.register(CompletedTask, CompletedTaskAdmin)
