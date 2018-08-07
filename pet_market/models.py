from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

# Create your models here.
# class GeneralUser(AbstractUser):
#
#     gender_choices = [
#         ('M', 'Male'),
#         ('F', 'Female')
#     ]
#     gender = models.CharField(max_length=1, choices=gender_choices)
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
#     phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True)


class UserManager(BaseUserManager):

    def create_user(self, phone_number, first_name, last_name, password=None):

        if not phone_number:
            raise ValueError('User must have a phone number')

        user = self.model(phone_number=phone_number, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, password):

        user = self.create_user(phone_number=phone_number, first_name=first_name,
                                last_name=last_name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class NewUser(AbstractBaseUser):

    # Include all the fields common to the user
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Uncomment after implementing UserManager
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):

        short_name = '%s' % self.first_name
        return short_name.strip()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Buyer(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    email = models.EmailField(blank=False)
    gender = models.CharField(choices=gender_choices, max_length=1, blank=False)
    coins = models.IntegerField(blank=False, default=0)


class Seller(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # seller credentials to be added later


class Address(models.Model):

    state_choices = [
        ('West Bengal', 'West Bengal'),
        ('Maharashtra', 'Maharashtra'),
        # Add more
    ]
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    pincode_regex = RegexValidator(regex=r'^[1-9][0-9]{5}$')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=13)
    pincode = models.CharField(validators=[pincode_regex], blank=False, max_length=6)
    locality = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(choices=state_choices, max_length=50, blank=False)
    landmark = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'Address'

    def __str__(self):
        return '%s, %s = %s' % (self.address, self.city, self.pincode)

'''
    Attributes that are not defined in the Item model is added to the below models
    The list are:
    1. Brand - For Pet products (dropdown needed)
    2. Color - For All items (dropdown needed)
    3. Breed - For Pets (dropdown needed)
'''


class ItemType(models.Model):

    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class AttributeType(models.Model):

    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class ItemAttributeValues(models.Model):
    # model for storing list of pre-defined values of certain attributes

    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    attr_type = models.ForeignKey(AttributeType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100, blank=False)

    class Meta:
        verbose_name_plural = 'ItemAttributeValues'

    def __str__(self):
        return '%s ( %s )' % (self.item_type, self.attr_type)


class Item(models.Model):

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    name = models.CharField(max_length=100, blank=False)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)
    # all item characteristics to be included below
    gender = models.CharField(choices=gender_choices, max_length=1, blank=True)    # cannot be applied for pet products
    age = models.IntegerField(blank=True)   # cannot be applied to fishes
    weight = models.IntegerField(blank=True)    # cannot be applied for fishes
    quantity = models.IntegerField(blank=True, default=1)   # To be applied for fishes only
    description = models.TextField(max_length=500, blank=True)  # User-defined (optional)

    def __str__(self):
        return '%s (%d)' % (self.type.name, self.id)


class ItemAttributes(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    attr_type = models.ForeignKey(AttributeType, on_delete=models.CASCADE)
    value = models.CharField(max_length=100, blank=False)

    class Meta:
        verbose_name_plural = 'ItemAtrributes'

    def __str__(self):
        return '%s ( %s )' % (self.item, self.attr_type)


class ItemImages(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField(default=0, blank=False)
    image_1 = models.CharField(max_length=20, blank=True)
    image_2 = models.CharField(max_length=20, blank=True)
    image_3 = models.CharField(max_length=20, blank=True)
    image_4 = models.CharField(max_length=20, blank=True)
    image_5 = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = 'ItemImages'

    def __str__(self):
        return self.image_1

'''    
-> The Transaction and Items are designed assuming all items of a transaction have same status at the same 
    time
'''


class Order(models.Model):

    order_date = models.DateTimeField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    buyer_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.IntegerField(blank=False)
    # no_of_items = models.IntegerField(blank=False)
    invoice = models.FileField()


class Transaction(models.Model):

    choices = [
        ('APR', 'Approved'),
        ('SHP', 'Shipped'),
        ('DLV', 'Delivered'),
    ]
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    seller_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    approval_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    status = models.CharField(max_length=3, choices=choices, default='APR')
    invoice = models.FileField()
    # Any more contracts needed


class Stock(models.Model):

    stock_status = [
        ('U', 'Unavailable'),
        ('A', 'Available')
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=stock_status, blank=False, default='A')
    # offer fields to be added later
