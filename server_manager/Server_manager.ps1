<# 
.SYNOPSIS 
	Script for download and management of DayZ server and mods.
	
.DESCRIPTION 
	This script can be used for download of SteamCMD, DayZ server data and DayZ server mod data.
	It can also run DayZ server with specified user configuration (launch parameters, server configuration file).
	
.NOTES 
	File Name  : Server_manager.ps1 
	Author : Bohemia Interactive a.s. - https://feedback.bistudio.com/project/view/2/
	Requires  : PowerShell V4
	Supported OS  : Windows 10, Windows Server 2012 R2 or newer
	
.LINK 
	https://community.bistudio.com/wiki/...

.EXAMPLE 
	Open Main menu:
	 C:\foo> .\Server_manager.ps1
 
.EXAMPLE 
	Update server:
	 C:\foo> .\Server_manager.ps1 -update server
	 
.EXAMPLE 
	Update both server and mods and start server with user config:
	 C:\foo> .\Server_manager.ps1 -u all -s start -lp user
	 
.EXAMPLE 
	Stop running servers:
	 C:\foo> .\Server_manager.ps1 -s stop
	 
.PARAMETER update 
   Update server and/or mods to latest version. Can be substituted by -u
   
   Use values:
   server - updates DayZ server data
   mod - updates selected mod data
   all - updates both DayZ server and mod data
   
.PARAMETER u
   Update server and/or mods to latest version. Can be substituted by -update
   
   Use values:
   server - updates DayZ server data
   mod - updates selected mod data
   all - updates both DayZ server and mod data
   
.PARAMETER server 
   Start or stop DayZ server. Can be substituted by -s
   Can be combined with -launchParam or -lp parameters.
   
   Use values:
   start - start DayZ server
   stop - stop running DayZ servers
   
.PARAMETER s
   Start or stop DayZ server. Can be substituted by -server
   Can be combined with -launchParam or -lp parameters.
   
   Use values:
   start - start DayZ server
   stop - stop running DayZ servers
   
.PARAMETER launchParam
   Choose if Dayz server should start with default or user launch parameters. Can be substituted by -lp
   Must be used in combination with -server or -s parameters.
   Default value is used if not specified otherwise.
   
   Use values:
   default - start DayZ server with default launch parameters
   user - start DayZ server with user launch parameters
   
.PARAMETER lp
   Choose if Dayz server should start with default or user launch parameters. Can be substituted by -launchParam
   Must be used in combination with -server or -s parameters.
   Default value is used if not specified otherwise.
   
   Use values:
   default - start DayZ server with default launch parameters
   user - start DayZ server with user launch parameters

.PARAMETER app 
   Select which Steam server application you want to use.
   Can be combined with all other parameters.
   Default value "stable" is used if not specified.
   
   Use values:
   stable - Stable Steam server app
   exp - Experimental Steam server app
  
#> 

#Comand line parameters
param
(
  [string] $u = $null,
  [string] $update = $null,
  [string] $s = $null,
  [string] $server = $null,
  [string] $lp = $null,
  [string] $launchParam = $null,
  [string] $app = $null
)

#Prepare variable for selection in menus
$select = $null

#Prepare variables related to user Documents folder
$userName = $env:USERNAME
$docFolder = 'C:\Users\' + $userName + '\Documents\DayZ_Server'
$steamDoc = $docFolder + '\SteamCmdPath.txt'
$modListPath = $docFolder + '\modListPath.txt'
$serverModListPath = $docFolder + '\serverModListPath.txt'
$modServerPar = $docFolder + '\modServerPar.txt'
$serverModServerPar = $docFolder + '\serverModServerPar.txt'
$userServerParPath = $docFolder + '\userServerParPath.txt'
$pidServer = $docFolder + '\pidServer.txt'
$tempModList = $docFolder + '\tempModList.txt'
$tempModListServer = $docFolder + '\tempModListServer.txt'

#Prepare variables related to SteamCMD folder
$steamApp = $null
$appFolder = $null
$folder = $null
$loadMods = $null


#Main menu
function Menu {

	echo "`n"
	echo "Menu:"
	echo "1) Server update"
	echo "2) Mod update"
	echo "3) Start server"
	echo "4) Stop running server"
	echo "5) Uninstall/Remove saved"
	echo "6) Exit"
	echo "`n"

	$select = Read-Host -Prompt 'Please select desired action from menu above'
	
    switch ($select)
        {
            #Call server update and related functions
            1 {
                echo "`n"
			    echo "Server update selected"
			    echo "`n"
			
			    SteamCMDFolder
			    SteamCMDExe
			    SteamLogin
			
			    Menu

                Break
            } 

            #Call mods update and related functions
            2 {
                echo "`n"
				echo "Mod update selected"
				echo "`n"
						
				SteamCMDFolder
				SteamCMDExe
				SteamLogin
						
				Menu

                Break
            }

            #Start DayZ server
            3 {
                echo "`n"
				echo "Start server selected"
				echo "`n"
								
				SteamCMDFolder
								
				$select = $null
								
				Server_menu
								
				Menu

                Break
            }

            #Stop running server
            4 {
                echo "`n"
				echo "Stop running server selected"
				echo "`n"
										
				ServerStop
										
				Menu

                Break
            }

            #Purge saved login/path info
            5 {
                echo "`n"
				echo "Uninstall/Remove saved selected"
				echo "`n"
												
				Remove_menu
                
                Break
            }

            #Close script
            6 {
                echo "`n"
				echo "Exit selected"
				echo "`n"
														
				exit 0

                Break
            }

            #Force user to select one of provided options
            Default {
                
                echo "`n"
				echo "Select number from provided list (1-6)"
				echo "`n"
																
				Menu
            }
        }
}


#SteamCMD folder
function SteamCMDFolder {
	#Check for file with path to SteamCMD folder
	if (!(Test-Path "$steamDoc"))
		{
			#Prompt user to insert path to SteamCMD folder
			$script:folder = Read-Host -Prompt 'Insert path where is or where will be created SteamCMD folder (without quotation marks)'

			#Check if path was really inserted
			if ($folder -eq "")
				{
					echo "`n"
					echo "No folder path inserted! Returning to Main menu..."
					echo "`n"
					
					Menu
				}
			
			echo "`n"
			echo "Selected SteamCMD folder is $folder"
			echo "`n"
			
			#Create SteamCMD folder if it doesn't exist
			if (!(Test-Path "$folder"))
				{
					echo "Selected SteamCMD folder created"
					echo "`n"
					
					mkdir "$folder" >$null
				}

			#Prompt user to save path to SteamCMD folder for future use
			$saveFolder = Read-Host -Prompt 'Do you want to save path for future use? (yes/no)'

			if ( ($saveFolder -eq "yes") -or ($saveFolder -eq "y")) 
				{ 	
					#Create DayZ_Server folder if it doesn't exist
					if (!(Test-Path "$docFolder"))
						{
							mkdir "$docFolder" >$null
						}
					
					#Save path to SteamCMD folder
					$folder | Set-Content "$steamDoc"
					
					echo "`n"
					echo "Path saved to $steamDoc"
					echo "`n"
				}
		} else {
					#Use saved path to SteamCMD folder
					$script:folder = Get-Content "$steamDoc"
					
					echo "Selected SteamCMD folder is $folder"
					echo "`n"
					
					#Create SteamCMD folder if it doesn't exist
					if (!(Test-Path "$folder"))
						{
							echo "Selected SteamCMD folder created"
							echo "`n"
							
							mkdir "$folder" >$null
						}
				}
}


