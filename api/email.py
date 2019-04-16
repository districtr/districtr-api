from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, HtmlContent, Subject

from .exceptions import ApiException


def send_email(from_address, to_address, subject, body):
    mail = Mail(
        from_email=From(from_address, "Districtr"),
        subject=Subject(subject),
        to_emails=To(to_address),
        html_content=HtmlContent(body),
    )

    if current_app.config.get("SEND_EMAILS", True) is False:
        print("Sending mail", mail)
        return

    client = SendGridAPIClient(api_key=current_app.config["SENDGRID_API_KEY"]).client
    response = client.mail.send.post(request_body=mail.get())

    if response.status_code >= 300:
        raise ApiException("Unable to send email.", status=500)
