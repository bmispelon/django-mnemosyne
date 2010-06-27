from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from tagging.fields import TagField
from django.contrib.auth.models import User

from mnemosyne.managers import MemoryManager

class Memory(models.Model):
    text = models.TextField(_('I remember'), max_length=500)
    text_html = models.TextField(_('HTML'))
    added = models.DateTimeField(_('added on'), auto_now_add=True)
    edited = models.DateTimeField(_('edited on'), auto_now=True)
    lang = models.CharField(_('language'), max_length=5, choices=map(lambda e: (e[0], _(e[1])), settings.LANGUAGES))
    author = models.ForeignKey(User, verbose_name=_('author'), blank=True, null=True)
    tags = TagField(_('tags'))
    
    objects = MemoryManager()
    
    class Meta:
        verbose_name = _('memory')
        verbose_name_plural = _('memories')
        get_latest_by = 'added'
        ordering = ('-added',)
    
    def __unicode__(self):
        return _('Memory #%(id)s') % {'id': self.id}

    def i_remember(self):
        from django.utils import translation as tr
        curlang = tr.get_language()
        tr.activate(self.lang)
        ret = tr.gettext('I remember')
        tr.activate(curlang)
        return ret
    
    @models.permalink
    def get_absolute_url(self):
        return ('mnemosyne-memory-detail', [str(self.id)])
    
    def cache_text_to_html(self):
        from markdown import markdown
        from BeautifulSoup import BeautifulSoup, Tag, NavigableString
        from mnemosyne.utils import purge_html
        
        text_html = markdown(self.text)
        soup = purge_html(BeautifulSoup(text_html))
        
        i_remember_tag = Tag(soup, "span")
        i_remember_tag.insert(0, NavigableString(self.i_remember() + ' '))
        i_remember_tag['class'] = 'iremember'
        soup.first().insert(0, i_remember_tag)
        
        return soup.decode()
    
    
    
    def save(self, *args, **kwargs):
        self.text_html = self.cache_text_to_html()
        super(Memory, self).save()