#SteamCMD exe
function SteamCMDExe {
	#Check if SteamCMD.exe exist
	if (!(Test-Path "$folder\steamcmd.exe")) 
		{
			echo "`n"
			#Prompt user to download and install SteamCMD
			$steamInst = Read-Host -Prompt "'$folder\steamcmd.exe' not found! Do you want to download and install it to previously chosen folder? (yes/no)"
			echo "`n"
			
			if ( ($steamInst -eq "yes") -or ($steamInst -eq "y")) 
				{ 
					echo "Downloading and installing SteamCMD..."
					echo "`n"

                    #Get Powershell version for compatibility check
					$psVer = $PSVersionTable.PSVersion.Major

                    if ($psVer -gt 3) 
	                    { 

				            echo "Using Powershell version $psVer"
							echo "`n"

                            #Download SteamCMD
                            $downloadURL = "http://media.steampowered.com/installer/steamcmd.zip"
                            $destPath = "$folder\steamcmd.zip"

                            (New-Object System.Net.WebClient).DownloadFile($downloadURL, $destPath)

                            #Unzip SteamCMD
                            $shell = New-Object -ComObject Shell.Application
                            $zipFile = $shell.NameSpace($destPath)
                            $unzipPath = $shell.NameSpace("$folder")

                            $copyFlags = 0x00
                            $copyFlags += 0x04 # Hide progress dialogs
                            $copyFlags += 0x10 # Overwrite existing files

                            $unzipPath.CopyHere($zipFile.Items(), $copyFlags)
						
						#If Powershell version is under 4
			            } else { 
						            echo "`n"
									echo "Wrong Powershell version $psVer !"
									echo "`n"
					           }
					
					#Update SteamCMD to latest version
					Start-Process -FilePath "$folder\steamcmd.exe" -ArgumentList ('+quit') -Wait -NoNewWindow
					
					sleep -Seconds 1 
					
					if (Test-Path "$folder\steamcmd.exe") 
						{
							#Remove SteamCMD zip file after successful installation
							Remove-Item -Path "$folder\steamcmd.zip" -Force
							
							echo "`n"
							echo "SteamCMD was successfully installed."
							echo "`n"
							
						} else {
									#Throw error if SteamCMD doesn't exist after installation
									echo "$folder\steamcmd.exe not found!"
									echo "`n"
									
									pause
									
									Menu
								}
				} else {
							#Throw error if SteamCMD doesn't exist and user chose not to install
							echo "$folder\steamcmd.exe not found!"
							echo "`n"
							
							pause
							
							Menu
						}			
		}
}

#Steam login
function SteamLogin {
	#Path to encrypted Steam login files
	$steamLog1 = $docFolder + '\SteamLog1.txt'
	$steamLog2 = $docFolder + '\SteamLog2.txt'

	#If one or both files don't exist
	if (!(Test-Path "$steamLog1") -or !(Test-Path "$steamLog2"))
		{
			echo "`n"
			#Prompt user to save Steam login to encrypted file for future use
			$slogin = Read-Host -Prompt 'Do you want to save Steam login for future use? (yes/no)'
			echo "`n"

			if ( ($slogin -eq "yes") -or ($slogin -eq "y")) 
				{ 	
					#Create DayZ_Server folder if it doesn't exist
					if (!(Test-Path "$docFolder"))
						{
							mkdir "$docFolder" >$null
						}
					
					#Save Steam login details to encrypted files
					#Steam username
					$steamUs = Read-Host -Prompt 'Insert Steam username'
					echo "`n"
					
					$secureSteamUs = ConvertTo-SecureString -String $steamUs -AsPlainText -Force
					$secureSteamUs | ConvertFrom-SecureString | Set-Content "$steamLog1"
					
					#Steam password
					$secureSteamPw = Read-Host -Prompt 'Insert Steam password' -AsSecureString
					
					$secureSteamPw | ConvertFrom-SecureString | Set-Content "$steamLog2"
					$steamPw = (New-Object PSCredential $userName,$secureSteamPw).GetNetworkCredential().Password
					
					echo "`n"
					echo "Steam login saved to encrypted file"
					echo "`n"

				} else {
							#Log in Steam without save of credentials
							$steamUs = Read-Host -Prompt 'Insert Steam username'
							echo "`n"

							$securePw = Read-Host -Prompt 'Insert Steam password' -AsSecureString
							echo "`n"
							
							$steamPw = (New-Object PSCredential $userName,$securePw).GetNetworkCredential().Password

						}
		} else {
					#Use stored Steam login credentials
					$secureUser = Get-Content "$steamLog1" | ConvertTo-SecureString
					$steamUs = (New-Object PSCredential $userName,$secureUser).GetNetworkCredential().Password
					
					$securePw = Get-Content "$steamLog2" | ConvertTo-SecureString
					$steamPw = (New-Object PSCredential $userName,$securePw).GetNetworkCredential().Password
					
					echo "Using stored Steam login credentials"
					echo "`n"
						
				}
		
		#Server update selected
		if ($select -eq '1') 
		{ 
			ServerUpdate
		}
		
		#Mods update selected
		if ($select -eq '2') 
		{ 
			ModsUpdate
		}
		
}
				
#Update DayZ server data
function ServerUpdate {
	
	echo "Downloading DayZ server now..."
	echo "`n"

	#Login to SteamCMD and update DayZ server app
	Start-Process -FilePath "$folder\steamcmd.exe" -ArgumentList ('+login',$steamUs,$steamPw,'+app_update',$steamApp,' -validate','+quit') -Wait -NoNewWindow

	sleep -Seconds 1 
	
	$script:steamUs = $null
	$script:steamPw = $null

	echo "`n"
	echo "DayZ server was updated to latest version"
	echo "`n"
	
}

