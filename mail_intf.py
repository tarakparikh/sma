#!/usr/bin/env python
# Import smtplib for the actual sending function
import smtplib
from datetime import date


# Send the message via our own SMTP server, but don't include the
# envelope header.


def _send_my_mail(my_text):

    FROM = 'tarak_parikh@mentor.com'
    TO = ['tmparikh@gmail.com']
    SUBJECT = "Daily SMA Analysis for " + date.today().strftime("%d-%m-%Y")
    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, my_text)

    #print message
    s = smtplib.SMTP('mail-na.mentorg.com')
    s.sendmail(FROM, TO, message)
    s.quit()



#my_text = "ths is the message that I want \nto send"
#_send_my_mail(my_text)
