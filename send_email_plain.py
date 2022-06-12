from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
from flask import Flask,jsonify,request

app = Flask(__name__)


logger = logging.getLogger(__name__)
# Replace smtp_username and smtp_password with your Amazon Pinpoint SMTP user name
    # and password.
SMTP_USERNAME = "AKIAVIASWTZFL52HQPWE"
SMTP_PASSWORD = "BBKW/w6q+hNFUsvz9TF8mi1dbzXJs8T3iaD+LmK2rwH8"
HOST = "email-smtp.us-east-1.amazonaws.com"
PORT = 587

def send_smtp_message(
        smtp_server, sender, to_address, cc_address,
        subject, html_message, text_message):
    """
    Sends an email by using an Amazon Pinpoint SMTP server.

    :param smtp_server: An smtplib SMTP session.
    :param smtp_username: The username to use to connect to the SMTP server.
    :param smtp_password: The password to use to connect to the SMTP server.
    :param sender: The "From" address. This address must be verified.
    :param to_address: The "To" address. If your account is still in the sandbox,
                       this address must be verified.
    :param cc_address: The "CC" address. If your account is still in the sandbox,
                       this address must be verified.
    :param subject: The subject line of the email.
    :param html_message: The HTML body of the email.
    :param text_message: The email body for recipients with non-HTML email clients.
    """
    # Create message container. The correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = to_address
    msg['Cc'] = cc_address
    msg['Subject'] = subject
    msg.attach(MIMEText(html_message, 'html'))
    msg.attach(MIMEText(text_message, 'plain'))

    smtp_server.ehlo()
    smtp_server.starttls()
    # smtplib docs recommend calling ehlo() before and after starttls()
    smtp_server.ehlo()
    smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
    # Uncomment the next line to send SMTP server responses to stdout.
    # smtp_server.set_debuglevel(1)
    smtp_server.sendmail(sender, to_address, msg.as_string())


def send_sample_email():
    # If you're using Amazon Pinpoint in an AWS Region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon Pinpoint SMTP
    # endpoint in the appropriate AWS Region.
    sender = 'yoni.keren@gmail.com'
    to_address = 'yoni.keren@gmail.com'
    #cc_address = "cc_recipient@example.com"
    subject = 'Amazon Pinpoint Test (Python smtplib)'
    text_message = (
        "Amazon Pinpoint Test\r\n"
        "This email was sent through the Amazon Pinpoint SMTP "
        "interface using the Python smtplib package.")
    html_message = """<html>
    <head></head>
    <body>
      <h1>Amazon Pinpoint SMTP Email Test</h1>
      <p>This email was sent with Amazon Pinpoint using the
        <a href='https://www.python.org/'>Python</a>
        <a href='https://docs.python.org/3/library/smtplib.html'>
        smtplib</a> library.</p>
    </body>
    </html>
                """

    

    print("Sending email through SMTP server.")
    send_email(sender=sender,to_address=to_address,subject=subject,text_message=text_message,html_message=html_message)


def send_email(sender,to_address,subject,text_message,html_message=''):
    # If you're using Amazon Pinpoint in an AWS Region other than US West (Oregon),
    # replace email-smtp.us-west-2.amazonaws.com with the Amazon Pinpoint SMTP
    # endpoint in the appropriate AWS Region.
    try:
        with smtplib.SMTP(HOST, PORT) as smtp_server:
            send_smtp_message(
                smtp_server, sender, to_address,
                '', subject, html_message, text_message)
    except Exception:
        logger.exception("Couldn't send message.")
        raise
    else:
        print("Email sent!")


@app.route('/shira/send_email',methods=['POST'])
def send_email_endpoint():
    sender = request.get_json(force = True)['sender']
    to_address = request.get_json(force = True)['to_address']
    subject = request.get_json(force = True)['subject']
    text_message = request.get_json(force = True)['text_message']
    send_email(sender=sender,to_address=to_address,subject=subject,text_message=text_message)
    return jsonify({'status':'sent email'})


if __name__ == '__main__':
   app.run(threaded=False,port=20000,host="0.0.0.0",debug=True)