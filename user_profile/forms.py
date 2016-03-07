from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from utils.image_utils import check_image
import re



class UserProfileForm(forms.ModelForm):


    # first_name = forms.CharField(max_length=30, label='First Name', required=False)
    # last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    # gender = forms.CharField(max_length=1, label='Gender', required=False)
    # intro = forms.CharField(max_length=300,label='Intro', required=False)
    # avatar = forms.ImageField(label='Avatar', required=False)
    class Meta:
        model = UserProfile
        fields = ['first_name', "last_name", "gender", "intro", "avatar"]

    def __init__(self, data=None, files=None, *args, **kwargs):
        super(UserProfileForm, self).__init__(data, *args, **kwargs)
        self.files = files


    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender in ['M', 'F', 'O']:
            return gender
        else:
            raise forms.ValidationError('Do not modify the source code for proper results')

    def clean_avatar(self):
        try:
            value = self.files['avatar']
            check_image(value)
            return value
        except:
            pass
            # raise forms.ValidationError('Uploaded Image cannot be empty')


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if len(first_name)>20:
            raise forms.ValidationError('first name must be less than 20 characters')
        pattern = re.compile('^[\w]+$')
        if pattern.match(first_name) is not None:
            return first_name
        else:
            raise forms.ValidationError('Invalid First Name ')

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        if len(last_name)>20:
            raise forms.ValidationError('last name must be less than 20 characters')
        pattern = re.compile('^[\w]+$')
        if pattern.match(last_name) is not None:
            return last_name
        else:
            raise forms.ValidationError('Invalid Last Name ')