#Update mods
function ModsUpdate {
	
	#Path to DayZ server folder
	$serverFolder = $folder + $appFolder 
	
	#Check if DayZ server folder exists
	if (!(Test-Path "$serverFolder"))
		{
			echo "DayZServer folder does not exist! Run server update before mod update."
			echo "`n"
			
		} else {
	
					#Check for files with paths to lists of mods
					if (!(Test-Path "$modListPath") -or !(Test-Path "$serverModListPath"))
						{
							#Check for file with path to list of server mods						
							if (!(Test-Path "$modListPath"))
								{
									#Prompt user to insert path to list of mods
									$modlist = Read-Host -Prompt 'Insert path to txt file with list of Steam Workshop mods (without quotation marks)'

									echo "`n"
									echo "Selected list is $modlist"
									echo "`n"
									
									#Check that list of mods exists
									if (!(Test-Path "$modlist"))
										{
											echo "Can't find $modlist !"
											echo "`n"
											
											Menu
										}

									#Prompt user to save path to list of mods for future use
									$saveList = Read-Host -Prompt 'Do you want to save path for future use? (yes/no)'

									if ( ($saveList -eq "yes") -or ($saveList -eq "y")) 
										{ 	
											#Create DayZ_Server folder if it doesn't exist
											if (!(Test-Path "$docFolder"))
												{
													mkdir "$docFolder" >$null
												}
											
											#Save path to list of mods
											$modlist | Set-Content "$modListPath"
											
											echo "Path saved to $modListPath"
											echo "`n"
										}
								
									#Load list of mods from file
									$script:loadMods = Get-Content "$modlist"
								}
						
							#Check for file with path to list of server mods						
							if (!(Test-Path "$serverModListPath"))
								{
									#Prompt user to insert path to list of server mods
									$serverModList = Read-Host -Prompt 'Insert path to txt file with list of Steam Workshop server mods (without quotation marks)'

									echo "`n"
									echo "Selected list is $serverModList"
									echo "`n"
									
									#Check that list of server mods exists
									if (!(Test-Path "$serverModList"))
										{
											echo "Can't find $serverModList !"
											echo "`n"
											
											Menu
										}

									#Prompt user to save path to list of server mods for future use
									$saveList = Read-Host -Prompt 'Do you want to save path for future use? (yes/no)'

									if ( ($saveList -eq "yes") -or ($saveList -eq "y")) 
										{ 	
											#Create DayZ_Server folder if it doesn't exist
											if (!(Test-Path "$docFolder"))
												{
													mkdir "$docFolder" >$null
												}
											
											#Save path to list of server mods
											$serverModList | Set-Content "$serverModListPath"
											
											echo "Path saved to $serverModListPath"
											echo "`n"
										}
										
									#Load list of server mods from file
									$script:loadServerMods = Get-Content "$serverModList"
								}
						
						} else {
									#Load lists of mods and server mods from files
									$modlist = Get-Content "$modListPath"
									$serverModList = Get-Content "$serverModListPath"
									
									#Check that lists of mods exists
									if (!(Test-Path "$modlist"))
										{
											echo "Can't find mod list $modlist !"
											echo "`n"
											
											Menu
										} elseif (!(Test-Path "$serverModList"))
												{
													echo "Can't find server mod list $serverModList !"
													echo "`n"
													
													Menu
												}
									
									$script:loadMods = Get-Content "$modlist"
									$script:loadServerMods = Get-Content "$serverModList"
											
									echo "Using stored lists $modlist and $serverModList"
									echo "`n"
											
									#Check that at least one mode exists in one of the lists
									if ((!$loadMods) -and (!$loadServerMods))
										{
											echo "Both lists are empty! Add at least one mod to one of the lists!"
											echo "`n"
													
											Menu
										}
								}
					
					$mods = @()
					$wrongId = @()
					$serverMods = @()
					$wrongServerId = @()
					
					#Create lists of correct and wrong format ids
					#For mods
					if ($loadMods)
						{
							ForEach ($mod in $loadMods) 
								{
									#Regex check for 8+ characters long decimal string which is most likely correct DayZ mod id
									if (($mod -notmatch "[a-zA-Z]") -and ($mod -match "\d{8,}")) 
										{
											$mods += $mod
											
										#Regex check for lines that start with # which serve as comments
										} elseif ($mod -match "^[#].*$") 
												{
													#Ignore comments and do nothing
												
												#Other lines are presumed as wrong format id
												} else {
															$wrongId += $mod
													
														}
								}
						}
					
					#For server mods					
					if ($loadServerMods)
						{
							ForEach ($serverMod in $loadServerMods) 
								{
									#Regex check for 8+ characters long decimal string which is most likely correct DayZ mod id
									if (($serverMod -notmatch "[a-zA-Z]") -and ($serverMod -match "\d{8,}")) 
										{
											$serverMods += $serverMod
											
										#Regex check for lines that start with # which serve as comments
										} elseif ($serverMod -match "^[#].*$") 
												{
													#Ignore comments and do nothing
												
												#Other lines are presumed as wrong format id
												} else {
															$wrongServerId += $serverMod
													
														}
								}
						}
					
					#List wrong format ids
					echo "Following mod ids have wrong format!"
					echo "`n"
					echo "Mods:"
					echo $wrongId
					echo "`n"
					echo "Server mods:"
					echo $wrongServerId
					echo "`n"

					#List correct format ids
					echo "Following mod ids will be used for update:"
					echo "`n"
					echo "Mods:"
					echo $mods
					echo "`n"
					echo "Server mods:"
					echo $serverMods
					echo "`n"

					#Path to SteamCMD DayZ Workshop content folder 
					$workshopFolder = $folder + '\steamapps\workshop\content\221100' 
					
					#Count correct mod ids
					$modCount = $mods.Count
					$serverModCount = $serverMods.Count

					$count = 0 
					$serverCount = 0 

					$updateMods = $null 
					$updateServerMods = $null

                    #Temporary command queues for SteamCMD
                    $tempList = $null
                    $tempListServer = $null
					
					#Download mods from the list
					if ($loadMods)
						{
                            #Generate command queue for SteamCMD
                            foreach ($mod in $mods)
								{ 
									$count++

                                    if ($count -eq $modCount)
			                            {

                                            $tempList += "workshop_download_item 221100 " + $mod + " validate`r`n" + "quit"

                                        } else {
                                                            
                                                    $tempList += "workshop_download_item 221100 " + $mod + " validate`r`n"

                                                }
								}
                            
                            #Save command queue to temporary file
                            $tempList | Set-Content "$tempModList" -Force


                            echo "Starting download of $modCount mods..."
							echo "`n"

                            #Login to SteamCMD and download/update selected mods
							Start-Process -FilePath "$folder\steamcmd.exe" -ArgumentList ('+login',$steamUs,$steamPw,'+runscript ',"$tempModList") -Wait -NoNewWindow 
									
							sleep -Seconds 1

                            Remove-Item -Path "$tempModList" -Force

						}
                        					
					#Copy downloaded mods to server folder if all previous downloads were succesfull
					if (!((Get-ChildItem $workshopFolder | Measure-Object).Count -eq 0))
						{ 
							
							#Copy mods from workshop folder to DayZ server folder
                            echo "`n"
							echo "Copying mods to DayZ server folder..."
							echo "`n"
							
							robocopy "$workshopFolder" "$serverFolder" /E /is /it /np /njs /njh /ns /nc /ndl /nfl
							
							#Copy mod bikeys from mod keys folders to server keys folder
							foreach ($mod in $mods)
								{
									Copy-Item "$serverFolder\$mod\keys\*.bikey" -Destination "$serverFolder\keys\"
								}
							
							echo "Selected mods were copied to DayZ server folder"
							echo "`n"
							
							#Check if list of mods for launch parameter exist
							if (!(Test-Path "$modServerPar"))
								{
									New-Item -Path "$docFolder" -Name "modServerPar.txt" -ItemType file >$null
								}
								
							#Clear old list of mods for launch parameter
							Clear-Content "$modServerPar"
							
							#Create new list of mods for launch parameter
							ForEach ($mod in $mods) 
								{
									[IO.File]::AppendAllText("$modServerPar", "$mod;") >$null
								}
						} 

					#Download Server mods from the list
					if ($loadServerMods)
						{
							foreach ($serverMod in $serverMods)
								{ 
									$serverCount++

                                    if ($serverCount -eq $serverModCount)
			                            {

                                            $tempListServer += "workshop_download_item 221100 " + $serverMod + " validate`r`n" + "quit"

                                        } else {
                                                            
                                                    $tempListServer += "workshop_download_item 221100 " + $serverMod + " validate`r`n"

                                                }
								}

                            #Save command queue to temporary file
                            $tempListServer | Set-Content "$tempModListServer" -Force


                            echo "Starting download of $serverModCount server mods..."
							echo "`n"

							#Login to SteamCMD and download/update selected server mods
							Start-Process -FilePath "$folder\steamcmd.exe" -ArgumentList ('+login',$steamUs,$steamPw,'+runscript ',"$tempModListServer") -Wait -NoNewWindow 
									
							sleep -Seconds 1 

                            Remove-Item -Path "$tempModListServer" -Force

						}
						
					#Copy downloaded server mods to server folder if all previous downloads were succesfull
					if (!((Get-ChildItem $workshopFolder | Measure-Object).Count -eq 0))
						{ 
							
							#Copy server mods from workshop folder to DayZ server folder
                            echo "`n"
							echo "Copying server mods to DayZ server folder..."
							echo "`n"
							
							robocopy "$workshopFolder" "$serverFolder" /E /is /it /np /njs /njh /ns /nc /ndl /nfl
							
							#Copy mod bikeys from mod keys folders to server keys folder
							foreach ($serverMod in $serverMods)
								{
									Copy-Item "$serverFolder\$serverMod\keys\*.bikey" -Destination "$serverFolder\keys\"
								}
							
							echo "Selected server mods were copied to DayZ server folder"
							echo "`n"
							
							#Check if list of server mods for launch parameter exist
							if (!(Test-Path "$serverModServerPar"))
								{
									New-Item -Path "$docFolder" -Name "serverModServerPar.txt" -ItemType file >$null
								}
								
							#Clear old list of server mods for launch parameter
							Clear-Content "$serverModServerPar"
							
							#Create new list of server mods for launch parameter
							ForEach ($serverMod in $serverMods) 
								{
									[IO.File]::AppendAllText("$serverModServerPar", "$serverMod;") >$null
								}
						}

                    $script:steamUs = $null
					$script:steamPw = $null 

				}
}

