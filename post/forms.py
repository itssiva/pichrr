from django import forms
from django.conf import settings
from utils.image_utils import check_image
from utils.common_utils import txt2set
import re
TITLE_MAX_LENGTH = 300
TITLE_MIN_LENGTH = 10
TXT_TAGS_MAX_LENGTH = 100
ACTUAL_OWNER_MAX_LENGTH = 200
MIN_LANGUAGES = 1
MAX_LANGUAGES = 2
USERNAME_REGEX = re.compile(r'^[\w.@+-]+$', re.UNICODE)

def range_check(number):
    if number >=0 and number <= MAX_LANGUAGES:
        return True
    return False


class PostForm(forms.Form):
    title = forms.CharField(max_length=TITLE_MAX_LENGTH, label= "Title", required=True)
    txt_tags = forms.CharField(max_length=TXT_TAGS_MAX_LENGTH, label='Tags', required=True)
    photo = forms.ImageField(label='Select Photo', required=True)
    creator = forms.CharField(max_length=ACTUAL_OWNER_MAX_LENGTH, label='Actual Source', required=False)
    is_anonymous = forms.BooleanField(label='Post Anonymously', initial=False, required=False)
    OPTIONS = (
                ("1", "English"),
                ("2", "Hindi"),
                ("3", "Telugu"),
                ("4", "Tamil"),
                ("5", "Kannada"),
                )
    languages = forms.MultipleChoiceField(choices=OPTIONS, widget=forms.CheckboxSelectMultiple, label='Choose audience language(Select one or two)', required=True)

    def __init__(self, data=None, files=None, instance=None, *args, **kwargs):
        super(PostForm, self).__init__(data, *args, **kwargs)
        self.files = files
        self.instance = instance

    def clean_photo(self):
        if self.instance:
            return None
        try:
            value = self.files['photo']
        except:
            raise forms.ValidationError('No Photo')
        check_image(value, settings.MAX_PHOTO_SIZE)
        return value

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) > TITLE_MAX_LENGTH or len(title) < TITLE_MIN_LENGTH:
            raise forms.ValidationError('Title too long or short, keep between 20 to 300')
        else:
            return title


    def clean_txt_tags(self):
        txt_tags = self.cleaned_data['txt_tags']
        if len(txt_tags) > 100:
            raise forms.ValidationError('Tags too many or long tags, keep them below 100 characters ')
        txt_tags_set = txt2set(self.cleaned_data['txt_tags'])
        if (len(txt_tags_set)) == 0:
            raise forms.ValidationError('tags cannot be empty')
        for tag in txt_tags_set:
            if len(tag) > 20:
                raise forms.ValidationError('Each tag must be less tahn 20 characters')

        return ','.join(txt_tags_set)

    def clean_languages(self):
        languages = self.cleaned_data['languages']
        if len(languages) >= MIN_LANGUAGES and len(languages) <= MAX_LANGUAGES:
            return self.cleaned_data['languages']
        else:
            raise forms.ValidationError('Select only '+str(MIN_LANGUAGES) + ' or ' + str(MAX_LANGUAGES) +' languages.')

    def clean_creator(self):
        attribute = self.cleaned_data['creator']
        if len(attribute) > ACTUAL_OWNER_MAX_LENGTH:
            raise forms.ValidationError('Too long')
        else:
            return attribute

    def clean_is_anonymous(self):
        import pdb
        print self.cleaned_data['is_anonymous']
        return self.cleaned_data['is_anonymous']

REPORT_REASON_MAX_LENGTH = 500
POST_MAX_LENGTH = 15


class ReportForm(forms.Form):
    REPORTS = (("1", "Abusive Content"),
               ("2", "Copyright violation"),
               ("3", "Copy of another post"),
               ("4", "Spam"),
               ("5", "Adult Content"),
               )

    report_type = forms.ChoiceField(choices=REPORTS)







