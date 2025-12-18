from django.db import models
from django.utils import timezone
from django.conf import settings



class FriendsList(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=(models.CASCADE), 
                                related_name='friends_list')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return self.user.user_name

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)
        
    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Terminates a friendship and reciprocally deletes friends from their friends list
        -removee is the object of the terminating friendship
        -self is the one terminating it
        """
        self.remove_friend(removee)
        #queries the user you want to remove from your friends list.
        friends_list= FriendsList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=(models.CASCADE), related_name='friend_requests_sent')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=(models.CASCADE), related_name='friend_requests_received')
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender','receiver'],
                name="unique_friend_request"
            )
        ]

    def __str__(self):
        return self.sender.user_name
    
    def accept(self):
        """Queries the friends list of both the sender and the receiver and adds both
        to their respective friends lists"""
        receiver_friends_list = FriendsList.objects.get(user=self.receiver)
        if receiver_friends_list:
            receiver_friends_list.add_friend(self.sender)    
            sender_friends_list = FriendsList.objects.get(user=self.sender)
            if sender_friends_list:
                sender_friends_list.add_friend(self.receiver)
        self.is_active = False
        self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        """
        works like decline, only differs from it in the 
        way it's handled by the app (notifications etc...)
        """
        self.is_active = False

    def renew(self):
        """makes request active again"""
        self.is_active = True
        self.save()