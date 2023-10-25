import os
from datetime import datetime

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from apps.orders.models import Orders, OrderItem, ReservationProduct


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem


def report_data(qs: QuerySet, text, data):
    file = os.path.abspath('simple_demo.pdf')
    font = os.path.abspath('ffont.ttf')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = f'Report {date}'

    response = HttpResponse(content_type=file)
    response['Content-Disposition'] = f'attachment; filename={filename}'
    pages = canvas.Canvas(response, pagesize=(900.0, 1080.0))
    pdfmetrics.registerFont(TTFont('text', font, 'UTF-8'))
    pages.setFont('text', 12)
    pages.setTitle(f'Отчет за {date}')
    pages.drawString(20, 1050, f'{text} {qs.count()}шт')
    y = 1000
    for _ in data:
        pages.drawString(20, y, _)
        y -= 30
    pages.showPage()
    pages.save()
    return response


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'ord_user_id', 'ord_date_created', 'ord_description',
                    'ord_address_delivery', 'ord_paid']
    list_display_links = ('id', 'ord_date_created')
    list_filter = ['ord_date_created', 'ord_paid']
    inlines = [OrderItemAdmin]
    actions = ['get_data']

    @admin.action(description='Распечатать информацию')
    def get_data(self, request, qs: QuerySet):
        cookie_filter = str(request.COOKIES.get('title_filter')).lower()
        if cookie_filter != 'none' and cookie_filter:
            text = f'Новых заказов появилось за {cookie_filter}:'
        else:
            text = 'Всего заказов:'
        data = []
        for attribute in qs:
            if attribute.paid:
                paid = 'оплачен'
            else:
                paid = 'не оплачен'
            data.append(
                f'{attribute.id}: пользователь - {attribute.user},'
                f' адресс доставки - "{attribute.deliv_address}",'
                f' описание - "{attribute.description}", заказ - {paid},'
                f' создан - {attribute.created.strftime("%Y-%m-%d %H:%M:%S")}'
            )
        return report_data(qs, text, data)


@admin.register(ReservationProduct)
class AdminReserveProducts(admin.ModelAdmin):
    list_display = ['id', 'res_order_id', 'res_user_id', 'res_time_created',
                    'res_time_out']
    list_display_links = ('id', 'res_user_id')
    list_filter = ['res_time_out']