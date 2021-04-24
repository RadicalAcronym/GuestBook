from django import forms

class GuestNameForm(forms.Form):
    guest_name = forms.CharField(label='Please enter your name', max_length=40)

# class UploadVideoForm(forms.Form):
#     vfile = forms.FileField(label='Video file')