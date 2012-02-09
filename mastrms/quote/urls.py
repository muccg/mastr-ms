from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    #Quotes views 
    (r'^listFormal/(?P<qid>.*)$', 'madas.quote.views.listFormal', {'SSL':True}),
    (r'^listFormal', 'madas.quote.views.listFormal', {'SSL':True}),
    (r'^listAll', 'madas.quote.views.listAll', {'SSL':True}),
    (r'^list', 'madas.quote.views.listQuotes', {'SSL':True}),
    (r'^history', 'madas.quote.views.history', {'SSL':True}),
    (r'^load', 'madas.quote.views.load', {'SSL':True}),
    (r'^listNeedsAttention', 'madas.quote.views.listQuotesRequiringAttention', {'SSL':True}),
    (r'^formalload', 'madas.quote.views.formalLoad', {'SSL':True}),
    (r'^formalsave', 'madas.quote.views.formalSave', {'SSL':True}),
    (r'^formalreject', 'madas.quote.views.formalReject', {'SSL':True}),
    (r'^formalaccept', 'madas.quote.views.formalAccept', {'SSL':True}),
    (r'^save', 'madas.quote.views.save', {'SSL':True}),
    (r'^downloadAttachment', 'madas.quote.views.downloadAttachment', {'SSL':True}),
    (r'^downloadPDF', 'madas.quote.views.downloadPDF', {'SSL':True}),
    (r'^sendRequest', 'madas.quote.views.sendRequest', {'SSL':True}),
    (r'^viewformal', 'madas.quote.views.viewFormalRedirect', {'SSL':True}),
    
) 
