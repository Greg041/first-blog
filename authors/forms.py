# Django imports
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _
# Local imports
from authors.models import Author
# Third party imports
from cloudinary.forms import CloudinaryFileField
import uuid


UserModel = get_user_model()

class AuthorAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """

    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "No existe ningún autor con las credenciales provistas"
        ),
        "inactive": _("Esta cuenta se encuentra inactiva."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.email_field = UserModel._meta.get_field(UserModel.EMAIL_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.errors:
                visible.field.widget.attrs['class'] += ' is-invalid'

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            author = Author.objects.filter(user__email=email).first()
            if not author:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login'
                )
            self.user_cache = authenticate(
                self.request, username=author.user.username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.email_field.verbose_name},
        )


class RegisterAuthorForm(forms.ModelForm):
    """ Form to register a new author"""
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Author
        fields = ['email', 'password', 'password_confirmation']

    def __init__(self, *args, **kwargs):
        super(RegisterAuthorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if visible.errors:
                visible.field.widget.attrs['class'] += ' is-invalid'
            
    def clean_email(self):
        """
            Validation for not repeated emails for authors
        """
        if Author.objects.filter(user__email=self.cleaned_data['email']).exists():
            raise ValidationError('Ya existe un autor registrado con este email')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            self.add_error('password', ValidationError("La contraseña y la confirmación de la contraseña deben ser iguales"))
            self.add_error('password_confirmation', ValidationError("La contraseña y la confirmación de la contraseña deben ser iguales"))
        return cleaned_data

    def save(self, commit=True):
        user = get_user_model().objects.create_user(
            username=uuid.uuid4(),
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        author = super().save(commit=False)
        author.user = user
        if commit:
            author.save()
        return author
    

class ModifyAuthorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, required=True, label="Nombre")
    last_name = forms.CharField(max_length=255, required=True, label="Apellido")
    
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'country', 'biography']
        
    
    def __init__(self, *args, **kwargs):
        super(ModifyAuthorForm, self).__init__(*args, **kwargs)
        # Include name and last_name of the user linked to the author as initial values 
        # when an author instance is received
        if 'instance' in kwargs:
            author = kwargs['instance']
            self.fields['first_name'].initial = author.user.first_name
            self.fields['last_name'].initial = author.user.last_name
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
            if visible.name == 'country':
                # Country widget must be half width and center the text
                visible.field.widget.attrs['class'] = 'form-select w-50 text-center'
            if visible.name != 'biography':
                visible.field.widget.attrs['class'] += ' w-50'
                
    def save(self, commit=True):
        author = super(ModifyAuthorForm, self).save(commit=False)
        user = author.user
        
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            author.save()
        
        return author
                

class AuthorProfilePictureForm(forms.ModelForm):
    picture = CloudinaryFileField()
    
    class Meta:
        model = Author
        fields = ['picture']
        
        
    def __init__(self, *args, **kwargs):
        super(AuthorProfilePictureForm, self).__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs['class'] = 'img-fluid rounded'
        self.fields['picture'].options = {
            'tags': 'new_image',
            'format': 'png',
        }