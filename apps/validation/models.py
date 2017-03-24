
from __future__ import unicode_literals

from django.db import models
import datetime
import bcrypt
import re

# Create your models here.
class UserAction(models.Manager):
    def newUser(self, POST_data):
        NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+_-]+@[a-zA-Z0-9+_-]+\.[a-zA-Z]+$')
        DATE_REGEX = re.compile(r'^[0-9]{2}/[0-9]{2}/[0-9]{4}')
        PW_REGEX = re.compile(r'^.{8,}$')
        message = []
        if self.filter(email=POST_data['email']):
            message.append('Account Error: Account already exists for that email')
        if not NAME_REGEX.match(POST_data['first_name']) or not NAME_REGEX.match(POST_data['last_name']):
            message.append('Name error: Name fields must be two or more characters')
        if not EMAIL_REGEX.match(POST_data['email']):
            message.append('Email error: Please enter a valid email')
        #Add error check for date hired 1) less than NOW 2) valid form
        if not DATE_REGEX.match(POST_data['date_hired']):
            message.append('Date hired error: Please verify the date format entered (must be mm/dd/yyyy)')
        else:
            hired = POST_data['date_hired'].split('/')
            try:
                dateHired = datetime.date(int(hired[2]),int(hired[0]),int(hired[1]))
            except ValueError:
                message.append('Date Error: Oops, not a valid date')
            else:
                if not dateHired <= datetime.datetime.today().date():
                    message.append('Date Error: Date must be before today')
        if not PW_REGEX.match(POST_data['pw']):
            message.append('Password error: Password must be 8 or more charaters')
        if not POST_data['pw'] == POST_data['pwConf']:
            message.append('Password error: Your passwords do not match')
        if message:
            return message, False
        else:
            hash = bcrypt.hashpw(POST_data['pw'].encode(), bcrypt.gensalt())
            newUser = self.create(first_name=POST_data['first_name'], last_name=POST_data['last_name'], email=POST_data['email'], hire_date=dateHired, password=hash)
            return newUser, True
    def validateUser(self, POST_data):
        message = []
        if POST_data['email']:
            email = POST_data['email']
            checkUser = self.filter(email=email)
            if not checkUser:
                message.append('Login error: User account not present')
                return message, False
            elif bcrypt.hashpw(POST_data['pw'].encode(), checkUser[0].password.encode()) == checkUser[0].password:
                    return checkUser[0], True
            else:
                message.append('Password error: Incorrect password')
                return message, False
        else:
            message.append('Email error: Please enter an email')
            return message, False
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    hire_date = models.DateField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserAction()
