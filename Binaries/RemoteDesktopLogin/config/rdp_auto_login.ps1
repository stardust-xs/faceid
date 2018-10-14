Param($envdomn, $usr, $pass, $admLogin, $ipAdr, $bbpLbg)
# If you are getting the error .ps1 script cannot be run. Then execute the below command.
#Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force

$ScriptDir = "$PSScriptRoot" # Script path
$EnvConfig = $ScriptDir + "\env_config.ps1"
#$LoginScript = $ScriptDir + "\snow_login.ps1"
$FileNameStartWitn = "Rdp_Login"

#=====================================
# Environment Variable Configuration
#=====================================
. $EnvConfig $ScriptDir $FileNameStartWitn $envdomn $usr $pass $bbpLbg

if($exit_flg -eq 1) {
  log "END"
  exit
}

#echo '' > $logfile
log "Log file is: $logfile"

#$domn = $snusr.split('\')[0]
log "Start time : $(Get-Date)"
log "Domain\UserID : $snusr"

if( $domn -eq "RMGP" ) {
  if( $rEnv -eq "BBP" ) {
    if( $ipAdr -eq "ALL" ) {
	  $rmv_crd = $bbp_rmgp
    }
	else {
	  $rmv_crd = $ipAdr
	}
  }
  else {
    if( $ipAdr -eq "ALL" ) {
	  $rmv_crd = $lbg_rmgp
    }
	else {
	  $rmv_crd = $ipAdr
	}
  }
}
elseif( $domn -eq "RMGV" ) {
   if( $ipAdr -eq "ALL" ) {
     $rmv_crd = $preprod_rmgv
   }
   else {
     $rmv_crd = $ipAdr
   }
}
elseif( $domn -eq "RMGN" ) {
  if( $rEnv -eq "TEST" ) {
    if( $ipAdr -eq "ALL" ) {
	  $rmv_crd = $test_rmgn
    }
	else {
	  $rmv_crd = $ipAdr
	}
  }
  else {
    if( $ipAdr -eq "ALL" ) {
	  $rmv_crd = $dev_rmgn
    }
	else {
	  $rmv_crd = $ipAdr
	}
  }
}

#if( $admLogin -eq "yes" ) {
#   $rmv_crd = $ipAdr
#}

connect_rdp $rmv_crd $admLogin

Start-Sleep -Seconds 20 
stop-process (Get-WMIObject -Class Win32_Process -Filter "Name='mstsc.exe'" | where { $_.WorkingSetSize -lt 40000000 }).Handle

$svr_name = ((Get-WMIObject -Class Win32_Process -Filter "Name='mstsc.exe'" | where { $_.WorkingSetSize -ge 40000000 }).CommandLine -split ' ')[2]

if ( $svr_name ) {
    log "Now entering into the rdp" 
    enter_into_rdp $svr_name
}

remove_cr $rmv_crd

log "End time : $(Get-Date)"
log " --- End --- "

#=====================================
# End
#=====================================
