from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelMultipleChoiceField, DateInput
from django.forms import ModelForm, FileInput, FileField
from django.forms.fields import ImageField
from django.forms.forms import Form
from django.urls import reverse
from django_select2.forms import Select2MultipleWidget, Select2Widget
from tinymce.widgets import TinyMCE

from . import settings
from .models import UserProfile, Article, Workshop, WorkshopCategory, \
    WorkshopType, UserInfo, WorkshopUserProfile, WorkshopParticipant
from .widgets import RenderHTML


class UserProfilePageForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_page']
        labels = {'profile_page': "Strona profilowa"}
        widgets = {'profile_page': TinyMCE()}


class UserCoverLetterForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['cover_letter']
        labels = {'cover_letter': "List motywacyjny"}
        widgets = {'cover_letter': TinyMCE()}


class UserInfoPageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserInfoPageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'

    def clean_start_date(self):
        if self.cleaned_data['start_date']:
            if self.cleaned_data['start_date'] < settings.WORKSHOPS_START_DATE:
                raise ValidationError('Warsztaty rozpoczynają się ' + str(settings.WORKSHOPS_START_DATE))
            if self.cleaned_data['start_date'] > settings.WORKSHOPS_END_DATE:
                raise ValidationError('Warsztaty kończą się ' + str(settings.WORKSHOPS_END_DATE))
            if 'end_date' in self.cleaned_data and self.cleaned_data['end_date']:
                if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
                    raise ValidationError('Nie możesz wyjechać wcześniej niż przyjechać! :D')
        return self.cleaned_data['start_date']

    def clean_end_date(self):
        if self.cleaned_data['end_date']:
            if self.cleaned_data['end_date'] < settings.WORKSHOPS_START_DATE:
                raise ValidationError('Warsztaty rozpoczynają się ' + str(settings.WORKSHOPS_START_DATE))
            if self.cleaned_data['end_date'] > settings.WORKSHOPS_END_DATE:
                raise ValidationError('Warsztaty kończą się ' + str(settings.WORKSHOPS_END_DATE))
            if 'start_date' in self.cleaned_data and self.cleaned_data['start_date']:
                if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
                    raise ValidationError('Nie możesz wyjechać wcześniej niż przyjechać! :D')
        return self.cleaned_data['end_date']

    class Meta:
        model = UserInfo
        fields = ['pesel', 'address', 'phone', 'start_date', 'end_date', 'tshirt_size', 'comments']
        labels = {
            'pesel': 'Pesel',
            'address': 'Adres zameldowania',
            'phone': 'Numer telefonu',
            'start_date': 'Data przyjazdu :-)',
            'end_date': 'Data wyjazdu :-(',
            'tshirt_size': 'Rozmiar koszulki',
            'comments': 'Dodatkowe uwagi (np. wegetarianin, uczulony na X, ale też inne)',
        }
        widgets = {
            'start_date': DateInput(attrs={'data-default-date': settings.WORKSHOPS_START_DATE, 'data-start-date': settings.WORKSHOPS_START_DATE, 'data-end-date': settings.WORKSHOPS_END_DATE}),
            'end_date': DateInput(attrs={'data-default-date': settings.WORKSHOPS_END_DATE, 'data-start-date': settings.WORKSHOPS_START_DATE, 'data-end-date': settings.WORKSHOPS_END_DATE})
        }


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
    
    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'matura_exam_year', 'how_do_you_know_about']
        labels = {
            'gender': 'Płeć',
            'school': 'Szkoła lub uniwersytet',
            'matura_exam_year': 'Rok zdania matury',
            'how_do_you_know_about': 'Skąd wiesz o WWW?',
        }


class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'E-mail',
        }


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'name', 'on_menubar', 'content']
        labels = {
            'title': 'Tytuł',
            'name': 'Nazwa (w URLach)',
            'on_menubar': 'Umieść w menu',
            'content': 'Treść',
        }

    def __init__(self, user, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        mce_attrs = {}
        if kwargs['instance']:
            mce_attrs['automatic_uploads'] = True
            mce_attrs['images_upload_url'] = reverse('upload', kwargs={'type': 'article', 'name': kwargs['instance'].name})
            mce_attrs['file_picker_types'] = 'image'
            mce_attrs['file_picker_callback'] = 'tinymce_local_file_picker'
        self.fields['content'].widget = TinyMCE(mce_attrs=mce_attrs)
        if not user.has_perm('wwwapp.can_put_on_menubar'):
            del self.fields['on_menubar']


class WorkshopForm(ModelForm):
    category = ModelMultipleChoiceField(label="Kategorie", queryset=WorkshopCategory.objects.filter(year=settings.CURRENT_YEAR),
                                        widget=Select2MultipleWidget(attrs={'width': '200px'}))

    category.help_text = ""  # this removes annoying message ' Hold down "Control", or "Command" (..) '
    type = ModelChoiceField(label="Rodzaj zajęć", queryset=WorkshopType.objects.filter(year=settings.CURRENT_YEAR),
                            widget=Select2Widget(attrs={'width': '200px'}))

    def __init__(self, *args, **kwargs):
        super(WorkshopForm, self).__init__(*args, **kwargs)
        if self.instance.status:
            self.fields['proposition_description'].disabled = True
            self.fields['proposition_description'].widget = RenderHTML()

    class Meta:
        model = Workshop
        fields = ['title', 'name', 'type', 'category', 'proposition_description']
        widgets = {
            'proposition_description': TinyMCE()
        }
        labels = {
            'title': 'Tytuł',
            'name': 'Nazwa (w URLach)',
            'proposition_description': 'Opis propozycji warsztatów',
        }


class WorkshopPageForm(ModelForm):
    qualification_problems = FileField(required=False, widget=FileInput(), label='Zadania kwalifikacyjne (zalecany format PDF):')

    class Meta:
        model = Workshop
        fields = ['qualification_problems', 'is_qualifying',
                  'qualification_threshold', 'max_points',
                  'page_content', 'page_content_is_public']
        labels = {
            'is_qualifying': 'Czy warsztaty są kwalifikujące (odznacz, jeśli nie zamierzasz dodawać zadań i robić kwalifikacji)',
            'qualification_threshold': 'Minimalna liczba punktów potrzeba do kwalifikacji (wpisz dopiero po sprawdzeniu zadań)',
            'max_points': 'Maksymalna liczba punktów możliwa do uzyskania z obowiązkowych zadań',
            'page_content': 'Strona warsztatów',
            'page_content_is_public': 'Zaznacz, jeśli opis jest gotowy i może już być publiczny.'
        }

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        mce_attrs = {}
        if kwargs['instance']:
            mce_attrs['automatic_uploads'] = True
            mce_attrs['images_upload_url'] = reverse('upload', kwargs={'type': 'workshop', 'name': kwargs['instance'].name})
            mce_attrs['file_picker_types'] = 'image'
            mce_attrs['file_picker_callback'] = 'tinymce_local_file_picker'
        self.fields['page_content'].widget = TinyMCE(mce_attrs=mce_attrs)


class WorkshopParticipantPointsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WorkshopParticipantPointsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # autocomplete=off fixes a problem on Firefox where the form fields don't reset on reload, making the save button visibility desync
            field.widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
            field.required = False

    class Meta:
        model = WorkshopParticipant
        fields = ['qualification_result', 'comment']

    def clean(self):
        # Only apply changes to the fields that were actually sent
        for k, v in self.cleaned_data.items():
            if k not in self.data:
                self.cleaned_data[k] = getattr(self.instance, k, self.cleaned_data[k])


class TinyMCEUpload(Form):
    file = ImageField()