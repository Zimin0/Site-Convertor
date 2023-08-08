# Site-Convertor

## request.session contains info:

* "phone_is_confirmed" - [True/False:bool] - does the user`s phone number was confirmed by a sms sending.
* "phone" - [+7xxxxxxxxxx:str] - contains user`s phone number to identify him later.
* "confirmation_code" - [xxxxxx:str] - confirmation code for sms sending


## To make a translation you need this commands:
* python manage.py makemessages -l ru -v 3  // creating a new django.po file with translating pairs.
* python manage.py makemessages -a          // adding changes in django.po if they were made.
* django-admin compilemessages              // compiling django.po into django.mo - need to be done after any changes in django.po.


# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2023-08-06 16:20+0300\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=4; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%"
"10<=4 && (n%100<12 || n%100>14) ? 1 : n%10==0 || (n%10>=5 && n%10<=9) || (n%"
"100>=11 && n%100<=14)? 2 : 3);\n"

#: .\convert_order\templates\convert_order\index.html:33
msgid "File convertor"
msgstr "Конвертор файлов"

#: .\convert_order\templates\convert_order\index.html:35
msgid "Choose language"
msgstr "Выберите язык"

#: .\convert_order\templates\convert_order\index.html:38
msgid "Engligh"
msgstr "Английский"

#: .\convert_order\templates\convert_order\index.html:39
msgid "Russian"
msgstr "Русский"

#: .\convert_order\views.py:27
msgid "Upload 2 files!"
msgstr "Загрузите оба файла!"

#: .\convert_order\views.py:32
msgid "Files {} and {} were uploaded!"
msgstr "Файлы {} и {} были загружены!"

#: .\payment\sms_sender.py:17
msgid "Confirmation code for logging on SAPXMLVersionUP.ru website: {}"
msgstr "Код подтверждения для входа на сайт SAPXMLVersionUP.ru: {}"

#: .\users\templates\users\code.html:9
msgid "Confirmation"
msgstr "Подтверждение"

#: .\users\templates\users\code.html:23
msgid "Close"
msgstr "Закрыть"

#: .\users\templates\users\code.html:31 .\users\views.py:30
msgid "Code has been sent!"
msgstr "Код уже отправлен!"

#: .\users\templates\users\code.html:39
msgid "Â© Copyright 2023. All rights reserved."
msgstr "Â© Copyright 2023. Все права защищены."

#: .\users\templates\users\good_code.html:30
msgid "Phone is confirmed!"
msgstr "Телефон подтвержден!"

#: .\users\views.py:57
msgid "The code doesn`t match.Try again."
msgstr "Код не совпадает. Попробуйте еще раз."

#: .\users\views.py:66
msgid "Code already have sent!"
msgstr "Код уже отправлен!"
