/**
 * This file is part of Madas.
 *
 * Madas is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Madas is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Madas.  If not, see <http://www.gnu.org/licenses/>.
 */


/**
 * madasChangeMainContent 
 * acts as a shallow controller between string function names and initialization/display of pages
 * it should only be called directly when processing the return from an ajax request
 * any time you wish to change the display based on a user action you should call 
 * to MA.Authorize() instead, as that will check authorization first, which can prevent odd
 * situations where a page displays but the content fails
 */
MA.ChangeMainContent = function(contentName, paramArray){

    //Ext.get('center').dom.innerHTML = '';
    var showMenu = true;
    var affectMenu = true;
    var cancelBackTarget = true; //whether or not this action should be invoked if a user clicks Cancel (where the variable is obeyed)

    Ext.QuickTips.init();
    //alert('called ChangeMainContent, contentName was: ' + contentName);
    
    switch (contentName) {
    
        case "dashboard": 
            if (paramArray) {
                resultContent = paramArray[0];
                params = paramArray[1];
                MA.Authorize(resultContent, params);
                break;
            }
            //default
            Ext.getCmp('center-panel').layout.setActiveItem('dashboard-panel'); 
            break;

        case "registration":
            showMenu = false;
            cancelBackTarget = false;
            Ext.getCmp('center-panel').layout.setActiveItem('registration-container-panel');
            break;
            
        case "login":
            showMenu = false;
            cancelBackTarget = false;
            MA.LoginInit(paramArray);
            Ext.getCmp('center-panel').layout.setActiveItem('login-container-panel');
            break;
            
        case "login:forgotpassword":
            showMenu = false;
            cancelBackTarget = false;
            MA.ForgotPasswordInit();
            Ext.getCmp('center-panel').layout.setActiveItem('forgot-password-container-panel');
            break;
            
        case "login:resetpassword":
            showMenu = false;
            cancelBackTarget = false;
            MA.ResetPasswordInit();
            Ext.getCmp('center-panel').layout.setActiveItem('resetpassword-container-panel');
            break;
            
        case "login:processLogout":
            cancelBackTarget = false;
            MA.LogoutInit();
            break;
            
        case "admin:adminrequests":
            MA.AdminRequestsInit();
            Ext.getCmp('center-panel').layout.setActiveItem('adminrequests-panel');
            break;
            
        case "admin:usersearch":
            MA.UserSearchInit();
            Ext.getCmp('center-panel').layout.setActiveItem('usersearch-panel');
            break;
            
        case "admin:rejectedUsersearch":
            MA.RejectedUserSearchInit();
            Ext.getCmp('center-panel').layout.setActiveItem('rejectedusersearch-panel');
            break;
            
        case "admin:deletedUsersearch":
            MA.DeletedUserSearchInit();
            Ext.getCmp('center-panel').layout.setActiveItem('deletedusersearch-panel');
            break;

        case "admin:nodelist":
            MA.NodeManagementInit();
            Ext.getCmp('center-panel').layout.setActiveItem('nodeManagementCmp');
            break;
            
        case "admin:orglist":
            MA.OrgManagementInit();
            Ext.getCmp('center-panel').layout.setActiveItem('orgManagementCmp');
            break;
            
        case "admin:useredit":
            cancelBackTarget = false;
            MA.AdminUserEditInit(paramArray);
            Ext.getCmp('center-panel').layout.setActiveItem('adminuseredit-container-panel');
            break;
            
        case "user:myaccount":
            cancelBackTarget = false;
            MA.UserEditInit(paramArray);
            Ext.getCmp('center-panel').layout.setActiveItem('useredit-container-panel');
            break;
            
        case "notauthorized":
            cancelBackTarget = false;
            Ext.getCmp('center-panel').layout.setActiveItem('notauthorized-panel');
            break;
            
        case "message":
            cancelBackTarget = false;
            affectMenu = false;
            MA.Message(paramArray);
            break;

        case "quote:request":
            MA.RequestQuoteInit();
            Ext.getCmp('center-panel').layout.setActiveItem('requestquote-container-panel');
            affectMenu = false;
            showMenu = false;
            break;
         
        case "quote:list":
            MA.QuoteRequestListInit();
            Ext.getCmp('center-panel').layout.setActiveItem('quotelistpanel');
            break;

        case "quote:edit":
            MA.QuoteRequestEditInit(paramArray);
            Ext.getCmp('center-panel').layout.setActiveItem('quoterequestedit-container-panel');
            break;
            
        case "quote:listAll":
            MA.QuoteRequestListAllInit();
            Ext.getCmp('center-panel').layout.setActiveItem('quoterequestsall-panel');
            break;

        case "quote:viewformal":
            MA.ViewFormalInit(paramArray);
            Ext.getCmp('center-panel').layout.setActiveItem('viewformalquote-container-panel');
            affectMenu = false;
            showMenu = false;
            break;
            
        case "quote:listFormal":
        	MA.FormalQuoteUserListInit();
        	Ext.getCmp('center-panel').layout.setActiveItem('fquolist-panel');
        	break;

    	case "help:screencasts-quoterequest":
    	    MA.ScreencastsInit('madas_requesting_quote.flv');
    	    Ext.getCmp('center-panel').layout.setActiveItem('screencasts-container-panel');
    	    break;
            
        case "help:contactus":
            cancelBackTarget = false;
            affectMenu = false;
            MA.Message({'message':"For any queries and issues please contact,<br><br>Dr.Saravanan Dayalan<br>sdayalan@unimelb.edu.au<br>+61 3 8344 2201"});
            break;
    	    
        case "helpadmin:screencasts-forwardquoterequest":
    	    MA.ScreencastsInit('madas_forwarding_quoterequest.flv');
    	    Ext.getCmp('center-panel').layout.setActiveItem('screencasts-container-panel');
    	    break;
    	    
	    case "helpadmin:screencasts-forwardformal":
    	    MA.ScreencastsInit('madas_sending_formalquote.flv');
    	    Ext.getCmp('center-panel').layout.setActiveItem('screencasts-container-panel');
    	    break;
    	    
	    case "helpadmin:screencasts-replaceformal":
    	    MA.ScreencastsInit('madas_fixing_formalquote.flv');
    	    Ext.getCmp('center-panel').layout.setActiveItem('screencasts-container-panel');
    	    break;
    	    
	    case "helpadmin:screencasts-authrequest":
    	    MA.ScreencastsInit('madas_auth_request.flv');
    	    Ext.getCmp('center-panel').layout.setActiveItem('screencasts-container-panel');
    	    break;
            
            
        default:
            cancelBackTarget = false;
    }
    
    //always affect menu if we are initing the app
    if (contentName == MA.InitFunction) {
        affectMenu = true;
    }

//    if (affectMenu) {
//        if (showMenu) {
//            MA.MenuShow();
//        } else {
//            MA.MenuHide();
//        }
//    }

    MA.MenuEnsure();

    if (cancelBackTarget) {
        MA.CancelBackTarget = contentName;
    }
    
    //append the application path onto the URL as a means of making things bookmarkable
    //var regex = /\#.*$/;
    //window.location = window.location.replace(regex, "#" + contentName);

};

