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
        [Alias("s")]
        [switch]$hevc = $false,
        [switch]$ls = $false,
        [Alias("g")]
        [switch]$usegpu = $false,
        [Alias("h")]
        [switch]$help = $false,
        [alias("compat")]
        [switch]$dsccompatible = $false
    )
    if ($help -eq $true) {
        Write-Host @'
Command: demicrosoft <input file> [-latest | -l] [-hevc | -s] [-usegpu | g] [-help | -h] [-dsccompat]
input file: The file to convert.
-latest | -l: Use the latest file in the directory. Overrides input file.
-hevc | -s: Use HEVC codec.
-dsccompat: Compress the file to ensure it is under Discord's 10MB limit. implies -hevc.
-usegpu: Use GPU for encoding. Implies -hevc (Less efficient compression, much faster encoding)
'@
        return
    }
    for ($i = 0; $i -lt $args.Length; $i++) {
        if ($args[$i] -eq "-l") {
            $latest = $true
        }
        if ($args[$i] -eq "-s") {
            $hevc = $true
        }
        if ($args[$i] -eq "-g") {
            $usegpu = $true
        }
    }
    if ($latest -eq $true) {
        $inputfile = Get-ChildItem | Sort-Object -Property LastWriteTime -Descending | Select-Object -First 1
    }
    if ($inputfile -eq "") {
        throw 'No input file specified.'
    }

    $inputfile = Convert-Path -Path $inputfile
    Write-Warning "Input file: $inputfile"
    $outputfile = $inputfile -replace ".mp4", "-reformed.mp4"

    if ($dsccompatible -eq $true) {
        $ffprobejson = ffprobe -v quiet -print_format json -show_format "$inputfile" | Out-String
        $duration = ($ffprobejson | ConvertFrom-Json).format.duration
        $outputfile = $outputfile -replace "-reformed.mp4", "-compressed.mp4"

        $target_file_size_bits = 10485760 # 10MB
        $video_bitrate_bps = $target_file_size_bits / $duration
        $video_bitrate_kbps = [math]::Round($video_bitrate_bps / 1024)

        Write-Warning "Duration: $duration`s    Video Bitrate: $video_bitrate_kbps kbps"
        
        if ($usegpu -eq $true) {
            $encoder_format = switch((Get-CimInstance -ClassName CIM_VideoController).AdapterCompatibility) {
                "NVIDIA" {"hevc_nvenc"}
                "Intel" {"hevc_qsv"}
                "AMD" {"hevc_amf"}
                default {"hevc"}
            }
            if ($encoder_format -eq "") {
                Write-Warning "No GPU encoder found, using CPU."
            }
        }

        ffmpeg -i "$inputfile" -y -c:v $encoder_format -b:v $video_bitrate_kbps`k -b:a 128k -pass 1 -an -f null NUL
        ffmpeg -i "$inputfile" -y -c:v $encoder_format -b:v $video_bitrate_kbps`k -b:a 128k -pass 2 "$outputfile"
        rm "ffmpeg2pass-0.log"
        if ($copy -eq $true) {
            Set-Clipboard -Path $outputfile
        }
        return
    }

    if ($hevc -eq $false ) {
        ffmpeg -i "$inputfile" "$outputfile"
    } elseif ($usegpu -eq $true) {
        $encoder_format = switch((Get-CimInstance -ClassName CIM_VideoController).AdapterCompatibility) {
            "NVIDIA" {"hevc_nvenc"}
            "Intel" {"hevc_qsv"}
            "AMD" {"hevc_amf"}
            default {"hevc"}
        }
        ffmpeg -i "$inputfile" -c:v $encoder_format "$outputfile"
    } else {
        ffmpeg -i "$inputfile" -c:v hevc "$outputfile"
    }

    if ((Get-Item $outputfile).Length -gt 26214400) {Write-Warning "The file is too large for Discord, try running with the -dsccompat flag"}
    if ($copy -eq $true) {
        Set-Clipboard -Path $outputfile
    } 
}
Write-Host 'Command: demicrosoft <input file> [-latest | -l] [-discord | -d] [-hevc | -s] [-usegpu] [-help | -h] [-dsccompat]'
