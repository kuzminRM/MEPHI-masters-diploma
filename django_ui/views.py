from django.http import JsonResponse
from django.views.generic import TemplateView


class DataView(TemplateView):
    template_name = "data_page.html"


class MappingView(TemplateView):
    template_name = "mapping_page.html"


class ReportView(TemplateView):
    template_name = "report_page.html"


def parsing_tasks_competed_table_json(request):
    data = [
            {"id": 4, "source": "Петрович", "state": "Выполняется", "status": "-", "count": "1589", "timestamp": "2025-03-18 12:01:44", "initiator": "Кузьмин РМ"},
            {"id": 3, "source": "OBI", "state": "Завершена", "status": "Успешно", "count": "45571", "timestamp": "2025-03-17 21:15:58", "initiator": "Кузьмин РМ"},
            {"id": 2, "source": "Строительный двор", "state": "Завершена", "status": "Успешно", "count": "14103", "timestamp": "2025-03-17 21:15:02", "initiator": "Кузьмин РМ"},
            {"id": 1, "source": "Строительный двор", "state": "Завершена", "status": "Ошибка", "count": "0", "timestamp": "2025-03-17 20:44:30", "initiator": "Кузьмин РМ"},
        ]

    return JsonResponse(data, safe=False)


def mapping_tasks_competed_table_json(request):
    data = [
            {"id": 8, "source": "Строительный двор - Петрович", "state": "Выполняется", "status": "-", "duration": "~01:44", "hadmatch": "-", "timestamp": "2025-03-19 19:00:19", "initiator": "Кузьмин РМ"},
            {"id": 7, "source": "Строительный двор - OBI", "state": "Выполняется", "status": "-", "duration": "~02:10", "hadmatch": "-", "timestamp": "2025-03-19 19:00:19", "initiator": "Кузьмин РМ"},
            {"id": 6, "source": "Строительный двор - Петрович", "state": "Завершена", "status": "Успешно", "duration": "01:44", "hadmatch": "58", "timestamp": "2025-03-19 14:58:19", "initiator": "Кузьмин РМ"},
            {"id": 5, "source": "Строительный двор - OBI", "state": "Завершена", "status": "Успешно", "duration": "02:10", "hadmatch": "44", "timestamp": "2025-03-19 14:58:19", "initiator": "Кузьмин РМ"},
            {"id": 4, "source": "Строительный двор - Петрович", "state": "Завершена", "status": "Ошибка", "duration": "00:00", "hadmatch": "-", "timestamp": "2025-03-19 14:44:05", "initiator": "Кузьмин РМ"},
            {"id": 3, "source": "Строительный двор - OBI", "state": "Завершена", "status": "Ошибка", "duration": "00:00", "hadmatch": "-", "timestamp": "2025-03-19 14:44:05", "initiator": "Кузьмин РМ"},
            {"id": 2, "source": "Строительный двор - Петрович", "state": "Завершена", "status": "Ошибка", "duration": "00:00", "hadmatch": "-", "timestamp": "2025-03-19 10:00:11", "initiator": "Кузьмин РМ"},
            {"id": 1, "source": "Строительный двор - OBI", "state": "Завершена", "status": "Ошибка", "duration": "00:00", "hadmatch": "-", "timestamp": "2025-03-19 10:00:11", "initiator": "Кузьмин РМ"},
        ]

    return JsonResponse(data, safe=False)


def report_tasks_competed_table_json(request):
    data = [
            {"id": 3, "name": "Средние отклонения", "state": "Завершена", "status": "Успешно", "file_type": "pdf", "info": "Строительный двор - OBI (7)", "timestamp": "2025-03-31 15:44:14", "initiator": "Кузьмин РМ"},
            {"id": 2, "name": "Средние отклонения", "state": "Завершена", "status": "Успешно", "file_type": "pdf", "info": "Строительный двор - Петрович (8)", "timestamp": "2025-03-31 15:41:21", "initiator": "Кузьмин РМ"},
            {"id": 1, "name": "Тест", "state": "Завершена", "status": "Успешно", "file_type": "csv", "info": "Test", "timestamp": "2025-03-30 18:12:07", "initiator": "admin"},
        ]

    return JsonResponse(data, safe=False)