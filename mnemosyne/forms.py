from django import forms
from mnemosyne.models import Memory

class MemoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._author = kwargs.pop('author', None)
        super(MemoryForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self._author:
            self.instance.author = self._author
        return super(MemoryForm, self).clean()

    class Meta:
        model = Memory
        fields = ('text', 'lang', 'tags')
