# Site-Convertor

## request.session contains info:

* "phone_is_confirmed" - [True/False:bool] - does the user`s phone number was confirmed by a sms sending.
* "phone" - [+7xxxxxxxxxx:str] - contains user`s phone number to identify him later.
* "confirmation_code" - [xxxxxx:str] - confirmation code for sms sending


## To make a translation you need this commands:
* python manage.py makemessages -l ru -v 3  // creating a new django.po file with translating pairs.
* python manage.py makemessages -a          // adding changes in django.po if they were made.
* django-admin compilemessages              // compiling django.po into django.mo - need to be done after any changes in django.po.