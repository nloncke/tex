from django import forms
import re

class SellForm(forms.Form):
    auction = forms.ChoiceField(choices=(('Yes','Yes'),), required=False, widget=forms.RadioSelect())
    CONDITIONS = (('New', 'New'),
                  ('Like New', 'Like New'),
                  ('Very Good', 'Very Good'),
                  ('Good', 'Good'),
                  ('Acceptable', 'Acceptable'),)
    picked_condition = forms.ChoiceField(choices=CONDITIONS, widget=forms.RadioSelect(), label='Condition')
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    price = forms.RegexField(regex=r'(^[1-9]$)|(^[1-9]\d$)|(^1\d\d$)|(^2\d\d$)')
    #price = forms.IntegerField(min_value=1, max_value=200)