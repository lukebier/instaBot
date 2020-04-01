import smtplib
from email.message import EmailMessage
        

def main(var):
    """
    Function used to send a notification Email when the quitter() has been activiated. 
    """

    senderMail = "sender@mail.de"
    receiverMail = "receiver@mail.com"
    msg = EmailMessage()
    msg['From'] = senderMail
    msg['To'] = receiverMail
    
    if var == 0:
        subject = "Programm gestartet"
    else:
        subject = "Programm beendet"

    msg['Subject'] = subject

    if var == 0:
        emailText = "Dein Programm wurde regulär gestartet."
    else:
        emailText = "Dein Programm wurde regulär beendet. Kontrolliere den Server, falls du es erneut starten möchtest."
    
    msg.set_content(emailText)

    server = smtplib.SMTP('serverurl', 'port')
    server.starttls()
    server.login(senderMail, 'password')
    text = msg.as_string()
    server.sendmail(senderMail, receiverMail, text)
    server.quit()