from django.conf import settings

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.contrib.auth import authenticate, login

from django.forms.models import model_to_dict

from pet_market.forms import SignUpBuyerForm, PostAdForm, UserProfileEditForm, NewAddressForm
from pet_market.models import *

from pet_market.util import file_manager

import json


# Create your views here.
# A sign up page for a buyer
# url: /signup/
def signup_buyer(request):

    user_form = SignUpBuyerForm()

    if request.method == 'POST':
        user_form = SignUpBuyerForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            authenticate(request, phone_number=user_form.cleaned_data['phone_number'],
                         password=user_form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'accounts/signup.html', {'form': user_form})


# the main home page of the user
# url: /
def home(request):

    offset = request.GET.get('offset', 0)

    # getting filtered list of items
    filters = request.GET.get('filters', None)
    if filters is not None:
        filters = json.loads(filters)
        items = Item.objects.filter(**filters).values('id', 'name', 'price', 'type__name')[offset:offset + 5]
    else:
        items = Item.objects.filter().values('id', 'name', 'price', 'type__name')[offset:offset + 5]

    for item in items:
        # getting corresponding images
        image = ItemImages.objects.get(item__id=item['id']).image_1
        item['image'] = image
        item.pop('id')
        item['type'] = item['type__name']
        item.pop('type__name')

    return render(request, 'home/index.html', {'items': items})


# Part of the Post Ad page
# returns the list of valid attributes for an item type
# url : /seller/post-ad/get-item-attr
def get_attributes(request):
    # the item type has been entered, we need to send the list of attributes and its pre-defined values

    if request.method == "GET":
        item_type = request.GET['item_type'].strip()
        item_type_obj = ItemType.objects.get(name=item_type)
        item_attributes = list(ItemAttributeValues.objects.filter(item_type=item_type_obj)\
            .values('attr_type', 'value'))

        print(item_attributes)

        # a set of different types of attributes of the item
        attrib_name_set = set([dict['attr_type'] for dict in item_attributes])

        # a list of attributes and its pre-defined values
        item_attributes = [
            {
                'attr_name': attrib_name,
                'values': [dict['value'] for dict in item_attributes if dict['attr_type'] == attrib_name]
            }
            for attrib_name in attrib_name_set
        ]

        return JsonResponse(item_attributes, safe=False)


# implement this later
# A Part of Post Ad form
# returns a list of invalid fields for a given item type
# url : /seller/post-ad/get-invalid-fields
def get_invalid_fields(request):

    # With the item type, get the corresponding invalid fields from a file stored in server
    invalid_fields = {
        'invalid_fields': ['gender', 'age', 'quantity']
    }

    return JsonResponse(invalid_fields, safe=False)


# A Page for displaying an item
# returns a json object listing out fields foe the specified item
# url : /items/<item_id>/
def display_item(request, item_id):

    if request.method == 'GET':
        item_obj = Item.objects.get(id=item_id)

        attributes = ItemAttributes.objects.filter(item=item_obj)
        attr_list = [
            {attribute.attr_type.name: attribute.value}
            for attribute in attributes
        ]

        # getting related images for the item
        images = model_to_dict(ItemImages.objects.get(item=item_obj))
        images_list = [
            val
            for key, val in images.items()
            if key.startswith('image') and val is not ''
        ]

        # Converting item object into dict
        item_dict = model_to_dict(item_obj)

        # removing foreign keys from the item dict
        item_dict.pop('id')
        item_dict['seller'] = item_obj.seller.user.get_full_name()
        item_dict['type'] = str(item_obj.type)

        context_dict = {
            'item': item_dict,
            'attrs': attr_list,
            'images': images_list
        }
        return render(request, 'items/item_display.html', context=context_dict)


# A Page part of the seller for posting ads
# accepts required fields for filling out the forms
# url :  /seller/post-ad/
def post_ad(request):

    seller = Seller.objects.get(user=request.user)

    if request.method == 'GET':
        item_types = list(ItemType.objects.all().values_list('name', flat=True))
        item_types = [item for item in item_types if '_' not in item]

        item_form = PostAdForm()

        context_dict = {
            'item_types': item_types,
            'post_ad_form': item_form
        }

        return render(request, 'seller/post-ad/post_ad.html', context_dict)

    elif request.method == 'POST':

        item_type_obj = ItemType.objects.get(name=request.POST['item_type'])
        new_item = Item(seller=seller, type=item_type_obj)
        item_form = PostAdForm(request.POST, instance=new_item)

        if item_form.is_valid():

            item_form.save()

            # a list of tuples having attribute and its value
            attrs = [
                (key[:key.find('_attr')], val) for key, val in request.POST.items()
                if key.find('_attr') >= 0
            ]

            for attr, val in attrs:
                attr_obj = AttributeType.objects.get(name=attr)
                ItemAttributeValues.objects.get_or_create(attr_type=attr_obj, item_type=item_type_obj,
                                                          value=val)
                ItemAttributes.objects.create(item=new_item, attr_type=attr_obj, value=val)

            # handling images
            image = request.FILES['image']
            if len(image) > 0:
                file_manager.upload_item_image(new_item, [image])

            return redirect('display_item', item_id=new_item.id)

        else:

            return HttpResponse('failed')


# A part of user account management
# Changes profile fields of a user (at non-admin level)
# url: /accounts/profile/
def user_profile(request):

    user = request.user
    user_form = UserProfileEditForm(instance=user)

    if request.method == 'POST':
        user_form = UserProfileEditForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()

    return render(request, 'accounts/profile.html', {'form': user_form})


# A part of user profile management
# Changes or adds addresses for a given user
# the client needs to send a json data with key 'modify' with something other
# than blank to modify address otherwise new address will be created
# url : /accounts/addresses/
def manage_addresses(request):

    user = request.user

    if request.method == 'GET':
        if request.GET.get('modify', '') is '':
            address_form = NewAddressForm()
        else:
            addr_obj = Address.objects.get(user=user, name=request.GET['name'])
            address_form = NewAddressForm(instance=addr_obj)

    if request.method == 'POST':
        if request.POST.get('modify', '') is '':
            address_form = NewAddressForm(request.POST)
        else:
            addr_obj = Address.objects.get(user=user, name=request.POST['name'])
            address_form = NewAddressForm(request.POST, instance=addr_obj)

        if address_form.is_valid():
            address_form.save()

    return render(request, 'accounts/addresses.html', {'form': address_form})


# A part of seller profile management
# Displays list of items sold or in transit for that seller
# url: /seller/my-sales/
def mysales(request):

    seller = Seller.objects.get(user=request.user)
    items = Item.objects.filter(seller=seller)

    transactions = []
    for item in items:
        try:
            transaction = Transaction.objects.get(item=item)
            seller_address = transaction.seller_address
            transaction_dict = model_to_dict(transaction)
            transaction_dict['item'] = item.name
            transaction_dict['seller_address'] = str(seller_address)
            transaction_dict['seller_address_name'] = seller_address.name
            transaction_dict['image'] = ItemImages.objects.get(item=item).image_1
            transactions.append(transaction_dict)

        except Transaction.DoesNotExist:
            pass

    for transaction in transactions:
        datestr = transaction['approval_date'].strftime('%a, %m %b, %Y')
        transaction['approval_date'] = datestr
        datestr = transaction['delivery_date'].strftime('%a, %m %b, %Y')
        transaction['delivery_date'] = datestr

    return render(request, 'seller/my_sales.html', {'items': transactions})

