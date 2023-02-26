Welcome to the README for the Binance Spot Market Trading Discord Bot! 

### Trade on Binance's SPOT market directly from your Discord server with your own discord bot. 

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

then create a private discord server , add the bot and start trading

once your bot is up send **!info** copy userid 

![image](https://user-images.githubusercontent.com/106902748/221430020-9328da53-b2c4-453e-a498-9213e07e7a10.png)

add this to <allowed> in **config.ini** and restart your discord bot 

this will allow you only to use the BOT so , no one can miss with your bot or trades

## Features:

    it Open trades and save them into a database
    it Track PNL and current price
    it DCA if needed
    it Show status of trades
    it Close deals



## Commands:
    
    !buy <symbol without USDT> <trade value> - example : **!buy btc 1000** -- it will buy BTC market order for $1000
    !dca <symbol> <trade value> - example : **!dca btc 2000**  -- it will DCA BTC at market order for $2000
    !sell <symbol> - Close a specific symbol example : **!sell btc** this will sell all your position which is saved in database
    !stats - Show the current status of all open trades

![image](https://user-images.githubusercontent.com/106902748/221428152-a8e7538d-add8-4277-bd6a-2d1e644fb6d4.png)


Contributing:
If you are interested in contributing to this project, please feel free to submit a pull request. Before doing so, please make sure to discuss your changes with the project maintainers.

License:
This project is licensed under the MIT license. See the LICENSE file for more details.


Please note that trading is inherently risky and users should exercise caution when using this bot. 
I'm not responsible for any losses incurred through its use.

### support

https://discord.gg/RWtT7Nx9jh
