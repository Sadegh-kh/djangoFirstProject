from django import forms


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهادات", "پیشنهاد"),
        ("انتقادات", "انتقاد"),
        ("گزارشات", "گزارش"),
    )
    # label
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=12, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    message = forms.CharField(widget=forms.Textarea)

    def clean_phone(self):
        phone=self.cleaned_data["phone"]
        if not phone.isnumeric():
            raise forms.ValidationError("شماره تلفن عددی نیست")
        else:
            return phone

