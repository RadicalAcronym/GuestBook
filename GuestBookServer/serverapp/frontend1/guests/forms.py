from django import forms

class GuestNameForm(forms.Form):
    guest_name = forms.CharField(label='Please enter your name', max_length=40)

class UploadVideoForm(forms.Form):
    title = forms.CharField(max_length=50)
    vfile = forms.FileField()