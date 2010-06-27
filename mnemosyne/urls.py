from django.conf.urls.defaults import *

urlpatterns = patterns('mnemosyne.views',
    url(r'^$', 'memory_list', name='mnemosyne-memory-list'),
    url(r'^lang/(?P<lang>[a-z]+)/$', 'memory_list', name='mnemosyne-memory-list-lang'),
    url(r'^user/(?P<username>[A-Za-z@.+_-]{1,30})/$', 'user_list', name='mnemosyne-user-list'),
    url(r'^memory/(?P<memory_id>\d+)/$', 'memory_detail', name='mnemosyne-memory-detail'),
    url(r'^memory/random/$', 'memory_random', name='mnemosyne-memory-random'),
    url(r'^memory/random/(?P<lang>[a-z]+)/$', 'memory_random', name='mnemosyne-memory-random-lang'),
    url(r'^memory/create/$', 'create_memory', name='mnemosyne-create-memory'),
    url(r'^memory/(?P<memory_id>\d+)/delete/$', 'delete_memory', name='mnemosyne-delete-memory'),
    url(r'^memory/(?P<memory_id>\d+)/update/$', 'update_memory', name='mnemosyne-update-memory')
)