#Run DayZ server with mods
function Server_menu {

	#Reload file with path to launch parameters in case it was manually changed without script restart
	$userServerParPath = $docFolder + '\userServerParPath.txt'
	
	#Path to server folder
	$serverFolder = $folder + $appFolder
	
	#Prepare empty variables for lists of mod ids
	$modsServer = $null
	$serverModsServer = $null
	
	#Check if list of mods for launch parameter exist
	if (Test-Path "$modServerPar")
		{
			#Get list of mod ids for -mod= launch parameter
			$modsServer = Get-Content "$modServerPar" -Raw
		}
		
	if (Test-Path "$serverModServerPar")
		{
			#Get list of mod ids for -serverMod= launch parameter
			$serverModsServer = Get-Content "$serverModServerPar" -Raw
		}
		
	#Check if DayZ server exe exists
	if (!(Test-Path "$serverFolder"))
		{
			echo "DayZServer folder does not exist in $serverFolder ! Run server update to download/repair server data."
			echo "`n"
			
		} else {
	
                    switch ($select)
                        {
                            #Start server menu
                            $null {
                                        echo "Start server menu:"
							            echo "1) Use user launch parameters"
							            echo "2) Use default launch parameters"
							            echo "3) Return to previous menu"
							            echo "`n"

							            $select = Read-Host -Prompt 'Please select desired action from menu above'

                                        Server_menu

                                        Break
                                }
                            
                            #Use user provided server parameters
                            1 {
                                    echo "`n"
							        echo "User launch parameters selected"
							        echo "`n"
							
							        #Check for file with user server launch parameters
							        if (!(Test-Path "$userServerParPath"))
								        {
									        #Prompt user to insert path to file with user server launch parameters
									        $serverParPath = Read-Host -Prompt 'Insert path to file with user launch parameters (without quotation marks)'

									        echo "`n"
									        echo "Selected file is $serverParPath"
									        echo "`n"
									
									        #Check that file with launch parameters exists
									        if (!(Test-Path "$serverParPath"))
										        {
											        echo "Can't find $serverParPath !"
											        echo "`n"
											
											        Menu
										        }

									        #Prompt user to save path to file with user server launch parameters for future use
									        $savePath = Read-Host -Prompt 'Do you want to save path for future use? (yes/no)'

									        if ( ($savePath -eq "yes") -or ($savePath -eq "y")) 
										        { 	
											        #Create DayZ_Server folder if it doesn't exist
											        if (!(Test-Path "$docFolder"))
												        {
													        mkdir "$docFolder" >$null
												        }
											
											        #Save path to file with user server launch parameters
											        $serverParPath | Set-Content "$userServerParPath"
											
											        echo "`n"
											        echo "Path saved to $userServerParPath"
											        echo "`n"
										        }
								        } else {
											        #Use saved path to file with user server launch parameters
											        $serverParPath = Get-Content "$userServerParPath"
											
											        echo "Selected file with user launch parameters is $serverParPath"
											        echo "`n"
											
										        }
								
								        #Load user server launch parameters
								        $serverPar = Get-Content "$serverParPath" -Raw
								
								        #Check if user server launch parameters were properly loaded
								        if (!$serverPar)
								        {
									        echo "Server launch parameter file is empty or wasn't loaded properly!"
									        echo "`n"
									
									        #Return to Main menu if it wasn't started from CMD			
									        if (($s -eq "") -and ($server -eq "")) 
										        { 
											        $select = $null

											        return
										        }
										
									        exit 0
								        }
								
								        echo "Launching DayZ server with user launch parameters..."
								        echo "`n"
									
								        #Run server
								        $procServer = Start-Process -FilePath "$serverFolder\DayZServer_x64.exe" -PassThru -ArgumentList "`"-bepath=$serverFolder\battleye`" $serverPar"
										
								        #Save server PID for future use
								        $procServer.id | Add-Content "$pidServer"
										
								        sleep -Seconds 5	
										
								        echo "DayZ server is up and running..."
								        echo "`n"

                                        Break
                                }
                            
                            #Use default server parameters
                            2 {
                                    echo "`n"
									echo "Default launch parameters selected"
									echo "`n"
										
									echo "Launching DayZ server with default launch parameters..."
									echo "`n"

									#Run server
									$procServer = Start-Process -FilePath "$serverFolder\DayZServer_x64.exe" -PassThru -ArgumentList "`"-config=$serverFolder\serverDZ.cfg`" `"-mod=$modsServer`" `"-serverMod=$serverModsServer`" `"-bepath=$serverFolder\battleye`" `"-profiles=$serverFolder\logs`" -port=2302 -freezecheck -adminlog -dologs"
										
									#Save server PID for future use
									$procServer.id | Add-Content "$pidServer"
										
									sleep -Seconds 5	
										
									echo "DayZ server is up and running..."
									echo "`n"

                                    Break
                                }

                            #Return to previous menu
                            3 {
                                    Menu

                                    Break
                                }
                            
                            #Force user to select one of provided options
                            Default {
                                        echo "`n"
										echo "Select number from provided list (1-3)"
										echo "`n"
															
										$select = $null
															
										Server_menu
                                }
                        }
				}               
}

#Stop running DayZ server
function ServerStop {
	
	#Get previously started DayZ server PIDs from the list
	$loadPID = Get-Content "$pidServer"
	
	#Check if PID list is not empty
	if (!$loadPID)
		{
			echo "There is no process ID in list! No DayZ server instance is running or it wasn't started by this script."
			echo "`n"
			
		} else {
					#Try every process id in list
					foreach ($proc in $loadPID)
						{
							#Get process id of DayZ server instance
							$killServer = Get-Process -Id $proc 2>$null
							
							#Check for running DayZ server instance
							if (!$killServer)
								{
									echo "DayZ server instance with PID $proc is not running!"
									echo "`n"
								
								#Kill server
								} else { 
											echo "DayZ server with PID $proc found, commencing shutdown..."
											echo "`n"
									
											#Gracefull exit
											$killServer.CloseMainWindow() >$null
											
											#Force exit after five seconds
											Sleep -Seconds 5
											
											if (!$killServer.HasExited)
												{
													$killServer | Stop-Process -Force
													
													echo "DayZ server with PID $proc was forcefully turned off"
													echo "`n"
													
												}
												
											echo "DayZ server with PID $proc was turned off"
											echo "`n"
											
										}
						}
					
					#Clear PID list
					Clear-Content "$pidServer" -Force	
				}
}

#Uninstall DayZ server
function ServerUninstall {
	
	echo "Uninstalling DayZ server now..."
	echo "`n"

    $serverFolder = $folder + $appFolder
														
	#Uninstall DayZ server
	Start-Process -FilePath "$folder\steamcmd.exe" -ArgumentList ('+app_uninstall -complete ',$steamApp,'+quit') -Wait -NoNewWindow 
																											
	sleep -Seconds 1
    
    #Check if server was deleted and if not removed it forcefully
    if (Test-Path "$serverFolder")
        {
            Remove-Item -Path "$serverFolder" -Recurse -Force
        }
	
    if (Test-Path "$serverFolder")
        {   																																				
	        echo "`n"
	        echo "DayZ server uninstallation was unsuccessful"
	        echo "`n"

        } else {
                    echo "`n"
	                echo "DayZ server was succesfully uninstalled"
	                echo "`n"

                }
}

