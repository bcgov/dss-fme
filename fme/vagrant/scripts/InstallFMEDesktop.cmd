rem install FME Desktop 2020.2.4 silently
msiexec.exe /i "C:\vagrant\fme-desktop-2020.2.4-b20825-win-x64.msi" /qb /l*v "C:\Temp\fme-desktop-2020.2.4-b20825-win-x64-msi.log" INSTALLLEVEL=3 INSTALLDIR="C:\Program Files\FME" ENABLE_POST_INSTALL_TASKS=no

rem authorize the software using a floating license
"C:\Program Files\FME\fmelicensingassistant" --%FME_LICENSING_SERVER% %FME_EDITION_NAME%
