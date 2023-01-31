# finBot
Telegram bot that saves all of your expenses to Google Sheets.

<p align="center">
  <img src="https://raw.githubusercontent.com/Sh3lldor/finBot/main/pics/icon.png">
</p>

## Table of Contents
- [finBot](#finbot)
  - [Table of Contents](#table-of-contents)
  - [Intro](#intro)
  - [Language](#language)
  - [Build](#build)
  - [Run](#run)
  - [Credits](#credits)

## Intro
This telegram bot saves all of your expenses to Google Sheets. Including: income, outcome and savings.</br>
You will need:
1) Get an access token for Google Sheets and rename it to `token.json`
2) Edit `.env` file with your personal information

## Language
Language settings can be changed via the `responses.py` file.

## Build
```
git clone https://github.com/Sh3lldor/finBot.git
cd finBot
docker build .
```

## Run
```
docker run -d --restart=always --name=finBot <FINBOT_IMAGE_ID>
```

## Credits
* Pictures and Icons
    * https://www.iconfinder.com
        * licensed by - https://creativecommons.org/licenses/by/3.0/
