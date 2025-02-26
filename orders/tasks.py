from celery import shared_task
from django.core.mail import EmailMessage
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    """Send order confirmation email asynchronously."""


    try:
        order = Order.objects.get(id=order_id)
        user = order.user

        # Constructing email body
        email_body = f"Dear {user.username},\n\n"
        email_body += f"Your order with order number {order.order_number} has been created successfully.\n\n"
        email_body += "Order Details:\n"
        for item in order.items.all():
            email_body += f"- {item.product.name}: {item.quantity} x ${item.price}\n"
        email_body += f"\nTotal Price: ${order.total_price}\n\n"
        email_body += "Thank you for shopping with us!\n"
        email_body += "Best regards,\nFlora E-commerce Team"

        order_confirm_mail = EmailMessage(
            subject=f"Order {order.order_number} Confirmation",
            body=email_body,
            to=[user.email]
        )
        order_confirm_mail.send()

        return f"Order confirmation email sent to {user.email}"

    except Order.DoesNotExist:
        return f"Order with ID {order_id} not found."
