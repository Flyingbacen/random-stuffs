Write-Host 'preset commands'
$userdirselect = "" # change this variable to user dir or something
# line 6, change adb to adb installation, on line 23, change yt-dlp installation directory and ffmpeg, line 23, 26, ffmpeg installation directory (unless they are in the path)
function adbappstart {
    param($packageName)
    adb.exe shell monkey -p $packageName -c android.intent.category.LAUNCHER 1 
}
Write-Host 'Command: adbappstart [packageName]'
function turtlesong {
    param(
        [Parameter(Mandatory)]
        [string]$time,
        [Parameter(Mandatory)]
        [string]$link,
        [Parameter(Mandatory)]
        [string]$number,
        [string]$topic
        )
    if ("$topic" -ne "") {
        $topic = ".($topic)"
    }
    if ((Test-Path "$userdirselect\turtlesongs\song.$number$topic.mp4") -eq $false) {
        ytdlp --embed-metadata --no-check-certificate --ffmpeg-location "C:\Windows" --download-sections "*$time" -o "$userdirselect\turtlesongs\song.$number$topic.mp4" $link
        $choice = Read-Host "Use ffmpeg and convert to audio? (y/n)"
        if ($choice -eq "y") {
            ffmpeg -i "$userdirselect\turtlesongs\song.$number$topic.mp4" -vn -c:a copy "$userdirselect\turtlesongs\audio\song.$number$topic.m4a"
        } else {
            write-host "Not converting to audio."
        }
    } else {
        write-host "Song with number ""$number"" already downloaded."
    }
}
Write-Host 'Command: turtlesong -time -link -number [-topic]'
function openastrustedinstaller { # requires NtObjectManager module, install with "Install-Module -Name NtObjectManager"
    param(
        $application,
        [switch]$start = $false
    )
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $isAdmin) {
    Write-Warning -Message 'You need to run this command as an administrator.'
    return
    }
    $ServiceName = 'TrustedInstaller'
    $arrService = Get-Service -Name $ServiceName
    while ($arrService.Status -ne 'Running')
    {
        Start-Service $ServiceName
        write-host $arrService.status
        write-host 'Starting TrustedInstaller service automatically, please wait'
        $arrService.Refresh()
        if ($arrService.Status -eq 'Running')
        {
            Write-Host 'Service is now Running, continuing script'
        } else {
            print "An error occurred while starting the service. Please start the service manually and run the script again. current status: ""$arrService.Status"""
        }
    }
    $parent = Get-NtProcess -ServiceName TrustedInstaller
    New-Win32Process $application -CreationFlags NewConsole -ParentProcess $parent
}
Write-Host 'Command: openastrustedinstaller <application> [-start] | Run -start if TrustedInstaller service is not running.'
function demicrosoft {
    param(
        [string]$inputfile,
        [Alias("l")]
        [switch]$latest = $false, 
        [switch]$Discord = $false, # Used as $true in script, PS limitation-can't use $true by default
        [Alias("s")]
        [switch]$hevc = $false,
        [switch]$ls = $false,
        [switch]$gpu = $false,
        [switch]$copy = $false
    )
    if ($ls -eq $true) {
        $latest = $true
        $hevc = $true
    }
    if ($latest -eq $true) {
        $inputfile = Get-ChildItem | Sort-Object -Property LastWriteTime -Descending | Select-Object -First 1
    }
    if ($inputfile -eq "") {
        throw 'No input file specified.'
    }
    $inputfile = Convert-Path -Path $inputfile
    $outputfile = $inputfile -replace ".mp4", "-reformed.mp4"
    if ($discord -eq $true -and (get-item (ffmpeg -i "$inputfile" (if ($hevc -eq $true) return -c:v (if ($gpu -ne $false) return ((($GPU=Get-CimInstance -ClassName CIM_VideoController).AdapterCompatibility) && if ($GPU -eq "NVIDIA") {return hevc_nvenc} elseif ($GPU -eq "Intel") {return hevc_qsv} elseif ($GPU -eq "AMD") {return hevc_amf} else {return hevc})) else {return hevc}) "$outputfile").Length -gt 26214400 (rem "26214400 = 25MB")) -and (Read-Host "File is larger than 25MB. Trim 5 seconds? (y/n)") -eq "y") {ffmpeg -i "$outputfile" -ss 5 -c copy ($outputfile -replace ".mp4", "-cut.mp4") && Remove-Item $outputfile}
    if ($copy -eq $true) {
        Set-Clipboard -Value $outputfile
    }
}
Write-Host 'Command: demicrosoft <input file> [-latest | -l] [-discord (use to disable)] [-hevc | -s] [-copy]'
