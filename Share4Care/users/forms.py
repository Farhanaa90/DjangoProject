from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SimpleRegistrationForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your email'})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Choose a username'})
    )
    user_type = forms.ChoiceField(
        choices=[('donor', 'Donor - I want to donate'), ('collector', 'Collector - I need help')],
        required=True,
        widget=forms.RadioSelect(attrs={'class': 'mr-2'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Create a password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'user_type', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match!")

        return password2

    def _post_clean(self):
        super(UserCreationForm, self)._post_clean()

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Create or update user profile with selected user_type
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.user_type = self.cleaned_data['user_type']
            profile.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                   'placeholder': 'Your full name'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                   'placeholder': 'Your email'})
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                   'placeholder': 'Phone number'})
    )
    address = forms.CharField(
        required=False, widget=forms.Textarea(
            attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                   'rows': 3, 'placeholder': 'Your address'})
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                   'placeholder': 'Your city'})
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['name'].initial = self.user.first_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data.get('name', '')
            self.user.email = self.cleaned_data.get('email', '')
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile