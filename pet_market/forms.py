from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from pet_market.models import Buyer, NewUser, Item, Address


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput())

    class Meta:
        model = NewUser
        fields = ('first_name', 'last_name', 'phone_number')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewUser
        fields = ('first_name', 'last_name', 'phone_number', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class SignUpBuyerForm(UserCreationForm):

    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect())

    class Meta:
        model = NewUser
        fields = UserCreationForm.Meta.fields + ('email', 'gender',)

    def save(self, commit=True):
        user = super(SignUpBuyerForm, self).save(commit=True)
        Buyer.objects.create(user=user, gender=self.cleaned_data['gender'])
        return user


class PostAdForm(forms.ModelForm):

    item_type = forms.CharField(max_length=50)

    class Meta:
        model = Item
        fields = ('item_type', 'name', 'price', 'gender', 'age', 'weight', 'quantity', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.Meta.fields:
            field = self.fields[field_name]
            field.widget.attrs.update({
                'class': 'post_ad_form',
                'id': field_name + '_field',
                'placeholder': field_name
            })
            field.label = ''


class UserProfileEditForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        fields = ('first_name', 'last_name', 'phone_number')

    def clean_password(self):
        pass


class NewAddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('name', 'phone_number', 'pincode', 'locality', 'address', 'city', 'state',
                  'landmark')
        widgets = {
            'address': forms.Textarea()
        }