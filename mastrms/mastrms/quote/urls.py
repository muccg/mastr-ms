from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns(
    '',
    #Quotes views
    (r'^listFormal/(?P<qid>\d+)/?$', 'mastrms.quote.views.listFormal'),
    (r'^listAll/?$', 'mastrms.quote.views.listAll'),
    (r'^list/?$', 'mastrms.quote.views.listQuotes'),
    (r'^history/?$', 'mastrms.quote.views.history'),
    (r'^load/?$', 'mastrms.quote.views.load'),
    (r'^listNeedsAttention/?$', 'mastrms.quote.views.listQuotesRequiringAttention'),
    (r'^formalload/?$', 'mastrms.quote.views.formalLoad'),
    (r'^formalsave/?$', 'mastrms.quote.views.formalSave'),
    (r'^formalreject/?$', 'mastrms.quote.views.formalReject'),
    (r'^formalaccept/?$', 'mastrms.quote.views.formalAccept'),
    (r'^save/?$', 'mastrms.quote.views.save'),
    (r'^downloadAttachment/?$', 'mastrms.quote.views.downloadAttachment'),
    (r'^downloadPDF/?$', 'mastrms.quote.views.downloadPDF'),
    (r'^sendRequest/?$', 'mastrms.quote.views.sendRequest'),
    (r'^viewformal/?$', 'mastrms.quote.views.viewFormalRedirect'),
)
