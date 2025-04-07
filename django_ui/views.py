from django.http import JsonResponse
from django.views.generic import TemplateView

import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased
from db_populate.session import db_session_as_kwarg
from db_populate.models import Match as SaMatch
from db_populate.models import Product as SaProduct


class DataView(TemplateView):
    template_name = "data_page.html"


class MappingView(TemplateView):
    template_name = "mapping_page.html"


class MappingScheduleFormView(TemplateView):
    template_name = "mapping_schedule_form.html"


class ReportView(TemplateView):
    template_name = "report_page.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        kwargs["html_plot"] = self.get_plot()

        return kwargs

    def get_plot(self) -> str:
        rows = self.get_products_prices()

        real_df = pd.DataFrame(rows, columns=["title", "price_1", "price_2"])
        real_df["delta"] = real_df["price_1"] - real_df["price_2"]
        real_df["relative_delta"] = real_df["delta"] / real_df["price_2"]

        fig = go.Figure()

        fig.add_trace(go.Histogram(
            x=real_df["relative_delta"],
            name="В OBI дешевле",
            opacity=1,
            marker_color="#E45756",
            xbins=dict(start=0, end=0.9, size=0.1)
        ))
        fig.add_trace(go.Histogram(
            x=real_df["relative_delta"],
            name="В Строительный двор дешевле",
            opacity=1,
            marker_color="#54A24B",
            xbins=dict(start=-0.9, end=0, size=0.1)
        ))

        fig.update_layout(
            title='Гистограмма распределения разницы цен Строительный двор - OBI',
            xaxis_title='Относительная разница стоимости',
            yaxis_title='Кол-во',
            bargap=0.1,
        )

        return plotly.offline.plot(fig, auto_open=False, output_type='div')

    @db_session_as_kwarg
    def get_products_prices(self, session: Session) -> list[list]:
        p1_alias = aliased(SaProduct)
        p2_alias = aliased(SaProduct)

        query = session.execute(
            select(p1_alias.title, p1_alias.price, p2_alias.price).select_from(SaMatch)
            .join(p1_alias, SaMatch.product_1_id == p1_alias.id)
            .join(p2_alias, SaMatch.product_2_id == p2_alias.id)
        )

        rows = []
        for sa_row in query.all():
            r = sa_row
            rows.append([
                sa_row[0],
                sa_row[1],
                sa_row[2],
            ])

        return rows


def parsing_tasks_competed_table_json(request):
    data = [
        {"id": 4, "source": "Петрович", "state": "Выполняется", "status": "-", "count": "1589",
         "timestamp": "2025-03-18 12:01:44", "initiator": "Кузьмин РМ"},
        {"id": 3, "source": "OBI", "state": "Завершена", "status": "Успешно", "count": "45571",
         "timestamp": "2025-03-17 21:15:58", "initiator": "Кузьмин РМ"},
        {"id": 2, "source": "Строительный двор", "state": "Завершена", "status": "Успешно", "count": "14103",
         "timestamp": "2025-03-17 21:15:02", "initiator": "Кузьмин РМ"},
        {"id": 1, "source": "Строительный двор", "state": "Завершена", "status": "Ошибка", "count": "0",
         "timestamp": "2025-03-17 20:44:30", "initiator": "Кузьмин РМ"},
    ]

    return JsonResponse(data, safe=False)


def mapping_tasks_competed_table_json(request):
    data = [
        {"id": 8, "source": "Строительный двор - Петрович", "state": "Выполняется", "status": "-", "duration": "~01:44",
         "hadmatch": "-", "timestamp": "2025-03-19 19:00:19", "initiator": "Кузьмин РМ"},
        {"id": 7, "source": "Строительный двор - OBI", "state": "Выполняется", "status": "-", "duration": "~02:10",
         "hadmatch": "-", "timestamp": "2025-03-19 19:00:19", "initiator": "Кузьмин РМ"},
        {"id": 6, "source": "Строительный двор - Петрович", "state": "Завершена", "status": "Успешно",
         "duration": "01:44", "hadmatch": "58", "timestamp": "2025-03-19 14:58:19", "initiator": "Кузьмин РМ"},
        {"id": 5, "source": "Строительный двор - OBI", "state": "Завершена", "status": "Успешно", "duration": "02:10",
         "hadmatch": "44", "timestamp": "2025-03-19 14:58:19", "initiator": "Кузьмин РМ"},
        {"id": 4, "source": "Строительный двор - Петрович", "state": "Завершена", "status": "Ошибка",
         "duration": "00:00", "hadmatch": "-", "timestamp": "2025-03-19 14:44:05", "initiator": "Кузьмин РМ"},
        {"id": 3, "source": "Строительный двор - OBI", "state": "Завершена", "status": "Ошибка", "duration": "00:00",
         "hadmatch": "-", "timestamp": "2025-03-19 14:44:05", "initiator": "Кузьмин РМ"},
        {"id": 2, "source": "Строительный двор - Петрович", "state": "Завершена", "status": "Ошибка",
         "duration": "00:00", "hadmatch": "-", "timestamp": "2025-03-19 10:00:11", "initiator": "Кузьмин РМ"},
        {"id": 1, "source": "Строительный двор - OBI", "state": "Завершена", "status": "Ошибка", "duration": "00:00",
         "hadmatch": "-", "timestamp": "2025-03-19 10:00:11", "initiator": "Кузьмин РМ"},
    ]

    return JsonResponse(data, safe=False)


def mapping_scheduled_tasks_table_json(request):
    data = [
        {"id": 3, "main_source": "Строительный двор", "other_sources": "OBI, Петрович", "cron": "59 23 * * 0", "initiator": "Кузьмин РМ"},
    ]

    return JsonResponse(data, safe=False)


def report_tasks_competed_table_json(request):
    data = [
        {"id": 3, "name": "Средние отклонения", "state": "Завершена", "status": "Успешно", "file_type": "pdf",
         "info": "Строительный двор - OBI (7)", "timestamp": "2025-03-31 15:44:14", "initiator": "Кузьмин РМ"},
        {"id": 2, "name": "Средние отклонения", "state": "Завершена", "status": "Успешно", "file_type": "pdf",
         "info": "Строительный двор - Петрович (8)", "timestamp": "2025-03-31 15:41:21", "initiator": "Кузьмин РМ"},
        {"id": 1, "name": "Тест", "state": "Завершена", "status": "Успешно", "file_type": "csv", "info": "Test",
         "timestamp": "2025-03-30 18:12:07", "initiator": "admin"},
    ]

    return JsonResponse(data, safe=False)
