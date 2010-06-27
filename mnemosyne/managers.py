from django.db.models import Manager

def get_install_lang():
    from django.conf import settings
    return settings.LANGUAGE_CODE

class MemoryManager(Manager):
    def lang(self, lang=None):
        if lang is None:
            lang = get_install_lang()
        if lang == 'all':
            return self.all()
        return self.all().filter(lang=lang)
    
