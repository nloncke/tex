from django import forms

class SellForm(forms.Form):
    auction = forms.BooleanField(intial=False, required=False)
    CONDITIONS = (('New', 'New'),
                  ('Like New', 'Like New'),
                  ('Very Good', 'Very Good'),
                  ('Good', 'Good'),
                  ('Acceptable', 'Acceptable'),)
    picked_condition = forms.MultipleChoiceField(choices=CONDITIONS, widget=forms.CheckboxInput())
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    #price = forms.CharField(regex=r"(^[1-9]$)|(^[1-9]\d$)|(^1\d\d$)|(^2\d\d$)")
    price = forms.IntegerField(min_value=1, max_value=200)
    SEMESTERS = (('Fall', 'Fall'),
                 ('Spring', 'Spring'),)
    picked_semester = forms.MultipleChoiceField(choices=SEMESTERS, widget=forms.CheckboxInput())
    #year = forms.CharField(regex=r'^20[1-9][0-9]$')
    year = forms.IntegerField(min_value=2010)