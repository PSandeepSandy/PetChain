from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from pet_market.models import *
from pet_market.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('first_name', 'last_name', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone_number', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(NewUser, UserAdmin)
admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Address)

admin.site.register(Transaction)
admin.site.register(Order)

admin.site.register(ItemType)
admin.site.register(ItemAttributes)
admin.site.register(AttributeType)
admin.site.register(Item)
admin.site.register(ItemAttributeValues)
admin.site.register(ItemImages)

admin.site.register(Stock)

admin.site.unregister(Group)
