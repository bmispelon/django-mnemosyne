from django.views.generic.create_update import update_object, delete_object
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required
from authwrapper.decorators import login_required_message as login_required

from mnemosyne.models import Memory
from mnemosyne.forms import MemoryForm
from django.contrib.auth.models import User

def memory_list(request, lang=None):
    if lang is None:
        lang = request.LANGUAGE_CODE
    return object_list(request,
            queryset=Memory.objects.lang(lang),
            paginate_by=15,
            extra_context={
                'lang':lang
            }
    )

def user_list(request, username):
    u = get_object_or_404(User, username=username)
    return object_list(request,
            queryset=Memory.objects.all().filter(author=u.id),
            extra_context={
                'author': u,
            },
            template_name='mnemosyne/user_list.html',
            paginate_by=15,
    )


def memory_detail(request, memory_id):
    return object_detail(request,
            queryset=Memory.objects.all(),
            object_id=memory_id,
    )

def memory_random(request, lang=None):
    if lang is None:
        lang = request.LANGUAGE_CODE
    try:
    	m = Memory.objects.lang(lang).order_by('?')[0]
    except IndexError:
    	messages.error(request, _("Sorry, there are no memories in your language."))
    	redir = reverse('mnemosyne-memory-list-lang', args=['all'])
    else:
    	redir = m.get_absolute_url()
    return HttpResponseRedirect(redir)

@login_required
def create_memory(request): 
    redir = request.REQUEST.get('next')
    if request.method == 'POST':
        f = MemoryForm(request.POST, author=request.user)
        if f.is_valid():
            m = f.save()
            msg = _("The %(verbose_name)s was created successfully.") % {'verbose_name': _('memory')}
            messages.success(request, msg)
            redir = redir or reverse('mnemosyne-memory-detail', args=[m.id])
            return HttpResponseRedirect(redir)
    else:
        f = MemoryForm(author=request.user,
                initial={'lang':request.LANGUAGE_CODE})
    return direct_to_template(request,
            template='mnemosyne/memory_form.html',
            extra_context={
                'form': f,
                'next': redir,
            },
    )


@login_required
def delete_memory(request, memory_id):
    m = get_object_or_404(Memory, pk=memory_id)
    if m.author_id != request.user.id:
        return HttpResponseForbidden('<h1>No way, Jose!</h1>')
    redir = request.REQUEST.get('next') or reverse('mnemosyne-memory-list')
    return delete_object(request,
            model=Memory,
            object_id=memory_id,
            post_delete_redirect=redir,
            extra_context={
                'next': redir,
            },
    )


@login_required
def update_memory(request, memory_id):
    m = get_object_or_404(Memory, pk=memory_id)
    if m.author_id != request.user.id:
        return HttpResponseForbidden('<h1>No way, Jose!</h1>')
    redir = request.REQUEST.get('next') or reverse('mnemosyne-memory-detail', args=[memory_id])
    return update_object(request,
            form_class=MemoryForm,
            object_id=memory_id,
            post_save_redirect=redir,
            extra_context={
                'next': redir,
            }
    )