#Uninstall/remove DayZ Server/saved info
function Remove_menu {

	echo "Remove menu:"
	echo "1) Remove Steam login"
	echo "2) Remove path to SteamCMD folder"
	echo "3) Remove path to mod list file"
	echo "4) Remove mod"
	echo "5) Remove path to user launch parameters file"
	echo "6) Uninstall DayZ server"
	echo "7) Uninstall SteamCMD"
	echo "8) Return to previous menu"
	echo "`n"

	$select = Read-Host -Prompt 'Please select desired action from menu above'
	
    switch ($select)
        {
            #Remove encrypted Steam login files
            1 {
                    echo "`n"
			        echo "Remove Steam login selected"
			        echo "`n"
			
			        #Path to encrypted Steam login files
			        Remove-Item "$docFolder\SteamLog*.txt"
			
			        echo "Stored Steam login was removed"
			        echo "`n"
			
			        Remove_menu

                    Break
            }

            #Remove stored path to SteamCMD folder
            2 {
                    echo "`n"
					echo "Remove path to SteamCMD folder selected"
					echo "`n"
						
					#Path to file with stored path to SteamCMD folder
					Remove-Item "$docFolder\SteamCmdPath.txt"
						
					echo "Stored path to SteamCMD folder was removed"
					echo "`n"
						
					Remove_menu

                    Break
            }

            #Remove stored path to mod list file
            3 {
                    echo "`n"
					echo "Remove path to mod list file selected"
					echo "`n"
								
					echo "Remove mod list menu:"
					echo "1) Remove mod list"
					echo "2) Remove server mod list"
					echo "3) Remove both mod and server mod lists"
					echo "4) Return to previous menu"
					echo "`n"
								
					#Prompt user for mod list selection
					$rem_list = Read-Host -Prompt 'Please select desired action from menu above'
																
					echo "`n"	
														
					if ($rem_list -eq '1') 
						{ 	
							if (Test-Path "$docFolder\modListPath.txt")
								{
									#Path to file with stored path to mod list file
									Remove-Item "$docFolder\modListPath.txt"
								}
											
							echo "Stored path to mod list file was removed"
							echo "`n"
										
						} elseif ($rem_list -eq '2')
									{
										if (Test-Path "$docFolder\serverModListPath.txt")
										{
											#Path to file with stored path to server mod list file
											Remove-Item "$docFolder\serverModListPath.txt"
										}
													
										echo "Stored path to server mod list file was removed"
										echo "`n"
										
									} elseif ($rem_list -eq '3')
												{
													#Files with paths to both mod and server mod file lists
													if (Test-Path "$docFolder\modListPath.txt")
														{
															#Path to file with stored path to mod list file
															Remove-Item "$docFolder\modListPath.txt"
														}
																
													if (Test-Path "$docFolder\serverModListPath.txt")
														{
															#Path to file with stored path to server mod list file
															Remove-Item "$docFolder\serverModListPath.txt"
														}
																
													echo "Stored paths to mod and server mod list files were removed"
													echo "`n"
																
												} elseif ($rem_list -eq '4') 
														{ 
															#Return to previous menu
															Remove_menu
																		
														}
								
					Remove_menu

                    Break
            }

            #Select mod and remove it
            4 {
                    $reminder = $false
                    
                    echo "`n"
					echo "Remove mod selected"
					echo "`n"
										
					SteamCMDFolder
										
					#Path to SteamCMD DayZ Workshop content folder 
					$workshopFolder = $folder + '\steamapps\workshop\content\221100' 

					#Path to DayZ server folder
					$serverFolder = $folder + $appFolder
										
					#Prompt user to insert path to SteamCMD folder
					$rem_mod = Read-Host -Prompt 'Insert mod id you wish to remove'
										
					#Check if mod id was really inserted
					if ($rem_mod -eq "")
						{
							echo "`n"
							echo "No mod id inserted! Returning to Remove menu..."
							echo "`n"
												
							Remove_menu
						}
										
					echo "`n"
										
					#Check if selected mod folder exist in workshop folder
					if (!(Test-Path "$workshopFolder\$rem_mod"))
						{
							echo "Selected mod folder doesn't exist in $workshopFolder !"
							echo "`n"
												
						} else { 
									#Remove selected mod folder from workshop folder
									Remove-Item -LiteralPath "$workshopFolder\$rem_mod" -Force -Recurse
														
									echo "Selected mod folder was removed from $workshopFolder"
									echo "`n"

                                    $reminder = $true
								}
													
					#Check if selected mod folder exist in DayZ server folder
					if (!(Test-Path "$serverFolder\$rem_mod"))
						{
							echo "Selected mod folder doesn't exist in $serverFolder !"
							echo "`n"
												
						} else { 
									#Remove selected mod folder from DayZ server folder
									Remove-Item -LiteralPath "$serverFolder\$rem_mod" -Force -Recurse
														
									echo "Selected mod folder was removed from $serverFolder"
									echo "`n"

                                    $reminder =  $true
								}
										
					#Remove selected mod id from mod and server mode lists
					if (Test-Path "$modServerPar")
						{
							$loadModList = Get-Content "$modServerPar" | % {$_ -replace "($rem_mod;)",""}
							$loadModList | Set-Content "$modServerPar"
												
						} 
											
					if (Test-Path "$serverModServerPar")
						{ 
							$loadServerModList = Get-Content "$serverModServerPar" | % {$_ -replace "($rem_mod;)",""}
							$loadServerModList | Set-Content "$serverModServerPar"
						}
					
					if ($reminder)		
						{ 
							echo "Don't forget to remove $rem_mod also from your list of mods/server mods in case you don't want to use it anymore!"
							echo "`n"
						}
										
					Remove_menu

                    Break
            }

            #Remove stored path to user launch parameters file
            5 {
                    echo "`n"
					echo "Remove path to user launch parameters file selected"
					echo "`n"
								
					#Path to file with stored path to mod list file
					Remove-Item "$docFolder\userServerParPath.txt"
												
					echo "Stored path to user launch parameters file was removed"
					echo "`n"
												
					Remove_menu

                    Break
            }

            #Uninstall DayZ server
            6 {
                    echo "`n"
					echo "Uninstall DayZ server selected"
					echo "`n"
														
					#Prompt user for DayZ server uninstall confirmation
					$rem_server = Read-Host -Prompt 'Are you sure you want to uninstall DayZ server? (yes/no)'
														
					echo "`n"	
														
					if ( ($rem_server -eq "yes") -or ($rem_server -eq "y")) 
						{ 	
							SteamCMDFolder
							SteamCMDExe
							ServerUninstall
																
						}
														
					Remove_menu

                    Break
            }

            #Uninstall SteamCMD
            7 {
                    echo "`n"
					echo "Uninstall SteamCMD selected"
					echo "`n"
																
					#Prompt user for SteamCMD uninstall confirmation
					$rem_server = Read-Host -Prompt 'Are you sure you want to uninstall SteamCMD? This option will also uninstall DayZ server and remove all its data! (yes/no)'
																
					echo "`n"	
														
					if ( ($rem_server -eq "yes") -or ($rem_server -eq "y")) 
						{ 	
							SteamCMDFolder
							SteamCMDExe
							ServerUninstall
																		
							echo "Uninstalling SteamCMD now..."
							echo "`n"
																		
							Remove-Item -LiteralPath "$folder" -Force -Recurse
																		
							echo "SteamCMD was succesfully uninstalled"
							echo "`n"
																		
						}
																
					#Prompt user for Documents folder removal confirmation
					$rem_mod = Read-Host -Prompt 'Do you want to remove Documents folder which contains all saved folder/exe paths, mod and SteamCMD login info from Documents? (yes/no)'
																
					echo "`n"	
														
					if ( ($rem_mod -eq "yes") -or ($rem_mod -eq "y")) 
						{ 	
							echo "Removing Documents folder now..."
							echo "`n"
																		
							Remove-Item -LiteralPath "$docFolder" -Force -Recurse
																		
							echo "Folder was succesfully removed"
							echo "`n"
																		
						}
																
					Remove_menu

                    Break
            }

            #Return to previous menu
            8 {
                    Menu

                    Break
            }

            #Force user to select one of provided options
            Default {
                        echo "`n"
						echo "Select number from provided list (1-7)"
						echo "`n"
																				
						Remove_menu
            }

        }

}

#When launch parameters are used
#Parameters are described in readme.txt
function CMD {
	
	#Prepare variables for correct parameter value check
	$paramCheckUpdate = $false
	$paramCheckServer = $false
	
	echo "`n"
	echo "Launch parameters are being used."

    #Set Steam app id and server folder name
	if ($app -eq "exp") 
		{ 
            echo "`n"
			echo "Experimental server management selected"
			echo "`n"
                    
            #Set Experimental app id
            $steamApp = 1042420
                    
            #Set Experimental app folder
            $appFolder = '\steamapps\common\DayZ Server Exp'

        } else {

                    echo "`n"
			        echo "Stable server management selected"
			        echo "`n"
                    
                    #Set Stable app id
                    $steamApp = 223350
                    
                    #Set Stable app folder
                    $appFolder = '\steamapps\common\DayZServer'

                }
	
	#Call server update and related functions
	if (($u -eq "server") -or ($update -eq "server")) 
		{ 
			echo "`n"
			echo "Server update selected"
			echo "`n"
			
			$select = 1
			
			SteamCMDFolder
			SteamCMDExe
			SteamLogin
				
			$paramCheckUpdate = $true
				
			
			#Call mods update and related functions		
			} elseif (($u -eq "mod") -or ($u -eq "mods") -or ($update -eq "mod") -or ($update -eq "mods"))
					{ 
						echo "`n"
						echo "Mods update selected"
						echo "`n"
						
						$select = 2
						
						SteamCMDFolder
						SteamCMDExe
						SteamLogin
							
						$paramCheckUpdate = $true
							
						
						#Call both server and mods updates 
						} elseif (($u -eq "all") -or ($update -eq "all"))
								{ 
									echo "`n"
									echo "Server + mod update selected"
									echo "`n"
									
									#Server update
									$select = 1
			
									SteamCMDFolder
									SteamCMDExe
									SteamLogin
									
									#Mods update
									$select = 2
									
									SteamLogin
									
									$paramCheckUpdate = $true
									
								}
	#Start DayZ server							
	if (($s -eq "start") -or ($server -eq "start")) 
		{ 
			echo "`n"
								
			SteamCMDFolder
			
			$paramCheckServer = $true
			
			#Check which launch parameter file to use
			#User launch parameters
			if (($lp -eq "user") -or ($launchParam -eq "user")) 
				{ 
					echo "Start server with user launch parameters selected"
					
					$select = 1
					
					Server_menu
					
					#Default launch parameters
					} else {
								echo "Start server with default launch parameters selected"
								
								$select = 2
					
								Server_menu
							}
				
			#Stop running server	
			} elseif (($s -eq "stop") -or ($server -eq "stop"))
					{ 	
						echo "`n"
						echo "Stop running server selected"
						echo "`n"
										
						ServerStop
						
						$paramCheckServer = $true

					}

	#Check for wrong launch parameter values
	if (($paramCheckUpdate -eq $false) -or ($paramCheckServer -eq $false))
		{ 
			if ((($paramCheckUpdate -eq $false) -and !($u -eq "")) -or (($paramCheckUpdate -eq $false) -and !($update -eq ""))) 
				{ 
					echo "`n"
					echo "Wrong -u/-update parameter value used! Check readme.txt or 'Get-Help .\Server_manager.ps1 -Parameter update' for correct lauch parameter values."
					echo "`n"
				}
				
			if ((($paramCheckServer -eq $false) -and !($s -eq "")) -or (($paramCheckServer -eq $false) -and !($server -eq ""))) 
				{ 
					echo "`n"
					echo "Wrong -s/-server parameter value used! Check readme.txt or 'Get-Help .\Server_manager.ps1 -Parameter server' for correct lauch parameter values."
					echo "`n"
				}
			
			exit 0
		}
			
	echo "All selected tasks are done."
	echo "`n"
	
	exit 0
}


