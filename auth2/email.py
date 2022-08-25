# Rest Framework
from rest_framework.response import Response
from rest_framework import status

# Sendgrid
from django.conf import settings
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail


def send_email(email, html_content, subject=None):
    # message = Mail(
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to_emails=email,
    #     subject='Django Rest Template',
    #     html_content=html_content
    # )
    # try:
    #     sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    #     response = sg.send(message)
    #     return Response(
    #         {"success": f"An email has been sent to {email}"},
    #         status=status.HTTP_200_OK,
    #     )
    # except Exception as e:
    #     print(e)
    #     return Response(
    #         {"error": f"An email could not be sent to {email}. Try again or try a different email."},
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )
    pass