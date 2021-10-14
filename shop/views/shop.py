from typing import ItemsView
from django.db.models.aggregates import Sum
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from shop.models import Deliveries, Item, Request, Users

# Create your views here.
@login_required(login_url='/login')
def dashboard(request):
   
    # Merchant
    storeadmins=Users.objects.filter(is_storeadmin=True)
    storeadmins_count=Users.objects.filter(is_storeadmin=True).count()
    deliveries_caption="ALL STORES"
    stores_caption="ALL STORES"
    stores=Deliveries.objects.values_list('store', flat=True).distinct()
    items_count=Item.objects.all().aggregate(Sum('number_of_items'))
    deliveries_count=Deliveries.objects.all().count()
    store_deliveries=Deliveries.objects.all()
    store_items=Item.objects.all()

    # Store admin
    clerks=Users.objects.filter(is_storeadmin=False, is_superuser=False)
    clerks_count=Users.objects.filter(is_storeadmin=False, is_superuser=False).count()
    individual_store_deliveries=Deliveries.objects.filter(store=request.user.store)
    individual_store_stock=Item.objects.filter(store=request.user.store)
    store_deliveries_count=Deliveries.objects.filter(store=request.user.store).count()
    storeitems_count=Item.objects.filter(store=request.user.store).aggregate(Sum('number_of_items'))
    unresponded_requests_count=Request.objects.filter(store=request.user.store, status="Pending").count()
    individual_stock_caption="All Products"
    individual_store_caption="All Deliveries"

    # clerk
    clerk_unpaid_deliveries=Deliveries.objects.filter(clerk=request.user, status=False).all()
    clerk_paid_deliveries=Deliveries.objects.filter(clerk=request.user, status=True).all()
    clerk_deliveries_count=Deliveries.objects.filter(clerk=request.user.id).count()
    clerk_requests_count=Request.objects.filter(clerk=request.user.id).count()
 
   
    # search in merchant dashboard
    if 'merchant' in request.POST:
        if 'searchdeliveriesby_store_name' == request.POST.get('merchant'): 
            store_name=request.POST.get("store_name")
            deliveries_caption="Store "+store_name
            store_deliveries=Deliveries.objects.filter(store=store_name).all()
    
        elif 'searchitemsby_store_name' == request.POST.get('merchant'): 
            store_name=request.POST.get("store_name")
            store_items=Item.objects.filter(store=store_name).all()
            stores_caption="Store "+store_name

        elif 'delete' == request.POST.get('merchant'): 
            id = request.POST.get('id')
            Users.objects.get(id=id).delete()
            messages.add_message(request, messages.SUCCESS,'Store admin deleted successfully!')
            return redirect(dashboard)
        
        elif 'activate' == request.POST.get('merchant'): 
            id = request.POST.get('id')
            user=Users.objects.get(id=id)
            user.is_active=True
            user.save()
            messages.add_message(request, messages.SUCCESS,'Store admin activated successfully!')
            return redirect(dashboard)

        elif 'deactivate' == request.POST.get('merchant'): 
            id = request.POST.get('id')
            user=Users.objects.get(id=id)
            user.is_active=False
            user.save()
            messages.add_message(request, messages.SUCCESS,'Store admin deactivated successfully!')
            return redirect(dashboard)

    # clerk
    if 'clerk' in request.POST:
        if 'confirm_paid' == request.POST.get('clerk'): 
            id = request.POST.get('id')
            delivery=Deliveries.objects.get(id=id)
            delivery.status=True
            delivery.save()
            messages.add_message(request, messages.SUCCESS,'Payment confirmed successfully!')
            return redirect(dashboard)


     # search in store admin dashboard
    elif 'store_admin' in request.POST:
        if 'searchstockby_item_name' == request.POST.get('store_admin'): 
            item_name=request.POST.get("item_name")
            individual_stock_caption=item_name
            individual_store_stock=Item.objects.filter(store=request.user.store,item_name=item_name).all()
    
        elif 'searchproductby_product_name' == request.POST.get('store_admin'): 
            product_name=request.POST.get("product_name")
            individual_store_deliveries=Deliveries.objects.filter(item_name=product_name).all()
            individual_store_caption=product_name

    merchants={"deliveries":store_deliveries,"storeadmins_count":storeadmins_count,"storeadmins":storeadmins,
     "deliveries_count":deliveries_count,"deliveries_caption":deliveries_caption,"stores_caption":stores_caption,"stores":stores,"store_items":store_items, "items_count":items_count}

    store_admins={"clerks":clerks,"clerks_count":clerks_count,"individual_store_deliveries":individual_store_deliveries,"store_deliveries_count":store_deliveries_count,
     "storeitems_count":storeitems_count,"unresponded_requests_count":unresponded_requests_count,"individual_stock_caption":individual_stock_caption,
     "individual_store_stock":individual_store_stock,"individual_stock_caption":individual_stock_caption,"individual_store_caption":individual_store_caption}
    clerk_variables={"clerk_paid_deliveries":clerk_paid_deliveries,"clerk_unpaid_deliveries":clerk_unpaid_deliveries,'clerk_deliveries_count':clerk_deliveries_count,'clerk_requests_count':clerk_requests_count}
  
     
    c_variables={**merchants, **store_admins}
    context={**clerk_variables,**c_variables}
    return render(request, 'dashboard.html',context)



'''
New items
'''

def new_items(request):
    if request.method == "POST":
        name = request.POST.get('name')
        code = request.POST.get('code')
        total_items = request.POST.get('number')
        spoiled = request.POST.get('spoiled')
        good_items = int(total_items)-int(spoiled)
        buying_price = request.POST.get('b_price')
        selling_price = request.POST.get('s_price')
        status = request.POST.get('status')
        if status == "1":
            status = False
        elif status == "2":
            status = True

        deliveries = Deliveries(item_code=code, item_name=name, status=status,
                                items_received=total_items, items_spoiled=spoiled,clerk=request.user)
        deliveries.save()
        check_Item = Item.objects.filter(item_code=code).count()
        if check_Item > 0:
            item = Item.objects.get(item_code=code)
            item.number_of_items = item.number_of_items + good_items
            item.save()
        else:
            item = Item(item_code=code, buying_price=buying_price,
                        selling_price=selling_price, item_name=name, number_of_items=good_items,store=request.user.store)
            item.save()

        messages.add_message(request, messages.SUCCESS,'Item saved successfully!')
    return render(request, 'new_items.html')


def send_requests(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        number_of_items = request.POST.get('number_of_items')

        new_request = Request(
            item_name=item_name, number_of_items=number_of_items, clerk=request.user, status="Pending",store=request.user.store)
        new_request.save()

        messages.add_message(request, messages.SUCCESS, 'Request sent!')
        return redirect(send_requests)

    else:
        requests=Request.objects.filter(clerk=request.user)
        return render(request, 'send_requests.html',{"requests":requests})

    '''RESPONDING TO REQUEST'''
def storeadmin_requests(request):
    if "requests" in request.POST:
        id=request.POST.get("id")
        if "approve" ==request.POST.get("requests"):
            req=Request.objects.get(id=id)
            req.status="Approved"
            req.save()

            messages.add_message(request, messages.SUCCESS, 'Request approved!')
            return redirect(storeadmin_requests)

        elif "decline" ==request.POST.get("requests"):
            req=Request.objects.get(id=id)
            req.status="Declined"
            req.save()
            messages.add_message(request, messages.SUCCESS, 'Request declined!')
            return redirect(storeadmin_requests)       

    requests=Request.objects.filter(store= request.user.store)
    return render (request,'requests.html',{"requests":requests})  

