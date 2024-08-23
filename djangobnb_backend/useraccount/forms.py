from django.forms import ModelForm

from .models import User


class EditUserAccountForm(ModelForm):
  class Meta:
    model = User
    fields = (
      'name','description','avatar'
    )