from django.urls import path
from service_history.views import schedule_listing, schedule_detail, schedule_add, schedule_edit, schedule_delete

urlpatterns = [
    path('schedules', schedule_listing),
    path('schedules/<int:id>', schedule_detail),
    path('schedule/add', schedule_add),
    path('schedules/<int:id>/edit', schedule_edit),
    path('schedules/<int:id>/delete', schedule_delete)
]

