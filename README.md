This script is very basic right now, but it seems to work great. It will load up all playlists on your spotify account and recreate them in google play.
It also spits out the playlists and their tracks to a text file.

By using ezportify you may violate both Spotify's and Google's Terms of Service. You agree that you are using ezportify on your own risk. The author does not accept liability (as far as permitted by law) for any loss arising from any use of this tool. If you choose not to agree to these terms, then you may not use this tool.

Run ezportify.py with python and follow the instructions in the command prompt. You will need your google play username and password along with a spotify oauth token from https://developer.spotify.com/web-api/console/get-current-user-playlists/

If you are unable to sign in to your Google account, turn on access for less secure apps here: https://www.google.com/settings/security/lesssecureapps/
You may turn it off after the program has completed.

Run ezportify.py -h for help (ezportify.exe -h for windows users)

**WINDOWS USERS** I have included ezportify.exe in win32.zip. If you are not comfortable with python you can download and extract win32.zip then run ezportify.exe to get going right away.
**[DOWNLOAD HERE](https://github.com/jordam/ezportify/raw/master/win32.zip)**

This script is based on pyportify by rckclmbr https://github.com/rckclmbr/pyportify 

pyportify is based on the original portify by mauimauer https://github.com/mauimauer/portify