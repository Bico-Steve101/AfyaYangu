from django import forms


class PaymentForm(forms.Form):
    phone_number = forms.CharField(max_length=15)


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}))