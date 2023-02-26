import discord
import secrets
import configparser
import asyncio
from binance.client import Client as Cclient, BinanceAPIException
from helpers.misc import (decimal_price, decimal_quantity,
                          get_commission, binance_pair)
from helpers.database import (add_deals, get_qnty, get_avg_price, update_deal_values, get_deals,
                              check_deal, get_orderid, delete_deal)

intents = discord.Intents.default()
intents.message_content = True
config = configparser.ConfigParser()
config.read("config.ini")
bclient = Cclient()
TOKEN = config.get("settings", "discord-token")
allowed = int(config.get("settings", "allowed"))

activity = discord.Activity(name=f"My Binance Account", type=discord.ActivityType.watching)
dis = discord.Client(activity=activity, intents=intents)

b_client = Cclient(api_key=config.get("settings", "apikey"),
                   api_secret=config.get("settings", "apisecret"),
                   )


@dis.event
async def on_ready():
    print("We are connected to discord as {0.user}".format(dis))
    status = bclient.get_system_status().get('msg').capitalize()
    await asyncio.sleep(2)
    if status == "Normal":
        print(f"Binance API System status: Normal\n")
    else:
        print("Error connecting to Binance API")


@dis.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    userid = message.author.id
    user_message = str(message.content)
    if message.author == dis.user:
        return

    elif userid == allowed:
        if user_message == "!info":
            msg = f"**Username** : {username}\n" \
                  f"**User ID** : {userid}\n" \
                  f"**Guild ID** : {message.guild.id}\n" \
                  f"**Channel id** : {message.channel.id}\n"
            embed_message = discord.Embed(title="Server Info", description=msg, color=discord.Color.random())
            await message.channel.send(embed=embed_message)

        elif user_message.startswith("!buy"):
            """Create  a new binance Deal with SMART"""
            try:
                ctx = user_message.split(" ")
                pair = binance_pair(ctx[1])
                trade_value = float(ctx[2])
                # let's get the price of the coin
                try:
                    price = float(b_client.get_symbol_ticker(symbol=pair)["price"])

                    # TODO add the deal to a database for watcher

                    quantity = float(trade_value / price)
                    buy_quantity = round(quantity, decimal_quantity(b_client, pair))

                    orderid = secrets.token_hex(6)
                    params = {
                        "symbol": pair,
                        "side": "BUY",
                        "type": "MARKET",
                        "quantity": buy_quantity,
                        "newClientOrderId": f"{orderid}-SMART",
                    }
                    neworder = b_client.create_order(**params)
                    if neworder:
                        buy_price = neworder["fills"][0]["price"]
                        quantity = ((float(neworder["origQty"]) - get_commission(b_client, pair,
                                                                                 neworder["orderId"])) * 0.998)
                        total_quantity = round(quantity, decimal_quantity(b_client, pair))

                        embed_message = discord.Embed(title="Deal Details",
                                                      description=f"**New Trade for {pair.upper()}**",
                                                      color=discord.Color.random())
                        embed_message.add_field(name="Coin Name", value=pair.upper())
                        embed_message.add_field(name="Trade Value", value=round(trade_value, 2))
                        embed_message.add_field(name="QNTY", value=buy_quantity, inline=True)
                        embed_message.add_field(name="AVG price", value=buy_price, inline=True)
                        embed_message.add_field(name="Trade ID", value=f"{orderid}-SMART", inline=True)
                        embed_message.add_field(name="Order ID ", value=neworder["orderId"], inline=True)
                        await message.channel.send(embed=embed_message)
                        add_deals(config, pair, neworder["orderId"], buy_quantity, buy_price)
                except BinanceAPIException as e:
                    await message.channel.send(f"Error creating order {pair} and error is : **{e}**")

            except IndexError:
                await message.channel.send(f"I'm Working but i got some internal error : "
                                           f" **You have sent an empty message try again**")
            except ValueError:
                await message.channel.send(f"I'm Working but i got some internal error : "
                                           f" **Check the DATA you send**")
        ###########################################################################

        elif user_message.startswith("!dca"):
            """DCA your deals if needed"""
            try:
                ctx = user_message.split(" ")
                pair = binance_pair(ctx[1])
                trade_value = float(ctx[2])
                try:
                    price = float(b_client.get_symbol_ticker(symbol=pair)["price"])

                    # TODO add the deal to a database for watcher

                    quantity = float(trade_value / price)
                    buy_quantity = round(quantity, decimal_quantity(b_client, pair))
                    orderid = secrets.token_hex(6)
                    params = {
                        "symbol": pair,
                        "side": "BUY",
                        "type": "MARKET",
                        "quantity": buy_quantity,
                        "newClientOrderId": f"{orderid}-SMART",
                    }
                    neworder = b_client.create_order(**params)
                    if neworder:
                        buy_price = neworder["fills"][0]["price"]
                        quantity = ((float(neworder["origQty"]) - get_commission(b_client, pair,
                                                                                 neworder["orderId"])) * 0.998)

                        total_quantity = float(get_qnty(config, pair)) + float(quantity)
                        total_quantity = round(total_quantity, decimal_quantity(b_client, pair))

                        total_cost = (float(get_qnty(config, pair)) * float(
                            get_avg_price(config, pair))) + (
                                             float(quantity) * float(buy_price))

                        average_entry_price = round((total_cost / total_quantity), decimal_price(b_client, pair))
                        update_deal_values(config, pair, average_entry_price, total_quantity)
                        embed_message = discord.Embed(title="DCA Details",
                                                      description=f"**Position edit for {pair.upper()}**",
                                                      color=discord.Color.random())
                        embed_message.add_field(name="Coin Name", value=pair.upper())
                        embed_message.add_field(name="Trade Value", value=round(total_cost, 2))
                        embed_message.add_field(name="QNTY", value=total_quantity, inline=True)
                        embed_message.add_field(name="AVG price", value=average_entry_price, inline=True)
                        embed_message.add_field(name="Trade ID", value=f"{orderid}-SMART", inline=True)
                        embed_message.add_field(name="Order ID ", value=neworder["orderId"], inline=True)
                        await message.channel.send(embed=embed_message)
                        add_deals(config, pair, neworder["orderId"], buy_quantity, buy_price)
                except BinanceAPIException as e:
                    await message.channel.send(f"Error creating order {pair} and error is : **{e}**")

            except IndexError:
                await message.channel.send(f"I'm Working but i got some internal error : "
                                           f" **You have sent an empty message try again**")
            except ValueError:
                await message.channel.send(f"I'm Working but i got some internal error : "
                                           f" **Check the DATA you send**")
        ###########################################################################

        elif user_message.startswith("!sell"):
            """Lets Close Deals """
            try:

                ctx = user_message.split(" ")
                pair = binance_pair(ctx[1])
                try:

                    if check_deal(config, pair):
                        quantity = float(
                            (get_qnty(config, pair) - get_commission(b_client, pair,
                                                                     get_orderid(config, pair))) * 0.998)
                        sell_quantity = round(quantity, decimal_quantity(b_client, pair))
                        params = {
                            "symbol": pair,
                            "side": "SELL",
                            "type": "MARKET",
                            "quantity": sell_quantity,
                        }
                        neworder = b_client.create_order(**params)
                        if neworder:
                            sell_price = float(neworder["fills"][0]["price"])
                            sell_qnty = float(neworder["origQty"])
                            total_sell = sell_price * sell_qnty
                            embed_message = discord.Embed(title="Close Deal Details",
                                                          description=f"**Position edit for {pair.upper()}**",
                                                          color=discord.Color.random())
                            embed_message.add_field(name="Coin Name", value=pair.upper())
                            embed_message.add_field(name="Trade Value", value=round(total_sell, 2))
                            embed_message.add_field(name="QNTY", value=sell_qnty, inline=True)
                            embed_message.add_field(name="AVG price", value=sell_price, inline=True)
                            embed_message.add_field(name="Order ID ", value=neworder["orderId"], inline=True)
                            await message.channel.send(embed=embed_message)
                            delete_deal(config, pair)
                    else:
                        await message.channel.send(f"Error creating order {pair}")
                except BinanceAPIException as e:
                    await message.channel.send(f"Error creating order **{pair}** and error is : **{e}**")

            except IndexError:
                await message.channel.send(f"I'm Working but i got some **internal error**")
            except ValueError:
                await message.channel.send(f"I'm Working but i got some internal error : "
                                           f" **Check the DATA you send**")

        elif user_message == "!stats":
            newtotals, Pnls, pairs, pnls, avgs = [], [], [], [], []
            for pair in get_deals(config):
                total = (float(get_qnty(config, pair)) * float(get_avg_price(config, pair)))
                avg_price = float(get_avg_price(config, pair))
                newtotal = (float(get_qnty(config, pair)) * float(b_client.get_symbol_ticker(symbol=pair)["price"]))
                Pnl = float(newtotal) - float(total)
                newtotals.append(f"${round(avg_price, 4)} | ${round(total, 2)} | ${round(newtotal, 2)}")
                pairs.append(pair)
                pnlZ = round((newtotal - total) / total * 100, 2)
                Pnls.append(f"${round(Pnl, 2)} | {pnlZ}%")
            order_Pairs = '\n'.join(map(str, pairs))
            order_newtotal = '\n'.join(map(str, newtotals))
            order_Pnl = '\n'.join(map(str, Pnls))

            embed_message = discord.Embed(title="Deals Stats",
                                          description=f"**Your Account - PNL Report**",
                                          color=discord.Color.random())
            embed_message.add_field(name="Pair", value=f"```CSS\n{order_Pairs}```\n", inline=True)
            embed_message.add_field(name="Deal Value", value=f"```CSS\n{order_newtotal}```\n", inline=True)
            embed_message.add_field(name="PNL", value=f"```CSS\n{order_Pnl}```\n", inline=True)
            if len(newtotals) > 0:
                await message.channel.send(embed=embed_message)
            else:
                await message.channel.send("Sorry No Deals are open")
    else:
        if (user_message.startswith("!stats") or user_message.startswith("!dca") or user_message.startswith("!new")
                or user_message.startswith("!close")):
            await message.channel.send("Sorry You are not allowed")
        else:
            if allowed == 0 and user_message == "!info":
                msg = f"**Username** : {username}\n" \
                      f"**User ID** : {userid}\n" \
                      f"**Guild ID** : {message.guild.id}\n" \
                      f"**Channel id** : {message.channel.id}\n"
                embed_message = discord.Embed(title="Server Info", description=msg, color=discord.Color.random())
                await message.channel.send(embed=embed_message)


dis.run(TOKEN)
