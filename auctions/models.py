from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField(null=True,blank=True)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    img_url = models.CharField(max_length=800)
    lister = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True, related_name="creator")
    status =  models.CharField(max_length=50)
    ltime = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.title} listed by {self.lister}"

class Bids(models.Model):
    bidding = models.IntegerField(default=None)
    buyer_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="buyer")
    blisting_id = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="bidlist")

    def __str__(self):
        return f"{self.blisting_id} bidded by {self.buyer_id}"
    
class Comments(models.Model):
    Comment =  models.CharField(max_length=200)
    clisting_id = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    commenter  =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="commenters")
    ctime = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.clisting_id} commented by {self.commenter}"


class Watchlist(models.Model):
    wlisting_id = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="watchlist")
    watchuser  =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="wuser")

    def __str__(self):
        return f"{self.wlisting_id} watchlisted by {self.watchuser}"

