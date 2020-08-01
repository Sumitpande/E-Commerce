from django.contrib import admin
from .models import *
# Register your models here.


class ListAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price","category","status","lister", "description", "img_url","ltime")
    list_editable = ("title", "price","category","status","lister", "description", "img_url","ltime")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidding","buyer_id","blisting_id")
    list_editable = ( "bidding","buyer_id","blisting_id")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "Comment","clisting_id", "commenter","ctime")
    list_editable = ( "Comment","clisting_id", "commenter","ctime")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id","wlisting_id", "watchuser")
    list_editable = ("wlisting_id", "watchuser")



admin.site.register(User)
admin.site.register(Listing, ListAdmin)
admin.site.register(Bids,BidAdmin)
admin.site.register(Comments,CommentAdmin)
admin.site.register(Watchlist,WatchlistAdmin)