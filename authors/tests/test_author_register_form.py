from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: Magy'),
        ('last_name', 'Ex.: Vanderguelt'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_palceholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
    
    @parameterized.expand([
        ('email', ('The e-mail must be valid.')),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number '
            'at least 8 characteres')),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
    
    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2')
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)
        
class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ng@P@assword1',
            'password2': 'Str0ng@P@assword1',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password2'),
        ('email', 'E-mail is required'),
    ])
    def test_field_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
        
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must have at least 4 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
    
    def test_username_field_mix_length_should_be_150(self):
        self.form_data['username'] = 'a'*151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must have less than 150 characters.'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'adc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = ( 
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number '
            'at least 8 characteres'
        )
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
        self.form_data['password'] = 'Abc@123456'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.context['form'].errors.get('password'))
        
    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@XXXadc123'
        self.form_data['password2'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Password and password2 must be equal'
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))
        
        self.form_data['password'] = '@XXXadc1234'
        self.form_data['password2'] = '@XXXadc1234'
        
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        self.assertNotIn(msg, response.content.decode('utf-8'))
        
    def test_view_create_not_method_post(self):
        url = reverse('authors:register_create')
        response = self.client.get(url, data=self.form_data, follow=True)
        
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 200)
        
    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'User e-mail is already in use'
        
        self.assertIn(
            msg,
            response.context['form'].errors.get('email')
        )
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        
        self.form_data.update({
            'username': 'testUser',
            'password': 'A@bc12345',
            'password2': 'A@bc12345',
        })
        
        self.client.post(url, data=self.form_data, follow=True)
        
        is_authenticated = self.client.login(
            username='testUser',
            password='A@bc12345'
        )
        
        self.assertTrue(is_authenticated)
        