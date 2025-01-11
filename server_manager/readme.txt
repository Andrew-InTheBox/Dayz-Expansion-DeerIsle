SYNOPSIS:
Script for download and management of DayZ server and mods.
	

DESCRIPTION: 
This script can be used for download of SteamCMD, DayZ server data and DayZ server mod data.
It can also run DayZ server with specified user configuration (launch parameters, server configuration file).


NOTES:
File Name: Server_manager.ps1 
Author: Bohemia Interactive a.s. - https://feedback.bistudio.com/project/view/2/
Requires: PowerShell V4
Supported OS: Windows 10, Windows Server 2012 R2 or newer
	

LINKS:
DayZ web:
https://dayz.com/

DayZ forums:
https://forums.dayz.com/forum/136-official/

DayZ Wiki:
https://community.bistudio.com/wiki/DayZ:Server_manager


PARAMETERS:				VALUES:				INFO:
	
-u or -update			server/mod/all	 	Update server or mods or both to latest version.

-s or -server			start/stop			Start server or stop running server/servers.

-lp or -launchParam		default/user		Must to be used in combination with -s/-server. 
											Select which file with server launch parameters will be used (default or user).

-app					stable/exp			Select which Steam server application you want to use.


EXAMPLE 1:
	Open Main menu:
	C:\foo> .\Server_manager.ps1
 
EXAMPLE 2:
	Update Experimental server:
	C:\foo> .\Server_manager.ps1 -update server -app exp
	 
EXAMPLE 3:
	Update both server and mods and start server with user config:
	C:\foo> .\Server_manager.ps1 -u all -s start -lp user
	 
EXAMPLE 4:
	Stop running servers:
	C:\foo> .\Server_manager.ps1 -s stop
	 
EXAMPLE 5:
	Help info for specific parameter:
	C:\foo> Get-Help .\Server_manager.ps1 -Parameter update
	 

	 
======================================================================================================

© 2018 Bohemia Interactive a.s.

All rights reserved.

See https://community.bistudio.com/wiki/DayZ:Server_manager for more details of usage