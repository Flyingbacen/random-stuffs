### Description of files
- [fish.py](./ps99%20scripts/fish.py) -> Made for auto-fishing in the Roblox game Pet Simulator 99

- [turtle pics](./find%20turtle%20pics.py) -> gui made to find the turtle pics in the spotify experiment, "he-brings-you-playback-progress". Uses [Rinuwaii's](https://github.com/rinuwaii) json file found [here](https://github.com/rinuwaii/he-brings-you-playback-progress/blob/main/heBringsYouPlaybackProgress.json), renamed to `list.json` in the file for simplicity.

- [ps profile script](./powershell%20profile%20scripts.ps1) -> second function (turtlesong) was not intended to be related to turtle pics, was used for downloading snippets of a stream, and output to ./turtlesongs/
    - first function was more of a test than anything else tbh
    - if they are not in your path, change adb, yt-dlp (or youtube-dl, should work with it too) and ffmpeg to their proper locations. (lines 6, 23, 26 respectively)
    - demicrosoft
        - Made for game bar recordings, since they are somehow __*extremely*__ ineficient with storage space. (btw, Discord supports hevc now)

- [8 ball pool free cure redeem](./8ballpoolredeem.py) -> Check out my other repository featuring a discord bot! -- [Github Repository](https://github.com/Flyingbacen/Discord-rawrbot)
    - This is just stolen from there, since I'm apparently too lazy to re set it up so that the bot boots with my computer

- [owo auto](./owo%20auto.py) -> made for the owo bot in discord. makes messy blob messages sometimes, shouldn't happen anymore though
    - broken version is broken. make a pull request if you think you can fix it :)

- [random list](./radom%20list%201-10.py) -> was bored and wanted to see if I could do it
    - easily customizable to however long you want the numbers to go on for

- [yes](./yes.py) -> I was bored and didn't know if there was a Windows equivalent

- [yt-dlp](./yt-dlp.sh) -> Was too lazy to find where the config file was, and Youtube is special, and for some reason, yt-dlp is missing the --download-sections arguement, so I needed to use ffmpeg.

- [counter](./counter.py) -> Lets you count, and has saving via json

- [pet simulator chance list](./ps99%20scripts/ps99%20luck%20calculator.py) -> Search up a pet from the egg, pick what egg you're looking for, and you can see the base odds for all the pets in the egg
    - If there is only one egg, it is automatically chosen

- [coin flip](./coinflip.py) -> flips a coin until it happens x times, over y iterations, and then shows it to you with mathplotlib. made for a 1 in 16 mil visualization on reddit. Takes a few hours to finish with current settings

- [chest open](./ps99%20scripts/chest%20open.py) -> made for opening chests in ps99

- [ps99 auto fuse](./ps99%20scripts/auto%20fuse.py) -> made for automatically fusing pets
    - To start it, go to the world 1 fuse machine located in area 28 and open the menu. open the script and it will start automatically. If the script breaks, go to line 9 and change `num:int=2` to `num:int=3`.
    - To stop the script, shove your mouse into any corner for about half a second.