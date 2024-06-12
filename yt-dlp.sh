#!/bin/bash
link=$1 # link to download
timestart=$2 # start time of clip
timeend=$3 # end time of clip

if [[ -z $link ]]; then
    echo "script usage: yt-dlp.sh <link> [start time] [end time]"
    echo "start time can be in the format of HH:MM:SS.mm or in seconds, same with end time"
    exit 1
fi

yt_dlp_download()
{
    ytdlp=~/Downloads/yt-dlp_linux
    downloadpath="~/Videos/%(title)s.%(ext)s"

    if [[ $link == "https://www.youtube.com/"* ]]; then # Is there a simpler way to do the following?
        if [[ -z $timestart || -z $timeend ]]; then
            echo "No time range, youtube" # debug
            $ytdlp -f "(bestvideo+bestaudio/best)[protocol!*=dash]" \
            -o $downloadpath \
            $link
        else
            echo "time range, youtube"
            $ytdlp -f "(bestvideo+bestaudio/best)[protocol!*=dash]" \
            --external-downloader ffmpeg \
            --external-downloader-args "ffmpeg_i:-ss $timestart -to $timeend" \
            -o $downloadpath \
            $link
        fi
    else
        if [[ -z $timestart || -z $timeend ]]; then
            echo "No time range, other"
            $ytdlp -f "(bestvideo+bestaudio/best)" \
            -o $downloadpath \
            $link
        else
            echo "time range, other"
            $ytdlp -f "(bestvideo+bestaudio/best)" \
            --external-downloader ffmpeg \
            --external-downloader-args "ffmpeg_i:-ss $timestart -to $timeend" \
            -o $downloadpath \
            $link
        fi
    fi
}

yt_dlp_download $link $timestart $timeend