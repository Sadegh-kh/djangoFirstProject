from django import forms
from .models import Comment, Post


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهادات", "پیشنهاد"),
        ("انتقادات", "انتقاد"),
        ("گزارشات", "گزارش"),
    )
    # label
    name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={"class": "name_ticket",
                                                                                        "placeholder": "نام"}))
    email = forms.EmailField()
    phone = forms.CharField(max_length=12, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    message = forms.CharField(widget=forms.Textarea)

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isnumeric():
            raise forms.ValidationError("شماره تلفن عددی نیست")
        else:
            return phone


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {'body': forms.Textarea(attrs={"class": "comment_body"})}

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("اسم وارد شده باید بیشتر از ۳ کارکتر باشد")
        else:
            return name


class PostForm(forms.ModelForm):
    image_1 = forms.ImageField(label="تصویر اول",required=False)
    image_2 = forms.ImageField(label="تصویر دوم",required=False)

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']

        def clean_title(self):
            title = self.cleaned_data['title']
            if len(title) < 1:
                raise forms.ValidationError("باید موضوع بیشتر از ۱ کارکتر باشه ")
            elif len(title) > 250:
                raise forms.ValidationError("باید موضوع کمتر از ۲۵۰ کارکتر باشه")
            else:
                return title

        def clean_description(self):
            description = self.cleaned_data['description']
            if len(description) < 5:
                raise forms.ValidationError("باید موضوع بیشتر از ۵ کارکتر باشه ")
            else:
                return description

        def clean_reading_time(self):
            reading_time = self.cleaned_data['reading_time']
            if reading_time <= 0:
                raise forms.ValidationError("باید زمان خواندن بیشتر از ۰ باشد ")
            else:
                return reading_time


class SearchForm(forms.Form):
    query = forms.CharField()
