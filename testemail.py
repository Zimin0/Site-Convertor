import smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login('nikzim2004@gmail.com','amikqiygmwhztgir') # 1//0cWOdiCmnWfk3CgYIARAAGAwSNwF-L9Ir5KIrznSE9IgjuN2VM0-yGC2z4_yqX2zoSsUfR50WEbiCJv4j9UlgHWf3ylqu4BwwiS0
smtpObj.sendmail("nikzim2004@gmail.com","nik.zimenkov.00@inbox.ru","go to bed!")