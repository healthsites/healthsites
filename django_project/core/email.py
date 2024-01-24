import logging

from django.conf import settings
from django.core import mail
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_email_with_html(
        subject: str, recipient_list: list, context: dict,
        html_path: str
):
    """Send email with html."""
    message = render_to_string(
        html_path,
        context
    )
    try:
        send_mail(
            subject,
            None,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            html_message=message,
            fail_silently=False
        )
        print(mail.outbox[0])
    except Exception as e:
        logger.exception(e)
