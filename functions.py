def send_email(smtp_server ,from_addr, to_addr, subject, message):
    smtp_server.sendmail(from_addr, to_addr, "Subject: {}\r\n\r\n{}".format(subject, message))
    smtp_server.quit()