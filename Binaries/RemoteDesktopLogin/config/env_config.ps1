Param($ScriptDir, $FileNameStartWitn, $envdomn, $inputUid, $inputPas, $bbpLbg)

#-----------------------------------
# I/O and LOG file settings
#-----------------------------------
$logDir = $ScriptDir + "\Logs"
$initial = $FileNameStartWitn #"Inc_Active_List"
$logfile = $logDir + "\" + $initial + ".log"
if(!(Test-Path $logDir)) { md $logDir }
echo 'Start Processing...' > $logfile

#-----------------------------------
# Get the registry settings
#-----------------------------------
# import assembly for keyboard input
Add-Type -AssemblyName Microsoft.VisualBasic
Add-Type -AssemblyName System.Windows.Forms
#remove the rdp saved settings
#Remove-Item -Path 'HKCU:\Software\Microsoft\Terminal Server Client\servers' -Recurse  2>&1 | Out-Null
#$rdp_saved_settings = $ScriptDir + "\rdp_setting.txt"
#Reg export "HKCU\Software\Microsoft\Terminal Server Client\servers" $rdp_saved_settings /y

#=====================================
# Function to append output in log file
#=====================================
function log($string, $color)
{
   if ($Color -eq $null) {$color = "white"}
   write-host $string -foregroundcolor $color
   $string | out-file -Filepath $logfile -append
}
log " --- Start --- "

$rEnv=$envdomn.split('\')[0]
$domn=$envdomn.split('\')[1]
log "$rEnv Environment"
log "$domn Domain"

$usrFile = $ScriptDir + '\' + $domn + "UserID.txt"
$passFile = $ScriptDir + '\' + $domn + "EncPass.txt"
$snusr = $( cat $usrFile 2> $null )
$snpass = $( cat $passFile 2> $null)

If ($inputUid -eq $Null -OR $inputUid -eq '') {
  If ($snusr -eq $Null) {
    Log "First time login? Please provide your UserID and try again."
    $exit_flg=1
    exit
  }
}else {
  echo "$domn\$inputUid" | out-file -Filepath $usrFile
  $snusr = $domn + '\' + $inputUid
}

If ($inputPas -eq $Null -OR $inputPas -eq '') {
  If ($snpass -eq $Null) {
    Log "First time login? Please provide your Password and try again."
    $exit_flg=1
    exit
  }
}else {
  #[Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secPass))
  $qvpas = ConvertTo-SecureString $inputPas -AsPlainText -Force
  $snpass = ConvertFrom-SecureString $qvpas
  $snpass | out-file -Filepath $passFile
}
$secPass = $snpass | ConvertTo-SecureString

$sv_time = $( (Get-Date).tostring("HHmmss") )
# Below setting is required for html entuty decoding
Add-Type -AssemblyName System.Web

#-----------------------------------
# Variables sets to limit multithreading
#-----------------------------------
$thread_count = 0 
$SleepTimer = 500
$MaxThreads = 7 # Setting up maxmimun threads

#-----------------------------------
# Server list
#-----------------------------------
$bbp_lbg=$bbpLbg

$bbp_rmgp=(
"172.19.1.171",
"172.19.1.172",
"172.19.1.194",
"172.19.1.195"
)

$lbg_rmgp=(
"172.19.1.167",
"172.19.1.168"
)           
            
$preprod_rmgv=(
"172.19.1.216",
"172.19.1.217",
"172.19.1.218",
"172.19.1.219",
"172.19.1.221",
"172.19.1.222"
)

$test_rmgn=(
"172.19.1.174",
"172.19.1.175",
"172.19.1.196",
"172.19.1.197",
"172.19.1.213",
"172.19.1.214"
)

$dev_rmgn=(
"172.19.1.224",
"172.19.1.225",
"172.19.1.226",
"172.19.1.227",
"172.19.1.228",
"172.19.1.229",
"172.19.1.230"
)

#=====================================
# Function to connect rdp
#=====================================
#function connect_rdp($svr_list, $admLogin)
#{
# helper function to locate a open program using by a given Window name
Function FindWindow([string]$windowName, [int]$sleepInterval = 500) {
  
  [int]$currentTry = 0;
  [bool]$windowFound = $false;
  
  Do {
    Start-Sleep -Milliseconds $sleepInterval
    Try {
	  #if ( $windowName -ne "Remote Desktop connection" ) {
        [Microsoft.VisualBasic.Interaction]::AppActivate($windowName)
      #}
      $windowFound = $true;
    } Catch {
      $windowFound = $false;
    }
	$currentTry++;
    if ( $currentTry -ge "10" )
    {
	  Log "Exit after trying for long time to get the RDP session."
      break;
    }
  } While ($windowFound -eq $false)
  return $windowFound;
}

Function rdp_login($ipAdr, $admLn) {
    cmdkey.exe /generic:$ipAdr /user:$snusr /pass:$( [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secPass)) )
    if ( $admLn -eq 'yes' )
    {
        Log "Admin login to $ipAdr"
        mstsc.exe /v $ipAdr /admin /f
    } else {
        mstsc.exe /v $ipAdr /f
    }
}

function connect_rdp($svr_list, $admLogin)
{
    if ( $snusr.split('\')[0] -eq "RMGP" )
    {
        $svr_list | % {
            rdp_login $_ $admLogin
            #$Sel = select-string -pattern "$_" -path $rdp_saved_settings
			#Log "found: $Sel = select-string -pattern $_ -path $rdp_saved_settings"
            #If ( $Sel.length -eq 0 ) 
            #{ 
            #    if(FindWindow("Remote Desktop connection")) {
            #        Start-Sleep -Milliseconds 250
            #        #[Microsoft.VisualBasic.Interaction]::AppActivate("Remote Desktop connection")
            #        [System.Windows.Forms.SendKeys]::SendWait('dy')
            #    }
            #}
        }
    } else {
        $svr_list | % {
            rdp_login $_ $admLogin
		}
		$svr_list | % {
            if(FindWindow("Windows Security")) {
                Start-Sleep -Milliseconds 200
				#[Microsoft.VisualBasic.Interaction]::AppActivate("Windows Security")
                [System.Windows.Forms.SendKeys]::SendWait($( [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secPass)) )+'{ENTER}')
            }
            if(FindWindow("Windows Security")) {
                Start-Sleep -Milliseconds 200
				#[Microsoft.VisualBasic.Interaction]::AppActivate("Windows Security")
                [System.Windows.Forms.SendKeys]::SendWait($( [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secPass)) )+'{ENTER}')
            }
            #$Sel = select-string -pattern "$_" -path $rdp_saved_settings 
			##Log "found: $Sel = select-string -pattern $_ -path $rdp_saved_settings"
            #If ( $Sel.length -eq 0 ) 
            #{ 
            #    if(FindWindow("Remote Desktop connection")) {
            #        Start-Sleep -Milliseconds 250
            #        #[Microsoft.VisualBasic.Interaction]::AppActivate("Remote Desktop connection")
            #        [System.Windows.Forms.SendKeys]::SendWait('dy')
            #    }
            #}
        }
    }    
}

function remove_cr($svr_list)
{
	$svr_list | % {
		cmdkey.exe /delete:$_
	}
}

function enter_into_rdp($svr_name)
{
	if(FindWindow("$svr_name - Remote Desktop Connection")) {
		Start-Sleep -Milliseconds 250
        Log "rdp found"
        [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    }
}
#get-process iexplore | stop-process
