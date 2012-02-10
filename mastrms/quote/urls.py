from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    #Quotes views 
    (r'^listFormal/(?P<qid>.*)$', 'mastrms.quote.views.listFormal', {'SSL':True}),
    (r'^listFormal', 'mastrms.quote.views.listFormal', {'SSL':True}),
    (r'^listAll', 'mastrms.quote.views.listAll', {'SSL':True}),
    (r'^list', 'mastrms.quote.views.listQuotes', {'SSL':True}),
    (r'^history', 'mastrms.quote.views.history', {'SSL':True}),
    (r'^load', 'mastrms.quote.views.load', {'SSL':True}),
    (r'^listNeedsAttention', 'mastrms.quote.views.listQuotesRequiringAttention', {'SSL':True}),
    (r'^formalload', 'mastrms.quote.views.formalLoad', {'SSL':True}),
    (r'^formalsave', 'mastrms.quote.views.formalSave', {'SSL':True}),
    (r'^formalreject', 'mastrms.quote.views.formalReject', {'SSL':True}),
    (r'^formalaccept', 'mastrms.quote.views.formalAccept', {'SSL':True}),
    (r'^save', 'mastrms.quote.views.save', {'SSL':True}),
    (r'^downloadAttachment', 'mastrms.quote.views.downloadAttachment', {'SSL':True}),
    (r'^downloadPDF', 'mastrms.quote.views.downloadPDF', {'SSL':True}),
    (r'^sendRequest', 'mastrms.quote.views.sendRequest', {'SSL':True}),
    (r'^viewformal', 'mastrms.quote.views.viewFormalRedirect', {'SSL':True}),
    
) 
