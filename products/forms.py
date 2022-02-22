from django import forms
from .widgets import CustomClearableFileInput
from .models import Bike, Brand


class BikeForm(forms.ModelForm):

    class Meta:
        model = Bike
        fields = '__all__'

    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        brands = Brand.objects.all()
        frontend_names = [(c.id, c.get_frontend_name()) for c in brands]

        self.fields['brand'].choices = frontend_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