function MainMenu {


		echo "`n"
		echo "Welcome to DayZ server/mods management app!"

        echo "`n"
	    echo "Menu:"
	    echo "1) Stable server management"
	    echo "2) Experimental server management"
        echo "3) Exit"
	    echo "`n"

	    $select = Read-Host -Prompt 'Please select desired action from menu above'
	
        switch ($select)
            {
                #Steam Stable server app
                1 {
                    echo "`n"
			        echo "Stable server app selected"
			        echo "`n"
                    
                    #Set Stable app id
                    $steamApp = 223350
                    
                    #Set Stable app folder
                    $appFolder = '\steamapps\common\DayZServer'
			
			        Menu

                    Break
                } 

                #Steam Experimental server app
                2 {
                    echo "`n"
				    echo "Experimental server app selected"
				    echo "`n"
                    
                    #Set Experimental app id
                    $steamApp = 1042420

                    #Set Experimental app folder
                    $appFolder = '\steamapps\common\DayZ Server Exp'
						
				    Menu

                    Break
                }

                #Close script
                3 {
                    echo "`n"
				    echo "Exit selected"
				    echo "`n"
														
				    exit 0

                    Break
                }

                #Force user to select one of provided options
                Default {
                            echo "`n"
						    echo "Select number from provided list (1-3)"
						    echo "`n"
																				
						    MainMenu
                }
	    }
}

#Open Main menu if launch parameters are not used
if (($u -eq "") -and ($update -eq "") -and ($s -eq "") -and ($server -eq "")) 
	{    
        MainMenu

    } else {
                #Run CMD function when launch parameters are used
                CMD

            }

