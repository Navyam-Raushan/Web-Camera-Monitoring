import smtplib
from email.message import EmailMessage
import imghdr
import os

PASSWORD = os.getenv("PASSWORD")
SENDER = "bsarthak935@gmail.com"
RECEIVER = "bsarthak935@gmail.com"


def send_mail(image_path):
    host = "smtp.gmail.com"
    port = 587
    # Object creation.
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer.")

    with open(image_path, "rb") as file:
        content = file.read()

    # We could get which type of file(.png, .jpeg, etc.) is this.
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None, content))

    # Server configuration setting.
    gmail = smtplib.SMTP(host, port)
    # STARTING SERVER
    gmail.ehlo()
    gmail.starttls()
    # LOGIN TO SERVER
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    # QUIT THE SERVER
    gmail.quit()


if __name__ == "__main__":
    send_mail()
