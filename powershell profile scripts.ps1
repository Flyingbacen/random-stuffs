Write-Host 'preset commands'
# checnge this variable to user dir or something
$userdirselect = ""
function adbappstart {
    param($packageName)
    $userdirselect\Documents\adb\adb.exe shell monkey -p $packageName -c android.intent.category.LAUNCHER 1
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
        $userdirselect\.stacher/youtube-dl --embed-metadata --no-check-certificate --ffmpeg-location C:\Windows\ --download-sections "*$time" -o "$userdirselect\turtlesongs\song.$number$topic.mp4" $link 
        
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
Write-Host 'Command: turtlesong -time -link -number'
