from django.urls import path
from . import views


app_name = 'django_ui'


urlpatterns = [
    path("data", views.DataView.as_view(), name="data_page"),
    path("data/parsing_tasks_competed_table_json", views.parsing_tasks_competed_table_json, name="parsing_tasks_competed_table_json"),

    path("mapping", views.MappingView.as_view(), name="mapping_page"),
    path("mapping/mapping_tasks_competed_table_json", views.mapping_tasks_competed_table_json, name="mapping_tasks_competed_table_json"),
    path("mapping/schedule_form", views.MappingScheduleFormView.as_view(), name="mapping_schedule_form"),
    path("mapping/scheduled_tasks_table_json", views.mapping_scheduled_tasks_table_json, name="mapping_scheduled_tasks_table_json"),


    path("report", views.ReportView.as_view(), name="report_page"),
    path("report/report_tasks_competed_table_json", views.report_tasks_competed_table_json, name="report_tasks_competed_table_json"),
]
