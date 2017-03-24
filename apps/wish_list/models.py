from __future__ import unicode_literals
from ..validation.models import User
from django.db import models
import re
REGEX_ITEM = re.compile(r'^.{3,}$')

# Create your models here.
class ItemAction(models.Manager):
    def checkItem(self, POST):
        if REGEX_ITEM.match(POST['new_item']):
            return True
        else:
            return False
    def makeItem(self, POST):
            return self.create(name=POST['new_item'], creator=User.objects.get(id=int(POST['user_id'])))
    def deleteItem(self, item_id):
        self.get(id=int(item_id)).delete()
        return
    def addToList(self, user_id, item_id):
        user = User.objects.get(id=int(user_id))
        item = self.get(id=int(item_id))
        item.wish_user.add(user)
        return
    def removeFromList(self, user_id, item_id):
        user = User.objects.get(id=int(user_id))
        item = self.get(id=int(item_id))
        item.wish_user.remove(user)
        return
    def getUsers(self, id):
        return self.get(id=int(id))
    def getAvailableItems(self, user):
        return self.all().exclude(creator__id=user).exclude(wish_user__id=user)
    def getUsersItems(self, user):
        return self.filter(wish_user=user)

class Item (models.Model):
    name = models.CharField(max_length=20)
    creator = models.ForeignKey(User, related_name='users_items')
    wish_user = models.ManyToManyField(User, related_name='user_wishes')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = ItemAction()
