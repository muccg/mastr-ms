from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    
    (r'^(?P<module>.*)/authorize', 'madas.quote.views.authorize', {'SSL':True}),
    (r'^authorize', 'madas.quote.views.authorize', {'SSL':True}),
    (r'^user/userload', 'madas.users.views.userload', {'SSL':True}),
    (r'^user/userSave', 'madas.users.views.userSave', {'SSL':True}),
    
    #LDAP Debug view...
    #(r'^(.*)/quote/listgroups', 'madas.quote.views.listGroups'),    
   
    #Quotes views 
    (r'^(.*)quote/listFormal/(?P<qid>.*)$', 'madas.quote.views.listFormal', {'SSL':True}),
    (r'^(.*)quote/listFormal', 'madas.quote.views.listFormal', {'SSL':True}),
    (r'^quote/listAll', 'madas.quote.views.listAll', {'SSL':True}),
    (r'^quote/listGroups', 'madas.quote.views.listGroups', {'SSL':True}),
    (r'^(.*)quote/listRestrictedGroups', 'madas.quote.views.listRestrictedGroups', {'SSL':True}),
    (r'^quote/list', 'madas.quote.views.listQuotes', {'SSL':True}),
    (r'^quote/history', 'madas.quote.views.history', {'SSL':True}),
    (r'^quote/load', 'madas.quote.views.load', {'SSL':True}),
    (r'^quote/formalload', 'madas.quote.views.formalLoad', {'SSL':True}),
    (r'^quote/formalsave', 'madas.quote.views.formalSave', {'SSL':True}),
    (r'^quote/formalreject', 'madas.quote.views.formalReject', {'SSL':True}),
    (r'^quote/formalaccept', 'madas.quote.views.formalAccept', {'SSL':True}),
    (r'^quote/save', 'madas.quote.views.save', {'SSL':True}),
    (r'^quote/downloadAttachment', 'madas.quote.views.downloadAttachment', {'SSL':True}),
    (r'^quote/downloadPDF', 'madas.quote.views.downloadPDF', {'SSL':True}),
    (r'^quote/sendRequest', 'madas.quote.views.sendRequest', {'SSL':True}),
    #links from emails to formal quotes...
    #(r'^quote/viewformal(\D+)(?P<qid>\d+)$', 'madas.quote.views.formalLoad'),
    
    #(r'^quote/viewformal', 'madas.quote.views.redirectMain'),
    #login
    (r'^login/processLogin', 'madas.quote.views.login', {'SSL':True}),
    (r'^login/processLogout', 'madas.login.views.processLogout', {'SSL':True}),
    (r'^login/processForgotPassword', 'madas.login.views.processForgotPassword', {'SSL':True}),
    (r'^login/populateResetPasswordForm', 'madas.login.views.populateResetPasswordForm', {'SSL':True}),
    (r'^login/processResetPassword', 'madas.login.views.processResetPassword', {'SSL':True}),
    (r'^login/forgotPassword', 'madas.login.views.forgotPasswordRedirect', {'SSL':True}),

    #admin
    (r'^admin/adminrequests', 'madas.admin.views.admin_requests', {'SSL':True}),
    (r'^admin/usersearch', 'madas.admin.views.user_search', {'SSL':True}),
    (r'^admin/rejectedUsersearch', 'madas.admin.views.rejected_user_search', {'SSL':True}),
    (r'^admin/deletedUsersearch', 'madas.admin.views.deleted_user_search', {'SSL':True}),
    (r'^admin/listGroups', 'madas.quote.views.listGroups', {'SSL':True}), #using the 'quotes' listGroups
    (r'^admin/nodesave', 'madas.admin.views.node_save', {'SSL':True}),
    (r'^admin/nodeDelete', 'madas.admin.views.node_delete', {'SSL':True}),
    (r'^admin/userload', 'madas.admin.views.user_load', {'SSL':True}), 
    (r'^admin/userSave', 'madas.admin.views.user_save', {'SSL':True}), 
    (r'^admin/orgsave[/]*$', 'madas.admin.views.org_save', {'SSL':True}), 
    (r'^admin/orgDelete[/]*$', 'madas.admin.views.org_delete', {'SSL':True}), 
    (r'^admin/listOrganisations', 'madas.admin.views.list_organisations', {'SSL':True}),

    #registration
    (r'^registration/submit', 'madas.registration.views.submit', {'SSL':True}), 
    
    #(r'serverinfo', 'madas.quote.views.serverinfo'),
    #default
    #(r'^(?P<modname>.*)/(?P<submodname.*>)?(P<args>.*)$', 'madas.quote.views.serveIndex', {module=modname, submodule=submodname, args=args}),
    (r'^(?P<cruft>.*)$', 'madas.quote.views.serveIndex', {'SSL':True}),
    
) 
