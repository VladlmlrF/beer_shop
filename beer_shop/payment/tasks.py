from io import BytesIO
from celery import shared_task
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.core.mail import EmailMessage
from orders.models import Order


@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@beer_shop.com',
                         [order.email])
    template = get_template('orders/order/pdf.html')
    context = {'order': order}
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
        email.attach(response)
        email.send()
