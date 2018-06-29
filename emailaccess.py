import smtplib

MY_MAIL = secret.my_mail
MY_PASSWORD = secret.my_password
GMAIL_SMTP_URL = 'smtp.gmail.com:587'
LINKCHAT_ACTIVATION_URL = 'zuccchat.pythonanywhere.com/activate-account/'

def create_server_connection()
    server = smtplib.SMTP(GMAIL_SMTP_URL)
    server.ehlo()
    server.starttls()

    #Next, log in to the server
    server.login(MY_MAIL, MY_PASSWORD)

    return server


def send_activation_message(activation_token, reciptient_mail)
    #Send the mail
    msg = "Welcome to linkchat! \n\n\n Your activation link is " + LINKCHAT_ACTIVATION_URL + activation_token # The /n separates the message from the headers
    server.sendmail(MY_MAIL, reciptient_mail , msg)