/**
 * madasInitApplication
 * initializes the main application interface and any required variables
 */
MA.InitApplication = function(appSecureUrl, username, mainContentFunction, params) {
   //various global settings for Ext
    Ext.BLANK_IMAGE_URL = appSecureUrl + 'static/ext-3.3.0/resources/images/default/s.gif';
   Ext.QuickTips.init();
    MA.BaseUrl = appSecureUrl;
   
   MA.LoginSubmitURL = appSecureUrl + 'login/processLogin';
   MA.InitFunction = mainContentFunction;

   // turn on validation errors beside the field globally
   Ext.form.Field.prototype.msgTarget = 'side';

   //the ViewPort defines the main layout for the entire Madas app
   //the center-panel component is the main area where content is switched in and out
   
   var viewport = new Ext.Viewport({
        layout:'border',

        items:[
            new Ext.BoxComponent({
                region:'north',
                el: 'north',
                height:54
            }),
            {
                region:'south',
                contentEl: 'south',
                height:20
            },
            {
                region:'center',
                id:'center-panel',
                layout: 'card',
                activeItem:0,
                items: [MA.DashboardCmp, MA.LoginCmp, MA.RegistrationCmp, MA.NotAuthorizedCmp, MA.AdminUserEditCmp, 
                        MA.UserEditCmp, MA.ForgotPasswordCmp, MA.ResetPasswordCmp, MA.NodeManagementCmp,
                        MA.OrgManagementCmp,
                        MA.RequestQuoteCmp, MA.QuoteRequestEditCmp, MA.ViewFormalCmp,
                        MA.ScreencastsCmp]
            }
            ]
    });

    MA.MenuRender(username);
    
    var paramArray;
    if (params) {
        paramArray = params; //eval is evil
    }
   
    MA.Authorize(mainContentFunction, paramArray);
};


MA.Message = function(paramArray) {

    Ext.Msg.alert("", paramArray['message']);

}

/**
 * madasAjaxMetadataProcess
 * look at the other headers in the header of an ajax request for a livegrid or other Object
 * assessing whether the user has timed-out or is not authorized to perform that action
 */
MA.AjaxMetadataProcess = function(ajaxData) {
    
   //look for specific sentinel values in the json
   //var authenticated = ajaxData.response.value.authenticated;
   //var authorized = ajaxData.response.value.authorized;

    var authenticated = ajaxData.authenticated;
    var authorized = ajaxData.authorized;

   if (authenticated != 1) {
        //trigger the login page
        MA.IsLoggedIn = false;
        MA.IsAdmin = false;
        Ext.getCmp('userMenu').setText('User: none');

        MA.ChangeMainContent('login');
        //return false to tell the JsonReader to abort
        return false;
   }
   
   if (authorized != 1) {
        //trigger a notauthorized page
        MA.ChangeMainContent('notauthorized');
        //return false to tell the JsonReader to abort
        return false;
   }
   
   return true;

}
