; example1.nsi
;
; This script is perhaps one of the simplest NSIs you can make. All of the
; optional settings are left to their default settings. The installer simply 
; prompts the user asking them where to install, and drops a copy of example1.nsi
; there. 

;--------------------------------
!include EnvVarUpdate.nsh

; The name of the installer
Name "MSDataSync"

; The file to write
OutFile "$%USERPROFILE%\Desktop\MSDataSync_Install.exe"

; The default installation directory
InstallDir $DESKTOP\MSDataSync

; The uninstall registry location
;  This constant specifies Windows uninstall key for your application.
!define REG_UNINSTALL "Software\Microsoft\Windows\CurrentVersion\Uninstall\MSDataSync"


; Request application privileges for Windows Vista
RequestExecutionLevel user

;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put All the DIST files there
  File /r dist\*.*

  ; Put the genkeys batch file there
  File genkeys.bat

  ; install VC redist
  File ..\supportwin32\vcredist_x86.exe

  ; Now silently install the vc redist
  ExecWait '"vcredist_x86.exe" /q:a'

  ; install cwrsync
  ; First, copy over the cwrsync installer
  File ..\supportwin32\cwRsync_4.0.5_Installer.exe

  ;Now run a silent install.
  ExecWait '"cwRsync_4.0.5_Installer.exe" /S'

  ;Now set environment variables for CWRSYNCHOME and append to path
  
  ;Now we set them for this 'shell' so that our script can use them,
  !define cwrsynchome '$PROGRAMFILES\CWRSYNC'
  System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("CWRSYNCHOME", "${cwrsynchome}").r0'
  StrCmp $0 0 error
  System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("PATH", "%PATH%;${cwrsynchome}\BIN").r0'
  StrCmp $0 0 error
  Goto done
  error:
    MessageBox MB_OK "Can't set environment variable"
  done:
 

  ; include for some of the windows messages defines
  !include "winmessages.nsh"
  ; HKLM (all users) vs HKCU (current user) defines
  !define env_hklm 'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"'
  !define env_hkcu 'HKCU "Environment"'
  ; set variable
  WriteRegExpandStr ${env_hkcu} "CWRSYNCHOME" "${cwrsynchome}" 
  ; make sure windows knows about the change
  SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
  
  DetailPrint "Sleeping 5 seconds"
  Sleep 5000

  #now update path
  ${EnvVarUpdate} $0 "PATH" "A" "HKCU" "${cwrsynchome}\BIN"
  ; WriteRegExpandStr ${env_hkcu} "PATH" "$%PATH%;${cwrsynchome}\BIN" 
  ; make sure windows knows about the change
  SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
  
  DetailPrint "Sleeping 5 seconds"
  Sleep 5000

  
  #install private key
  ExecWait 'genkeys.bat >> genkeys_output.txt'

  ;Uninstall Information
    WriteRegStr HKLM "${REG_UNINSTALL}" "DisplayName" "MSDataSync -- Data Sync Application by CCG"
  WriteRegStr HKLM "${REG_UNINSTALL}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
SectionEnd ; end the section

Section Uninstall
  ;TODO: remove cwrsync

  ;Remove PATH entry
  ${un.EnvVarUpdate} $0 "PATH" "A" "HKCU" "${cwrsynchome}\BIN"

  ;Removes directory and registry key:
  RMDIR /r $INSTDIR
  DeleteRegKey HKLM "${REG_UNINSTALL}"
SectionEnd

