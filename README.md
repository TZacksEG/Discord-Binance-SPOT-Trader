Welcome to the README for the Binance Spot Market Trading Discord Bot! 

## WHY it was created ?
_The Binance SPOT market does not have a built-in interface or a way to track trades, so this bot was created to fill that gap._

_The purpose of this bot is to allow users to open trades, track their PNL and current prices, and even DCA if needed and close them._

## Getting Started
follow these steps to install and run the bot:

1. Clone the project's GitHub repository to your VPS using the git clone command. git clone https://github.com/TZacksEG/Discord-Binance-SPOT-Trader
2. Navigate to the <Discord-Binance-SPOT-Trader> directory.
3. Install the required Python packages by running pip install -r requirements.txt
4. open "config.ini" and fill its required data 
5. Run the bot by executing the main.py file in the terminal using the **python3 main.py** command.

## config.ini file 
![image](https://user-images.githubusercontent.com/106902748/221427059-9be287ba-a56d-417e-b1af-a8689a0e14f9.png)


[settings]:

    timezone = Africa/Cairo
    debug = False
    logrotate = 7
    database-name = binance-discord
    apikey = Binance apikey
    apisecret = Binance secret
    discord-token = Discord bot token
    allowed = 0


to get a discord bot token go to [Discord Developer Portal](https://discord.com/developers/applications)
then click on **NEW APPLICATION**

![image](https://user-images.githubusercontent.com/106902748/221427406-5e14b25a-9167-4ecc-ba45-5c24259b3a42.png)

Then click on **ADD BOT**

![image](https://user-images.githubusercontent.com/106902748/221427482-ad26da36-5f5e-452d-b627-01add29a3eaf.png)

then make sure **message intent is active** and click on **RESET TOKEN**

![image](https://user-images.githubusercontent.com/106902748/221427602-617c4dbb-f908-4c6d-bb3e-41bb8a438567.png)


COPY THE TOKEN and add it to **discord-token** in config.ini file .

then create a private discord server and use the bot 

Features:

    it Open trades and save them into a database
    it Track PNL and current price
    it DCA if needed
    it Show status of trades
    it Close deals

![image](https://user-images.githubusercontent.com/106902748/221428152-a8e7538d-add8-4277-bd6a-2d1e644fb6d4.png)

The bot's stats include pairs, average entry price, total invested in the trade, total value now for the trade, UPNL in USD value, and UPNL in percentage.

Getting Started:
To use this bot, you will need to have an account on Binance's SPOT market. Once you have an account, you will need to generate an API key with "trade" permissions. Make sure to keep this key safe and not share it with anyone.

Clone the repository:
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY

Create a virtual environment:
python -m venv venv

Activate the virtual environment:
venv\Scripts\activate.bat (Windows)
source venv/bin/activate (macOS/Linux)

Install the requirements:
pip install -r requirements.txt

Set up the environment variables:

    Create a .env file in the root directory of the project
    Add the following environment variables:

makefile

DISCORD_TOKEN=<your discord token>
BINANCE_API_KEY=<your binance api key>
BINANCE_SECRET_KEY=<your binance secret key>

Run the bot:
python main.py

Commands:

    !buy <symbol> <quantity> <price> - Buy a specific symbol at a specific price
    !sell <symbol> <quantity> <price> - Sell a specific symbol at a specific price
    !close <symbol> - Close a specific symbol
    !stats - Show the current status of all open trades
    !help - Show a list of all available commands

Contributing:
If you are interested in contributing to this project, please feel free to submit a pull request. Before doing so, please make sure to discuss your changes with the project maintainers.

License:
This project is licensed under the MIT license. See the LICENSE file for more details.

Acknowledgments:
Special thanks to the Binance API and the Discord API for making this project possible.

Please note that trading is inherently risky and users should exercise caution when using this bot. The creators of this bot are not responsible for any losses incurred through its use.
