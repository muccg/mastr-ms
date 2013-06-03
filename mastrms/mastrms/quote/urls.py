from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(
    '',
    #Quotes views
    (r'^listFormal/(?P<qid>.*)$', 'mastrms.quote.views.listFormal', {'SSL':settings.SSL_ENABLED}),
    (r'^listFormal', 'mastrms.quote.views.listFormal', {'SSL':settings.SSL_ENABLED}),
    (r'^listAll', 'mastrms.quote.views.listAll', {'SSL':settings.SSL_ENABLED}),
    (r'^list', 'mastrms.quote.views.listQuotes', {'SSL':settings.SSL_ENABLED}),
    (r'^history', 'mastrms.quote.views.history', {'SSL':settings.SSL_ENABLED}),
    (r'^load', 'mastrms.quote.views.load', {'SSL':settings.SSL_ENABLED}),
    (r'^listNeedsAttention', 'mastrms.quote.views.listQuotesRequiringAttention', {'SSL':settings.SSL_ENABLED}),
    (r'^formalload', 'mastrms.quote.views.formalLoad', {'SSL':settings.SSL_ENABLED}),
    (r'^formalsave', 'mastrms.quote.views.formalSave', {'SSL':settings.SSL_ENABLED}),
    (r'^formalreject', 'mastrms.quote.views.formalReject', {'SSL':settings.SSL_ENABLED}),
    (r'^formalaccept', 'mastrms.quote.views.formalAccept', {'SSL':settings.SSL_ENABLED}),
    (r'^save', 'mastrms.quote.views.save', {'SSL':settings.SSL_ENABLED}),
    (r'^downloadAttachment', 'mastrms.quote.views.downloadAttachment', {'SSL':settings.SSL_ENABLED}),
    (r'^downloadPDF', 'mastrms.quote.views.downloadPDF', {'SSL':settings.SSL_ENABLED}),
    (r'^sendRequest', 'mastrms.quote.views.sendRequest', {'SSL':settings.SSL_ENABLED}),
    (r'^viewformal', 'mastrms.quote.views.viewFormalRedirect', {'SSL':settings.SSL_ENABLED}),

)
