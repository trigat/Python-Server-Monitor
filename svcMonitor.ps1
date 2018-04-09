  <#
  ------------- Service Checker ------------------

  .SYNOPSIS
  Scan list of servers and checks status of known services.

  .SETUP
  Place list of servers and services in servers.txt and services.txt.

  .USE
  Just run it after you fill in .txt files.
  You can use % for wildcard in list.

  .OUTCOME
  svclog.csv will be created

  #>

$myServices = $PSScriptRoot + "\list\services.txt" # $PSScriptRoot references current directory
$myServers  = $PSScriptRoot + "\list\servers.txt"
$Log        = $PSScriptRoot + "\log\svclog.csv"
$LogLive    = $PSScriptRoot + "\log\svclogLive.csv"

Remove-Item -Path $Log

$serviceList = Get-Content $myServices

$comps = Get-Content $myServers

$results = Invoke-Command -ComputerName $comps -ScriptBlock {
    ForEach ($service in $using:serviceList)
    {
        Get-WmiObject -Class Win32_Service -Filter "Name LIKE '$service'"
    }
} 

# remember, keep Select on outside of Inovke scriptblock to format properly
$results | Select-Object -Property PSComputerName, Name, State, StartMode | Export-Csv -NoTypeInformation -Path $Log

# Create a second current log that Python can read while this script runs
Copy-Item -Path $Log -Destination $LogLive
