from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
import datetime
from django.utils import timezone
from django.db.models import Max
from .forms import *


def index(request):
    count=0
    if request.user.is_authenticated:
        l = Watchlist.objects.filter(watchuser = request.user).values('wlisting_id')
        x = [d['wlisting_id'] for d in l if 'wlisting_id' in d]
        count = Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count()
    else:
        x=[]
        
   
    
    return render(request, "auctions/index.html", {
        'count':count,
        "items":Listing.objects.filter(status= 'active'),
        'wids':x
    })

def listing(request):
    if request.user.is_authenticated:
        l = Watchlist.objects.filter(watchuser = request.user).values('wlisting_id')
        x = [d['wlisting_id'] for d in l if 'wlisting_id' in d]
    else:
        x=[]
   
    
    return render(request, "auctions/index.html", {
        'count':Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count(),
        "items":Listing.objects.all(),
        'wids':x
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required

def createListing(request):
    catlog = ['Collectibles & Art','Home & Garden', 'Sporting Goods', 'Electronics', 'Auto Parts & Acessories', 'Toys & Hobbies', 'Fashion', 'Musical Instruments & Gear', 'Others' ]

    if request.method == "POST":
        listing = Listing()
        listing.title = request.POST["title"]
        listing.category = request.POST["category"]
        listing.img_url = request.POST["img_url"]
        listing.price = request.POST["price"]
        listing.description = request.POST["description"]
        listing.lister = request.user
        listing.status = 'active'
        listing.ltime = datetime.datetime.now()
        listing.save()


    return render(request, "auctions/listing.html", {
        'count':Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count(),
        'cats': catlog

    })

@login_required
def categories(request):
    catlog = ['Collectibles & Art','Home & Garden', 'Sporting Goods', 'Electronics', 'Auto Parts & Acessories', 'Toys & Hobbies', 'Fashion', 'Musical Instruments & Gear', 'Others' ]


    return render(request, "auctions/categories.html", {
        'count':Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count(),
        'cats': catlog

    })

@login_required
def categories_view(request,cat):

    l = Watchlist.objects.filter(watchuser = request.user).values('wlisting_id')
    x = [d['wlisting_id'] for d in l if 'wlisting_id' in d]
    
    ll = Listing.objects.filter(category = cat)
    return render(request, "auctions/index.html", {
        'count':Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count(),
        "items":ll,
        'wids':x

    })

def displayItem(request,id):
    x=Bids.objects.filter(blisting_id=id)
    maxbid = x.aggregate(Max('bidding'))['bidding__max']
    winner=None
    msg=False
    if Watchlist.objects.filter(wlisting_id=id ).filter(watchuser=request.user).values('id'):
        wid= Watchlist.objects.filter(wlisting_id=id ).filter(watchuser=request.user).values('id')[0]['id']
    else:
        wid=0



    for p in x:
                
        if p.blisting_id.status == "inactive":
            
            maxbid = x.aggregate(Max('bidding'))['bidding__max']
            winner = p.buyer_id
            if request.user == winner:
                msg = True

    if request.method == 'POST':
        
        if 'Comment' in request.POST:
            c = Comments()
            c.clisting_id= Listing(id=id)
            c.Comment = request.POST['Comment']
            c.commenter = request.user
            c.ctime = datetime.datetime.now()
            c.save()

        else:

            x=Bids.objects.filter(blisting_id=id)
            
            for p in x:
                
                if p.blisting_id.status == "inactive":
                   
                    maxbid = x.aggregate(Max('bidding'))['bidding__max']
                    winner = p.buyer_id
                    if request.user == winner:
                        msg = True


            form = BidsForm(request.POST)
            print('one')
            if form.is_valid() :
                print('two')
                bidding = form.cleaned_data['bidding']
                print('1',bidding, Listing.objects.get(id=id).price)
                if bidding < Listing.objects.get(id=id).price:
                    print('2',bidding, Listing.objects.get(id=id).price)
                    maxbid = x.aggregate(Max('bidding'))['bidding__max']
                    return render(request, "auctions/item.html", {
                    'form':BidsForm(request.POST),
                    'count':Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count(),
                    'item': Listing.objects.get(id=id),
                    'bidders':Bids.objects.all(),
                    'w': Watchlist.objects.filter(wlisting_id=id ).filter(watchuser=request.user),
                    'wid':  wid,
                    'cc':Comments.objects.filter(clisting_id=id),
                    'maxbid':maxbid,
                    'winner':winner,
                    'msg':msg,
                    'ermsg': True
                })
                else:
                    
                    b = Bids()
                    b.bidding = bidding
                    b.blisting_id = Listing(id=id)
                    b.buyer_id = request.user
                    b.save()
                    maxbid = x.aggregate(Max('bidding'))['bidding__max']
           
            
            # b = Bids()
            # b.bidding = request.POST["price"]
            # b.blisting_id = Listing(id=id)
            # b.buyer_id = request.user
            # b.save()
            
    
    
    
        
    
    
    return render(request, "auctions/item.html", {
        'form':BidsForm(),
        'count':Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count(),
        'item': Listing.objects.get(id=id),
        'bidders':Bids.objects.all(),
        'w': Watchlist.objects.filter(wlisting_id=id ).filter(watchuser=request.user),
        'wid':  wid,
        'cc':Comments.objects.filter(clisting_id=id),
        'maxbid':maxbid,
        'winner':winner,
        'msg':msg
    })


@login_required
def watchlist(request):

    wl = Watchlist.objects.filter(watchuser = request.user)
    print(Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count())


    return render(request, "auctions/watchlist.html", {
        'count':Watchlist.objects.filter(watchuser = request.user).values('wlisting_id').count(),
        'items':wl,
        
        

    })

@login_required
def addToWatchlist(request,id):
    items  = Watchlist() 
    items.wlisting_id = Listing(id = id)
    items.watchuser = request.user
    items.save()
    
    return HttpResponseRedirect(reverse("index"))

    

@login_required
def removeFromWl(request,id):
    l = Watchlist(id = id)
    l.delete()
 

    return HttpResponseRedirect(reverse("index"))
    

@login_required
def endBid(request,id):
    l = Listing.objects.get(id=id)
    l.status = "inactive"
    l.save() 

    return HttpResponseRedirect(reverse("index"))
    