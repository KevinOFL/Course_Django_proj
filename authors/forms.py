from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()
    
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number '
            'at least 8 characteres'
            ),
            code='invalid'                  
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: Magy')
        add_placeholder(self.fields['last_name'], 'Ex.: Vanderguelt')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')
        add_attr(self.fields['username'], 'css', 'a-css-class')
    
    password = forms.CharField(
        required=True,
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number '
            'at least 8 characteres'
        ),
        validators=[strong_password]
    )
    
    password2 = forms.CharField(
        required=True,
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        
        labels = {
            'username':'Username',
            'last_name':'Last name',
            'first_name':'First name',
            'email':'E-mail',
            'password':'Password',
        }
        
        help_texts = {
            'email': 'The e-mail must be valid.'
        }
        
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        
    def clean_password(self):
        data = self.clean #.get('password')
        
        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(pipoca)s no campo password',
                code='invalid',
                params={'pipoca': 'atenção'}
            )
        
        return data
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        
        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': 'John Doe'}
            )
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password != password2:
            raise ValidationError({
                'password': ValidationError(
                    'Password and password2 must be equal',
                    code='invalid'
                ),
                'password2':'Password and password2 must be equal',
                
            })