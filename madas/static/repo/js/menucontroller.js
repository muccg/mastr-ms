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
            
        case 'experiment:my':
            MA.CurrentExpId = 0;
            experimentListStore.reload();
            Ext.getCmp('center-panel').layout.setActiveItem('experiment-list');
            break;
        case 'experiment:new':
            MA.CurrentExpId = 0;
            var namefield = Ext.getCmp('experimentName');
            var desc = Ext.getCmp('experimentDescription');
            var comment = Ext.getCmp('experimentComment');
            var formalQuote = Ext.getCmp('formalQuote');
            var jobNumber = Ext.getCmp('jobNumber');
            var et = Ext.getCmp("experimentTitle");
            et.setTitle('new experiment');
            
            namefield.setValue('');
            desc.setValue('');
            comment.setValue('');
            formalQuote.setValue('');
            jobNumber.setValue('');
            //fall through to force render of new experiment
        case 'experiment:view':
            Ext.getCmp('center-panel').layout.setActiveItem(0);
            Ext.getCmp('expNav').getSelectionModel().selectFirstRow();            
            break;
            
        case 'admin:db':
            window.location = "../repoadmin/";
            break;
            
        case 'clients:list':
            clientsListStore.reload();
            Ext.getCmp('center-panel').layout.setActiveItem('clients-list');
            break;
            
        case 'clients:samples':
            Ext.getCmp('center-panel').layout.setActiveItem('client-samples-list');
            break;
            
        case 'projects:list':
            projectsListStore.reload();
            Ext.getCmp('center-panel').layout.setActiveItem('projects-list');
            break;
            
        case 'project:new':
            MA.CurrentProjectId = 0;
            var titlefield = Ext.getCmp('projectTitle');
            var desc = Ext.getCmp('projectDescription');
            
            titlefield.setValue('');
            desc.setValue('');
            //fall through to force render of new experiment
        case 'project:view':
            Ext.getCmp('center-panel').layout.setActiveItem(6);
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

MA.Message = function(paramArray) {
    
    Ext.Msg.alert("", paramArray.message);
    
};

