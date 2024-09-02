# Discord call logger and metrics

This script lets you get metrics and call data from a private chat in Discord. This script was made because I needed a call log for immigration to the USA. This script does not reveal any private information about people in the private chat.

## Instructions

- Download the script from GitHub
- If not installed, install Python 3.11 - [Download Python](https://www.python.org/downloads/)
- Install the following package:

```console
# Linux/Mac
pip install -U snowflake-util

# Windows
py -3 -m pip install -U snowflake-util
```

- Open Discord **in your browser** and connect to your account
- Press F12 on your keyboard to open the dev console and go to the _Network_ tab
- Open the private chat you want to pull the call logs out off
- In the _Network_ you should see a **message?limit=50** in the _Name_ column
- You will need the channelID (top green box) and the authorization token (bottom green box) from **\*Request** Headers\*
  ![alt text](https://github.com/VincenzoPucci/discord_call_logs/blob/main/discordF12.PNG?raw=true)
- Insert the values in the _cst.py_ file in the script
- In the _cst.py_ file, set the start and end date with the START_DATE and END_DATE constants
- Run the script with the command

```console
# Linux/Mac
python3 ./api.py

# Windows
python ./api.py
```

## Authors

- [@VincenzoPucci](https://github.com/VincenzoPucci)
