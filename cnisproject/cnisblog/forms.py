from django import forms


class emailForm(forms.Form):
    to = forms.EmailField(help_text="enter the reciepient email.")
    sender = forms.EmailField(help_text="enter your email.")
    subject = forms.CharField(help_text="enter your subject.")
    message_text = forms.CharField(help_text="enter your message.")
