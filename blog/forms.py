from django import forms
from .models import Comment


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهادات", "پیشنهاد"),
        ("انتقادات", "انتقاد"),
        ("گزارشات", "گزارش"),
    )
    # label
    name = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={"class":"name_ticket",
                                                                                       "placeholder":"نام"}))
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
        widgets = {'body': forms.Textarea(attrs={"class":"comment_body"})}

    def clean_name(self):
        name=self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("اسم وارد شده باید بیشتر از ۳ کارکتر باشد")
        else:
            return name
