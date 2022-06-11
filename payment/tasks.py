from io import BytesIO
from myshop.celery import app
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from django.shortcuts import get_object_or_404


@app.task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = get_object_or_404(Order, id=order_id)

    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'

    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    # stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    # weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])

    # attach PDF file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    # send e-mail
    email.send()