exit 0
# SIG # Begin signature block
# MIIcZwYJKoZIhvcNAQcCoIIcWDCCHFQCAQExCzAJBgUrDgMCGgUAMGkGCisGAQQB
# gjcCAQSgWzBZMDQGCisGAQQBgjcCAR4wJgIDAQAABBAfzDtgWUsITrck0sYpfvNR
# AgEAAgEAAgEAAgEAAgEAMCEwCQYFKw4DAhoFAAQUJGaUFA3dh1nuwSV6iEEgPK1Z
# yQOggheRMIIE8TCCA9mgAwIBAgIQPLyHe5m6GFiJpDaKnGk42TANBgkqhkiG9w0B
# AQsFADB/MQswCQYDVQQGEwJVUzEdMBsGA1UEChMUU3ltYW50ZWMgQ29ycG9yYXRp
# b24xHzAdBgNVBAsTFlN5bWFudGVjIFRydXN0IE5ldHdvcmsxMDAuBgNVBAMTJ1N5
# bWFudGVjIENsYXNzIDMgU0hBMjU2IENvZGUgU2lnbmluZyBDQTAeFw0xOTA0MzAw
# MDAwMDBaFw0yMjA1MDcyMzU5NTlaMIGIMQswCQYDVQQGEwJDWjEZMBcGA1UECAwQ
# U3RyZWRvY2Vza3kga3JhajEYMBYGA1UEBwwPTW5pc2VrIHBvZCBCcmR5MSEwHwYD
# VQQKDBhCT0hFTUlBIElOVEVSQUNUSVZFIGEucy4xITAfBgNVBAMMGEJPSEVNSUEg
# SU5URVJBQ1RJVkUgYS5zLjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
# ALnwscZ1gIwHNKD5OAfX/6HYpkh1lfaqYiDuomVQji5IvD0dsPqdiCN9+4AuI7wF
# og05Qp/dFpvEmF6E0WiP+nw6dt7wnoQ4tipZKkHSw7SJkp4zlQxAqvMGwd5x6RMP
# cLjEKA8CEadG1dM3+x7Evm27QxbEwGYSE45Qz0DBYDQoD9njyvA83DQGXpbxR69K
# vFRW8xcTFnVshYvLRx9EurrakweWYtIv1DGFfZKwqpx+DYHemztGVAlQWDo8yCcq
# 6wIOU8xi4NMsYpiIgGxUhG1nriS2DKXPRcVpldF0lJdfh7lSS+Wb4L/JQAqt47pD
# DmD1AjHc6FGpDFzsBnrfjP0CAwEAAaOCAV0wggFZMAkGA1UdEwQCMAAwDgYDVR0P
# AQH/BAQDAgeAMCsGA1UdHwQkMCIwIKAeoByGGmh0dHA6Ly9zdi5zeW1jYi5jb20v
# c3YuY3JsMGEGA1UdIARaMFgwVgYGZ4EMAQQBMEwwIwYIKwYBBQUHAgEWF2h0dHBz
# Oi8vZC5zeW1jYi5jb20vY3BzMCUGCCsGAQUFBwICMBkMF2h0dHBzOi8vZC5zeW1j
# Yi5jb20vcnBhMBMGA1UdJQQMMAoGCCsGAQUFBwMDMFcGCCsGAQUFBwEBBEswSTAf
# BggrBgEFBQcwAYYTaHR0cDovL3N2LnN5bWNkLmNvbTAmBggrBgEFBQcwAoYaaHR0
# cDovL3N2LnN5bWNiLmNvbS9zdi5jcnQwHwYDVR0jBBgwFoAUljtT8Hkzl699g+8u
# K8zKt4YecmYwHQYDVR0OBBYEFMa2/MDoNhLIzM6lAKuSUC9oHzgZMA0GCSqGSIb3
# DQEBCwUAA4IBAQBf2J8DPInPPgYsJgtd8S20hrsO2HAdJHBX5UwPwp0XdL2X25G2
# 50qdUgmWYHnPa0nmVW7q+oRJ9rJFKar2uQlbnBA2hh2tatG8EjPJGT7Si2IEy5aP
# QO/eStKX5sNxufChKfEgF4TUAWch/yJkJH6JX2QNWKaWtZvxyYQefqjFwO7xY90e
# dcDkIWEUfWkUGEJiT5T5HlS4VLXPzd6pc2sUn2LGq5be3SU/HTsZ/5gWFG1XQoMD
# lUoXGks9q5TjqO8mrWZcEEq3TBTZEFyYkVBN2kaSCN8EBcetZIsv8Q9AtBYBbsHn
# 8yYsWSfU6ZfbHQsdnBE4/GFppwPb+5G8d8m6MIIFWTCCBEGgAwIBAgIQPXjX+XZJ
# YLJhffTwHsqGKjANBgkqhkiG9w0BAQsFADCByjELMAkGA1UEBhMCVVMxFzAVBgNV
# BAoTDlZlcmlTaWduLCBJbmMuMR8wHQYDVQQLExZWZXJpU2lnbiBUcnVzdCBOZXR3
# b3JrMTowOAYDVQQLEzEoYykgMjAwNiBWZXJpU2lnbiwgSW5jLiAtIEZvciBhdXRo
# b3JpemVkIHVzZSBvbmx5MUUwQwYDVQQDEzxWZXJpU2lnbiBDbGFzcyAzIFB1Ymxp
# YyBQcmltYXJ5IENlcnRpZmljYXRpb24gQXV0aG9yaXR5IC0gRzUwHhcNMTMxMjEw
# MDAwMDAwWhcNMjMxMjA5MjM1OTU5WjB/MQswCQYDVQQGEwJVUzEdMBsGA1UEChMU
# U3ltYW50ZWMgQ29ycG9yYXRpb24xHzAdBgNVBAsTFlN5bWFudGVjIFRydXN0IE5l
# dHdvcmsxMDAuBgNVBAMTJ1N5bWFudGVjIENsYXNzIDMgU0hBMjU2IENvZGUgU2ln
# bmluZyBDQTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJeDHgAWryyx
# 0gjE12iTUWAecfbiR7TbWE0jYmq0v1obUfejDRh3aLvYNqsvIVDanvPnXydOC8KX
# yAlwk6naXA1OpA2RoLTsFM6RclQuzqPbROlSGz9BPMpK5KrA6DmrU8wh0MzPf5vm
# wsxYaoIV7j02zxzFlwckjvF7vjEtPW7ctZlCn0thlV8ccO4XfduL5WGJeMdoG68R
# eBqYrsRVR1PZszLWoQ5GQMWXkorRU6eZW4U1V9Pqk2JhIArHMHckEU1ig7a6e2iC
# Me5lyt/51Y2yNdyMK29qclxghJzyDJRewFZSAEjM0/ilfd4v1xPkOKiE1Ua4E4bC
# G53qWjjdm9sCAwEAAaOCAYMwggF/MC8GCCsGAQUFBwEBBCMwITAfBggrBgEFBQcw
# AYYTaHR0cDovL3MyLnN5bWNiLmNvbTASBgNVHRMBAf8ECDAGAQH/AgEAMGwGA1Ud
# IARlMGMwYQYLYIZIAYb4RQEHFwMwUjAmBggrBgEFBQcCARYaaHR0cDovL3d3dy5z
# eW1hdXRoLmNvbS9jcHMwKAYIKwYBBQUHAgIwHBoaaHR0cDovL3d3dy5zeW1hdXRo
# LmNvbS9ycGEwMAYDVR0fBCkwJzAloCOgIYYfaHR0cDovL3MxLnN5bWNiLmNvbS9w
# Y2EzLWc1LmNybDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYBBQUHAwMwDgYDVR0P
# AQH/BAQDAgEGMCkGA1UdEQQiMCCkHjAcMRowGAYDVQQDExFTeW1hbnRlY1BLSS0x
# LTU2NzAdBgNVHQ4EFgQUljtT8Hkzl699g+8uK8zKt4YecmYwHwYDVR0jBBgwFoAU
# f9Nlp8Ld7LvwMAnzQzn6Aq8zMTMwDQYJKoZIhvcNAQELBQADggEBABOFGh5pqTf3
# oL2kr34dYVP+nYxeDKZ1HngXI9397BoDVTn7cZXHZVqnjjDSRFph23Bv2iEFwi5z
# uknx0ZP+XcnNXgPgiZ4/dB7X9ziLqdbPuzUvM1ioklbRyE07guZ5hBb8KLCxR/Md
# oj7uh9mmf6RWpT+thC4p3ny8qKqjPQQB6rqTog5QIikXTIfkOhFf1qQliZsFay+0
# yQFMJ3sLrBkFIqBgFT/ayftNTI/7cmd3/SeUx7o1DohJ/o39KK9KEr0Ns5cF3kQM
# Ffo2KwPcwVAB8aERXRTl4r0nS1S+K4ReD6bDdAUK75fDiSKxH3fzvc1D1PFMqT+1
# i4SvZPLQFCEwggZqMIIFUqADAgECAhADAZoCOv9YsWvW1ermF/BmMA0GCSqGSIb3
# DQEBBQUAMGIxCzAJBgNVBAYTAlVTMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAX
# BgNVBAsTEHd3dy5kaWdpY2VydC5jb20xITAfBgNVBAMTGERpZ2lDZXJ0IEFzc3Vy
# ZWQgSUQgQ0EtMTAeFw0xNDEwMjIwMDAwMDBaFw0yNDEwMjIwMDAwMDBaMEcxCzAJ
# BgNVBAYTAlVTMREwDwYDVQQKEwhEaWdpQ2VydDElMCMGA1UEAxMcRGlnaUNlcnQg
# VGltZXN0YW1wIFJlc3BvbmRlcjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
# ggEBAKNkXfx8s+CCNeDg9sYq5kl1O8xu4FOpnx9kWeZ8a39rjJ1V+JLjntVaY1sC
# SVDZg85vZu7dy4XpX6X51Id0iEQ7Gcnl9ZGfxhQ5rCTqqEsskYnMXij0ZLZQt/US
# s3OWCmejvmGfrvP9Enh1DqZbFP1FI46GRFV9GIYFjFWHeUhG98oOjafeTl/iqLYt
# WQJhiGFyGGi5uHzu5uc0LzF3gTAfuzYBje8n4/ea8EwxZI3j6/oZh6h+z+yMDDZb
# esF6uHjHyQYuRhDIjegEYNu8c3T6Ttj+qkDxss5wRoPp2kChWTrZFQlXmVYwk/PJ
# YczQCMxr7GJCkawCwO+k8IkRj3cCAwEAAaOCAzUwggMxMA4GA1UdDwEB/wQEAwIH
# gDAMBgNVHRMBAf8EAjAAMBYGA1UdJQEB/wQMMAoGCCsGAQUFBwMIMIIBvwYDVR0g
# BIIBtjCCAbIwggGhBglghkgBhv1sBwEwggGSMCgGCCsGAQUFBwIBFhxodHRwczov
# L3d3dy5kaWdpY2VydC5jb20vQ1BTMIIBZAYIKwYBBQUHAgIwggFWHoIBUgBBAG4A
# eQAgAHUAcwBlACAAbwBmACAAdABoAGkAcwAgAEMAZQByAHQAaQBmAGkAYwBhAHQA
# ZQAgAGMAbwBuAHMAdABpAHQAdQB0AGUAcwAgAGEAYwBjAGUAcAB0AGEAbgBjAGUA
# IABvAGYAIAB0AGgAZQAgAEQAaQBnAGkAQwBlAHIAdAAgAEMAUAAvAEMAUABTACAA
# YQBuAGQAIAB0AGgAZQAgAFIAZQBsAHkAaQBuAGcAIABQAGEAcgB0AHkAIABBAGcA
# cgBlAGUAbQBlAG4AdAAgAHcAaABpAGMAaAAgAGwAaQBtAGkAdAAgAGwAaQBhAGIA
# aQBsAGkAdAB5ACAAYQBuAGQAIABhAHIAZQAgAGkAbgBjAG8AcgBwAG8AcgBhAHQA
# ZQBkACAAaABlAHIAZQBpAG4AIABiAHkAIAByAGUAZgBlAHIAZQBuAGMAZQAuMAsG
# CWCGSAGG/WwDFTAfBgNVHSMEGDAWgBQVABIrE5iymQftHt+ivlcNK2cCzTAdBgNV
# HQ4EFgQUYVpNJLZJMp1KKnkag0v0HonByn0wfQYDVR0fBHYwdDA4oDagNIYyaHR0
# cDovL2NybDMuZGlnaWNlcnQuY29tL0RpZ2lDZXJ0QXNzdXJlZElEQ0EtMS5jcmww
# OKA2oDSGMmh0dHA6Ly9jcmw0LmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydEFzc3VyZWRJ
# RENBLTEuY3JsMHcGCCsGAQUFBwEBBGswaTAkBggrBgEFBQcwAYYYaHR0cDovL29j
# c3AuZGlnaWNlcnQuY29tMEEGCCsGAQUFBzAChjVodHRwOi8vY2FjZXJ0cy5kaWdp
# Y2VydC5jb20vRGlnaUNlcnRBc3N1cmVkSURDQS0xLmNydDANBgkqhkiG9w0BAQUF
# AAOCAQEAnSV+GzNNsiaBXJuGziMgD4CH5Yj//7HUaiwx7ToXGXEXzakbvFoWOQCd
# 42yE5FpA+94GAYw3+puxnSR+/iCkV61bt5qwYCbqaVchXTQvH3Gwg5QZBWs1kBCg
# e5fH9j/n4hFBpr1i2fAnPTgdKG86Ugnw7HBi02JLsOBzppLA044x2C/jbRcTBu7k
# A7YUq/OPQ6dxnSHdFMoVXZJB2vkPgdGZdA0mxA5/G7X1oPHGdwYoFenYk+VVFvC7
# Cqsc21xIJ2bIo4sKHOWV2q7ELlmgYd3a822iYemKC23sEhi991VUQAOSK2vCUcIK
# SK+w1G7g9BQKOhvjjz3Kr2qNe9zYRDCCBs0wggW1oAMCAQICEAb9+QOWA63qAArr
# Pye7uhswDQYJKoZIhvcNAQEFBQAwZTELMAkGA1UEBhMCVVMxFTATBgNVBAoTDERp
# Z2lDZXJ0IEluYzEZMBcGA1UECxMQd3d3LmRpZ2ljZXJ0LmNvbTEkMCIGA1UEAxMb
# RGlnaUNlcnQgQXNzdXJlZCBJRCBSb290IENBMB4XDTA2MTExMDAwMDAwMFoXDTIx
# MTExMDAwMDAwMFowYjELMAkGA1UEBhMCVVMxFTATBgNVBAoTDERpZ2lDZXJ0IElu
# YzEZMBcGA1UECxMQd3d3LmRpZ2ljZXJ0LmNvbTEhMB8GA1UEAxMYRGlnaUNlcnQg
# QXNzdXJlZCBJRCBDQS0xMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
# 6IItmfnKwkKVpYBzQHDSnlZUXKnE0kEGj8kz/E1FkVyBn+0snPgWWd+etSQVwpi5
# tHdJ3InECtqvy15r7a2wcTHrzzpADEZNk+yLejYIA6sMNP4YSYL+x8cxSIB8HqIP
# kg5QycaH6zY/2DDD/6b3+6LNb3Mj/qxWBZDwMiEWicZwiPkFl32jx0PdAug7Pe2x
# QaPtP77blUjE7h6z8rwMK5nQxl0SQoHhg26Ccz8mSxSQrllmCsSNvtLOBq6thG9I
# hJtPQLnxTPKvmPv2zkBdXPao8S+v7Iki8msYZbHBc63X8djPHgp0XEK4aH631XcK
# J1Z8D2KkPzIUYJX9BwSiCQIDAQABo4IDejCCA3YwDgYDVR0PAQH/BAQDAgGGMDsG
# A1UdJQQ0MDIGCCsGAQUFBwMBBggrBgEFBQcDAgYIKwYBBQUHAwMGCCsGAQUFBwME
# BggrBgEFBQcDCDCCAdIGA1UdIASCAckwggHFMIIBtAYKYIZIAYb9bAABBDCCAaQw
# OgYIKwYBBQUHAgEWLmh0dHA6Ly93d3cuZGlnaWNlcnQuY29tL3NzbC1jcHMtcmVw
# b3NpdG9yeS5odG0wggFkBggrBgEFBQcCAjCCAVYeggFSAEEAbgB5ACAAdQBzAGUA
# IABvAGYAIAB0AGgAaQBzACAAQwBlAHIAdABpAGYAaQBjAGEAdABlACAAYwBvAG4A
# cwB0AGkAdAB1AHQAZQBzACAAYQBjAGMAZQBwAHQAYQBuAGMAZQAgAG8AZgAgAHQA
# aABlACAARABpAGcAaQBDAGUAcgB0ACAAQwBQAC8AQwBQAFMAIABhAG4AZAAgAHQA
# aABlACAAUgBlAGwAeQBpAG4AZwAgAFAAYQByAHQAeQAgAEEAZwByAGUAZQBtAGUA
# bgB0ACAAdwBoAGkAYwBoACAAbABpAG0AaQB0ACAAbABpAGEAYgBpAGwAaQB0AHkA
# IABhAG4AZAAgAGEAcgBlACAAaQBuAGMAbwByAHAAbwByAGEAdABlAGQAIABoAGUA
# cgBlAGkAbgAgAGIAeQAgAHIAZQBmAGUAcgBlAG4AYwBlAC4wCwYJYIZIAYb9bAMV
# MBIGA1UdEwEB/wQIMAYBAf8CAQAweQYIKwYBBQUHAQEEbTBrMCQGCCsGAQUFBzAB
# hhhodHRwOi8vb2NzcC5kaWdpY2VydC5jb20wQwYIKwYBBQUHMAKGN2h0dHA6Ly9j
# YWNlcnRzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydEFzc3VyZWRJRFJvb3RDQS5jcnQw
# gYEGA1UdHwR6MHgwOqA4oDaGNGh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9EaWdp
# Q2VydEFzc3VyZWRJRFJvb3RDQS5jcmwwOqA4oDaGNGh0dHA6Ly9jcmw0LmRpZ2lj
# ZXJ0LmNvbS9EaWdpQ2VydEFzc3VyZWRJRFJvb3RDQS5jcmwwHQYDVR0OBBYEFBUA
# EisTmLKZB+0e36K+Vw0rZwLNMB8GA1UdIwQYMBaAFEXroq/0ksuCMS1Ri6enIZ3z
# bcgPMA0GCSqGSIb3DQEBBQUAA4IBAQBGUD7Jtygkpzgdtlspr1LPUukxR6tWXHvV
# DQtBs+/sdR90OPKyXGGinJXDUOSCuSPRujqGcq04eKx1XRcXNHJHhZRW0eu7NoR3
# zCSl8wQZVann4+erYs37iy2QwsDStZS9Xk+xBdIOPRqpFFumhjFiqKgz5Js5p8T1
# zh14dpQlc+Qqq8+cdkvtX8JLFuRLcEwAiR78xXm8TBJX/l/hHrwCXaj++wc4Tw3G
# XZG5D2dFzdaD7eeSDY2xaYxP+1ngIw/Sqq4AfO6cQg7PkdcntxbuD8O9fAqg7iwI
# VYUiuOsYGk38KiGtSTGDR5V3cdyxG0tLHBCcdxTBnU8vWpUIKRAmMYIEQDCCBDwC
# AQEwgZMwfzELMAkGA1UEBhMCVVMxHTAbBgNVBAoTFFN5bWFudGVjIENvcnBvcmF0
# aW9uMR8wHQYDVQQLExZTeW1hbnRlYyBUcnVzdCBOZXR3b3JrMTAwLgYDVQQDEydT
# eW1hbnRlYyBDbGFzcyAzIFNIQTI1NiBDb2RlIFNpZ25pbmcgQ0ECEDy8h3uZuhhY
# iaQ2ipxpONkwCQYFKw4DAhoFAKBwMBAGCisGAQQBgjcCAQwxAjAAMBkGCSqGSIb3
# DQEJAzEMBgorBgEEAYI3AgEEMBwGCisGAQQBgjcCAQsxDjAMBgorBgEEAYI3AgEV
# MCMGCSqGSIb3DQEJBDEWBBTa+6rb6zq4va07MPoV2/88kByOvTANBgkqhkiG9w0B
# AQEFAASCAQALP+N/tqR0/Qw451i4fsXK/Cr+XcuRTqivAnlfJbHvZI11NSxwQ03X
# KY2qu60+wg0Gfl/ZwwAznN1IUFUyBObCmmFoF7lxABUOnT7/mlKQCPQ4JPFlI1kK
# 1F6DhsS9LAIAsci1IClXszVfWFCZ/1JYvh3aRF+dN5s04jqXOqpInSTOskbyB6ad
# 1u9EessQSZJFqJolkookkIov8xhxcF7UOH/FZfzKhDnJvITS7x4cbH01CAuvAdCO
# WenI8WeZVLJHajWnrZ9V1JJda2BQoWbDf6I9LOsavGy/s6MiopjUg4RvS72D8L0N
# msDnj3u7ydVYfJ+67pPW/zGyd++wsG4RoYICDzCCAgsGCSqGSIb3DQEJBjGCAfww
# ggH4AgEBMHYwYjELMAkGA1UEBhMCVVMxFTATBgNVBAoTDERpZ2lDZXJ0IEluYzEZ
# MBcGA1UECxMQd3d3LmRpZ2ljZXJ0LmNvbTEhMB8GA1UEAxMYRGlnaUNlcnQgQXNz
# dXJlZCBJRCBDQS0xAhADAZoCOv9YsWvW1ermF/BmMAkGBSsOAwIaBQCgXTAYBgkq
# hkiG9w0BCQMxCwYJKoZIhvcNAQcBMBwGCSqGSIb3DQEJBTEPFw0yMDAzMjYxMjA0
# MzVaMCMGCSqGSIb3DQEJBDEWBBRF8BlvtZC95yC6p4E/UqSASV633zANBgkqhkiG
# 9w0BAQEFAASCAQAo8I30sVb5ntMYgCRot1euFD41ojwoESSRh85mxXK3Oj+vREpb
# ZxD2OgDnvwFlxzgsQrENSg+bIveT8w4boW/Owt3b/kOmuqb9I6DwK4RQOlYYp56z
# zA0YkwS03lA5sZKxvsvsWJwX4ZBdpzibwRs6RX4cJvgPJgD0yfVwWwxyKUqAdggx
# lWpGyzUrk43QbfbLamlJ0yro/iud5fbNps0F3b3e+nzqkn4NFz0JdqwevnPMXXXN
# UbJ0g5+qJZdKBwjgPqSlDECThZHeapzKNMVof9yx+H3gd4IiE9Awg8JvCvJ+e0Y3
# jptZrzTzeVAv7ukQhZjhqD9IFtgNXOXot49/
# SIG # End signature block
