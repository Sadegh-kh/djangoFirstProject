from django import forms


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهاد", "پیشنهاد"),
        ("انتقاد", "انتقاد"),
        ("گزارش", "گزارش"),
    )
    # label
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=12, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)
    massage = forms.CharField(widget=forms.Textarea)
