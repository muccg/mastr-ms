from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^listFormal/(?P<qid>\d+)/?$', views.listFormal),
    url(r'^listAll/?$', views.listAll),
    url(r'^list/?$', views.listQuotes),
    url(r'^history/?$', views.history),
    url(r'^load/?$', views.load),
    url(r'^listNeedsAttention/?$', views.listQuotesRequiringAttention),
    url(r'^formalload/?$', views.formalLoad),
    url(r'^formalsave/?$', views.formalSave),
    url(r'^formalreject/?$', views.formalReject),
    url(r'^formalaccept/?$', views.formalAccept),
    url(r'^save/?$', views.save),
    url(r'^downloadAttachment/?$', views.downloadAttachment),
    url(r'^downloadPDF/?$', views.downloadPDF),
    url(r'^sendRequest/?$', views.sendRequest),
    url(r'^viewformal/?$', views.viewFormalRedirect),
]
