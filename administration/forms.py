from django import forms


class AddEventForm(forms.Form):
    title = forms.CharField()
    source = forms.ChoiceField()
    url = forms.URLField()
    start = forms.DateTimeField()
    end = forms.DateTimeField(required=False)
    all_day = forms.BooleanField()
    location = forms.CharField(required=False)
    agenda = forms.ChoiceField()

    def for_user(self, user):
        self["source"].field.choices = [(x.id, x.source) for x in user.usersource_set.all()]
