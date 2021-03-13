from django import forms


class CreateTestForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required="")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required="")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), required="")
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required="")


class CreateQuestion(forms.Form):
    OPTIONS = (
        ("text", "text"),
        ("single", "single"),
        ("multiple", "multiple"),
    )
    text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required="")
    type = by_letter = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control', 'id': 'selector'}),
                                         choices=OPTIONS, )


class Register(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required="")
