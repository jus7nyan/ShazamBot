#!/bin/bash
url="$1"
path="$2"
type="$3"
name="$4"
service="$5"

if [ "$service" == "youtube"  ]
then
        if [ "$type" == "audio" ]
        then
                yt-dlp -f 'ba' -x --audio-format mp3 $url  -o $path'/'$name'.%(ext)s'
        else
                yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' $url -o $path'/'$name'.%(ext)s'
        fi
else
        yt-dlp -f 480p $url -o $path'/'$name'.%(ext)s'
fi