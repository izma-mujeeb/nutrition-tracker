from django import forms 
from info.models import Person 

class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Person 
        exclude = ["monday", "tuesday", "wednesday", "thursday", "friday", "fat", "sodium", "potassium", "cholesterol", "carbohydrates", "fiber", "sugar"] 


class LoginForm(forms.Form):
    username = forms.CharField(label = "Username", 
                               max_length = 100, 
                               widget = forms.TextInput(attrs = {
                                                    "class": "form-control"
                                                    }))
    password = forms.CharField(label = "Password", 
                               max_length = 100, 
                               widget = forms.TextInput(attrs = {
                                                        "class": "form-control"
                                                    }))
    
