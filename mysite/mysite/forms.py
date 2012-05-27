from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label='Your e-mail address')
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message

class CustomUserCreationForm(UserCreationForm):
    
    STATE_CHOICES = (
                     ('AL', 'Alabama'),
                     ('AK', 'Alaska'),
                     ('AZ', 'Arizona'),
                     ('AR', 'Arkansas'),
                     ('CA', 'California'),
                     ('CO', 'Colorado'),
                     ('CT', 'Connecticut'),
                     ('DE', 'Delaware'),
                     ('FL', 'Florida'),
                     ('GA', 'Georgia'),
                     ('HI', 'Hawaii'),
                     ('ID', 'Idaho'),
                     ('IL', 'Illinois'),
                     ('IN', 'Indiana'),
                     ('IA', 'Iowa'),
                     ('KS', 'Kansas'),
                     ('KY', 'Kentucky'),
                     ('LA', 'Louisiana'),
                     ('ME', 'Maine'),
                     ('MD', 'Maryland'),
                     ('MA', 'Massachusetts'),
                     ('MI', 'Michigan'),
                     ('MN', 'Minnesota'),
                     ('MS', 'Mississippi'),
                     ('MO', 'Missouri'),
                     ('MT', 'Montana'),
                     ('NE', 'Nebraska'),
                     ('NV', 'Nevada'),
                     ('NH', 'New Hampshire'),
                     ('NJ', 'New Jersey'),
                     ('NM', 'New Mexico'),
                     ('NY', 'New York'),
                     ('NC', 'North Carolina'),
                     ('ND', 'North Dakota'),
                     ('OH', 'Ohio'),
                     ('OK', 'Oklahoma'),
                     ('OR', 'Oregon'),
                     ('PA', 'Pennsylvania'),
                     ('RI', 'Rhode Island'),
                     ('SC', 'South Carolina'),
                     ('SD', 'South Dakota'),
                     ('TN', 'Tennessee'),
                     ('TX', 'Texas'),
                     ('UT', 'Utah'),
                     ('VT', 'Vermont'),
                     ('VA', 'Virginia'),
                     ('WA', 'Washington'),
                     ('WV', 'West Virginia'),
                     ('WI', 'Wisconsin'),
                     ('WY', 'Wyoming'),
                     )
    
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    state = forms.ChoiceField(label="State", choices=STATE_CHOICES)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "state",)
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user