; example1.nsi
;
; This script is perhaps one of the simplest NSIs you can make. All of the
; optional settings are left to their default settings. The installer simply 
; prompts the user asking them where to install, and drops a copy of example1.nsi
; there. 

;--------------------------------

; The name of the installer
Name "MSDataSync"

; The file to write
OutFile "MSDataSync_Install.exe"

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

  ; install cwrsync
  ; First, copy over the cwrsync installer
  File supportwin32\cwRsync_3.1.0_Installer.exe

  ;Now run a silent install.
  ExecWait '"cwRsync_3.1.0_Installer.exe" /S'

  ;Uninstall Information
  WriteRegStr HKLM "${REG_UNINSTALL}" "DisplayName" "MSDataSync -- Data Sync Application by CCG"
  WriteRegStr HKLM "${REG_UNINSTALL}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
SectionEnd ; end the section

Section Uninstall
  ;TODO: remove cwrsync
 
  ;Removes directory and registry key:
  RMDIR /r $INSTDIR
  DeleteRegKey HKLM "${REG_UNINSTALL}"
SectionEnd

