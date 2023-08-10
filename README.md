# Site-Convertor

## request.session contains info:
* "phone_is_confirmed" - [True/False:bool] - does the user`s phone number was confirmed by a sms sending.
* "phone" - [+7xxxxxxxxxx:str] - contains user`s phone number to identify him later.
* "confirmation_code" - [xxxxxx:str] - confirmation code for sms sending
* "last_page" - contains 
* "cookies_is_confirmed" 

## To make a translation you need this commands:
* python manage.py makemessages -l ru -v 3  // creating a new django.po file with translating pairs.
* python manage.py makemessages -a          // adding changes in django.po if they were made.
* django-admin compilemessages              // compiling django.po into django.mo - need to be done after any changes in django.po.

* While adding translation - do not forget to mark all quotes in your text like that: 
text:           "Swear me that you will not take \"this\" thing"
translation :   "Пообещай мне, что ты не будешь брать \"это\" "

* Also: delete lines, that contain fuzzy tag. Otherwise, they will be ignored in translation! 
* If you need add text in JS - use command: django-admin makemessages -d djangojs -a
* In templates russian language can be used instead of english phrases
* How to add translated videos - they must be named as [button<№1-2>_<lang-code>] - f. e. - button2_en

## Before changing email in admin django - make sure:
* that your mail is by Google (contains "gmail" part)
- you are using app key, generated in Google account settings - not your password

## Proger notes
Something is going wrong with FileFields - unfixable issue with convertation. 
Is it more reliably to store filepath in CharField ? FileField do the same. 