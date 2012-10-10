Installing and running the MSDataSync program. (Preview Release)
----------------------------------------------------------------
1. Double click the installer executable
2. Choose where you want to install. For the Preview Release, the default is to a folder on the desktop.
   The installer copies files to the destination directory, and sets up an rsync environment.
3. Installation is complete. Close the installer.


Running the program:
--------------------
The Preview Release does not put an icon on the desktop, or entries in the start menu. The only way to start the program is to navigate to the install directory (the default is a folder called MSDataSync on the desktop) and double click the program executable.

Double click the mdatasync.exe file in the installation folder. 
We need to do some initial configuration to set the program up to run automatically.
From the menu bar, click Edit->Preferences
The preferences dialog will open. You will notice that the text at the very top of the preferences window says that the current node is defaultorg.defaultsite.defaultstation. This is because we have not located our station in the tree yet.


Setting the station identifier:
-------------------------------
Click the 'Choose' button at the top of the preferences dialog. The 'Node Locator' dialog opens, allowing you to find and select the 'target machine' (the machine that this software is installed on) in a tree. The tree is organised into Organisations->Site/Building/Division->MachineName. An example might be:

BioCorpX->North Lab->XPMachine_NLid_425

These need to be set up on the server beforehand, so if your Organisation/Site/Machine is not in the list, please contact CCG and we will get it set up for you. Once you have chosen a machine, the OK button should become available.


Choosing the Data Sync dir:
---------------------------
The next step is to set the location for the client to read data from. Everything under the chosen directory will be analysed to see if it is part of an experiment involving the target machine. Click the 'Browse' button, and find the root directory of your data and click OK.


Setting the Sync frequency:
---------------------------
You can also set the frequency for syncing in minutes. The default is 30 minutes, meaning that the client attempts to sync data to the server every 30 minutes.


Setting the Username:
--------------------
The last important setting is the username. This should have been given to you by CCG. If not, please contact CCG to obtain the username you should use for sync attempts.


Sending the public key:
-----------------------
Lastly, before the client can sync smoothly, the public key that was generated at installation time needs to be sent to the server and set up by the CCG staff. Click the 'Send Key' button, and you should get the response 'ok'. For this Preview release, the CCG staff then need to manually install this key in the correct place, so you need to contact them with your username, notifying them that you have just uploaded a new key.


Performing a Manual Sync:
------------------
Syncing should automatically happen at whichever frequency was set in the preferences dialog. Before this though, we should try an initial manual data sync. 

Choose File->Check Now

Depending on the contents of the sync directory, and the state of the experiments on the website, files may or may not be synced to the server. What should happen is a black window should pop up and ask you to verify the host key for ccg.murdoch.edu.au - this will only be asked once. You should type 'yes and press Enter. 

Set and forget:
---------------

From now on, the client should run automatically.

 

