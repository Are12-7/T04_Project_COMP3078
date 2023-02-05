from django.forms import ModelForm
from .models import Village


class VillageForm(ModelForm):
    class Meta:
        model = Village
        fields = '__all__'
