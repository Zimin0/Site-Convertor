def send_email(to_email:str, message:str):
    """ Отправляет письмо на почту to_email с текстом message. """
    import smtplib
    status = True
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('nikzim2004@gmail.com','amikqiygmwhztgir') # 1//0cWOdiCmnWfk3CgYIARAAGAwSNwF-L9Ir5KIrznSE9IgjuN2VM0-yGC2z4_yqX2zoSsUfR50WEbiCJv4j9UlgHWf3ylqu4BwwiS0
    smtpObj.sendmail(to_email, "nik.zimenkov.00@inbox.ru", message)
send_email('nik.zimenkov.00@inbox.ru', 'hello world!')