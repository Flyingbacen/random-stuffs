#### Requirements
To run most of the files, you will need modules not included in python core. To fix this, after you have downloaded the zip in **code -> Download ZIP**, navigate to the folder in cmd/powershell and run <kbd>pip3 install -r requirements.txt</kbd>
### Description of files
<details><summary><h5>Note:</h4></summary>
Scripts for ps99 have been moved <a href="https://github.com/Flyingbacen/PS99-scripts">here</a> due to how many I have made over time.
</details>

- [turtle pics](./find%20turtle%20pics.py) -> gui made to find the turtle pics in the spotify experiment, "he-brings-you-playback-progress". Uses [Rinuwaii's](https://github.com/rinuwaii) json file found [here](https://github.com/rinuwaii/he-brings-you-playback-progress/blob/main/heBringsYouPlaybackProgress.json), renamed to `list.json` in the file for simplicity.

- [ps profile script](./powershell%20profile%20scripts.ps1) -> second function (turtlesong) was not intended to be related to turtle pics, was used for downloading snippets of a stream, and output to ./turtlesongs/
    - first function was more of a test than anything else tbh
    - if they are not in your path, change adb, yt-dlp (or youtube-dl, should work with it too) and ffmpeg to their proper locations. (lines 6, 23, 26 respectively)
    - demicrosoft
        - Made for game bar recordings, since they are somehow __*extremely*__ ineficient with storage space. (btw, Discord supports hevc now)

- [8 ball pool free cue redeem](./8ballpoolredeem.py) -> Check out my other repository featuring a discord bot! -- [Github Repository](https://github.com/Flyingbacen/Discord-rawrbot)
    - This is just stolen from there, since I'm apparently too lazy to re set it up so that the bot boots with my computer

- [owo auto](./owo%20auto.py) -> made for the owo bot in discord. makes messy blob messages sometimes, shouldn't happen anymore though

- [random list](./radom%20list%201-10.py) -> was bored and wanted to see if I could do it
    - easily customizable to however long you want the numbers to go on for

- [yes](./yes.py) -> I was bored and didn't know if there was a Windows equivalent

- [yt-dlp](./yt-dlp.sh) -> Was too lazy to find where the config file was, and Youtube is special, and for some reason, yt-dlp is missing the --download-sections arguement, so I needed to use ffmpeg.

- [counter](./counter.py) -> Lets you count, and has saving via json

- [coin flip](./coinflip.py) -> flips a coin until it happens x times, over y iterations, and then shows it to you with mathplotlib. made for a 1 in 16 mil visualization on reddit. Takes a few hours to finish with current settings

- [screenshot/autotranslate](./screenshot.py) -> Takes a screenshot of a predefined area and automatically translates
    - To change the region where the screenshot is saved by default, change `DEFAULTREGION` to the format x<sub>1</sub>, y<sub>1</sub>, x<sub>2</sub>, y<sub>2</sub>.
        - x<sub>1</sub>, y<sub>1</sub> is the top left corner of the region to screenshot
        - x<sub>2</sub>, y<sub>2</sub> is the bottom right corner
    - You can choose to disable translation by changing `TRANSLATE = True` to `TRANSLATE = False`
        - The default language translation is from chinese simplified _(zh\_Hans)_ to English _(en)_.
    - You can choose to have the screenshot taken saved to the clipboard by setting `IMAGE_TO_CLIPBOARD = False` to `IMAGE_TO_CLIPBOARD = True`
    <details><summary>Default keybinds:</summary>
        <ul>
            <li><kbd>s</kbd>: take a screenshot and/or translate</li>
            <li><kbd>d</kbd>: clear terminal output</li>
            <li><kbd><kbd>shift</kbd>+<kbd>[</kbd></kbd>: Change the region</li>
            <ul>
                <li>after activating this keybind, press enter on the top right region, and then enter on the bottom right region. The enter key shouldn't activate anything on the program itself.</li>
            </ul>
            <li><kbd><kbd>shift</kbd>+<kbd>r</kbd></kbd>: Change the region back to <code>DEFAULTREGION</code></li>
        </ul>
    </details>

    <details><summary>Individual Python Dependencies</summary>
        <kbd>pip3 install pyautogui pywin32 numpy translate keyboard Pillow</kbd>
    </details>

- [twitch api thing?](./twitchapi.py) -> Made for the Pokemon drops, where you need to watch specific streamers for the specific game, leave it running in the background and it will send a webhook wherever you want it to in discord.
    - requires manually setting up your twitch api/application
    - follow [this](https://dev.twitch.tv/docs/api/get-started/) official guide for an easy setup.<br>You only need to follow up to "Get an OAuth Token"
    - Uses authcodes.json, which should be in the same directory as the file.
        <details><summary>example file setup</summary>
        <pre><code>
        {
            "client_id": "client_id",
            "secret": "client_secret",
            "Authorization": "oauth_token"
        }
        </code></pre>
        </details>
    - the script should theoretically automatically update your OAuth token, but I'm not entirely sure if it works properly or not yet