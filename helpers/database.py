import sqlite3
import random


def add_deals(cfg, deal, orderid, qnty, avg_price):
    """Add Deals to offline Database"""

    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    dbcursor.execute('''CREATE TABLE IF NOT EXISTS deals
              (dealpair TEXT, orderid TEXT , qnty NUMERIC, avg_price NUMERIC)'''
                     )
    try:
        if dbcursor.execute(f"SELECT dealpair FROM deals WHERE dealpair = '{deal}'").fetchone()[0]:
            pass
    except sqlite3.OperationalError as e:
        pass
    except IndexError as e:
        pass
    except TypeError as e:
        pass
        dbcursor.execute(
            "INSERT INTO deals ('dealpair', 'orderid', 'qnty', 'avg_price')"
            f"VALUES ('{deal}', '{orderid}', '{qnty}', '{avg_price}')"
        )
        print(f"{deal} has been added to offline database -- Good luck ..")
        db.commit()
        db.close()


def delete_deal(cfg, deal):
    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    """Delete Deals to offline Database"""
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    dbcursor.execute('''CREATE TABLE IF NOT EXISTS deals
              (dealpair TEXT, orderid TEXT , qnty NUMERIC, avg_price NUMERIC, tp NUMERIC, status TEXT)'''
                     )
    try:
        if dbcursor.execute(f"SELECT dealpair FROM deals WHERE dealpair = '{deal}'").fetchone()[0]:
            dbcursor.execute(f"DELETE FROM deals WHERE dealpair = '{deal}'")
            db.commit()
            db.close()
            print(f"{deal} has been Deleted from offline database -- Good luck ..")

            pass
    except sqlite3.OperationalError as e:
        print(f"SQLite database error {e}")
        pass

    except IndexError as e:
        print(f"SQLite database error {e}")
        pass

    except TypeError as e:
        print(f"Deal not found in database :{e} , --Ignoring -- ")
        pass


def update_deal_values(cfg, deal, avg_price, qnty):
    """Update Deals in offline Database"""

    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    try:
        if dbcursor.execute(f"SELECT dealpair FROM deals WHERE dealpair = '{deal}'").fetchone()[0]:
            update_stmt = '''
            UPDATE deals
            SET avg_price = ? , qnty = ? 
            WHERE dealpair = ?;
            '''
            values = (avg_price, qnty, deal)
            dbcursor.execute(update_stmt, values)
            print(f"{deal} has been updated in the offline database")
            db.commit()
            db.close()
            pass

    except sqlite3.OperationalError as e:
        print(f"SQLite database error {e}")
        pass

    except IndexError as e:
        print(f"SQLite database error {e}")
        pass

    except TypeError as e:
        print(f"Deal not found in database , --Ignoring -- ")
        random.randint(687618, 9827267)
        dbcursor.execute(
            "INSERT INTO deals ('dealpair', 'orderid', 'qnty', 'avg_price')"
            f"VALUES ('{deal}', '{random.randint(687618, 9827267)}', '{qnty}', '{avg_price}')"
        )
        db.commit()
        db.close()
        pass


def get_qnty(cfg, deal):
    """Check how many deals are open and if they are less than MAX Deals in config INI"""
    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    try:
        if dbcursor.execute(f"SELECT dealpair FROM deals WHERE dealpair = '{deal}'").fetchone()[0]:
            qnty = db.execute(f"SELECT qnty FROM deals WHERE dealpair = '{deal}'").fetchone()[0]
            db.commit()
            db.close()
            return float(qnty)

    except sqlite3.OperationalError as e:
        pass

        return False

    except IndexError as e:
        pass
        return False
    except TypeError as e:
        print(f"Deal not found in database : {e} , --Ignoring -- ")
        pass


def get_orderid(cfg, deal):
    """Check how many deals are open and if they are less than MAX Deals in config INI"""
    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    try:
        if dbcursor.execute(f"SELECT dealpair FROM deals WHERE dealpair = '{deal}'").fetchone()[0]:
            orderid = db.execute(f"SELECT orderid FROM deals WHERE dealpair = '{deal}'").fetchone()[0]
            db.commit()
            db.close()
            return orderid

    except sqlite3.OperationalError as e:
        pass

        return False

    except IndexError as e:
        pass
        return False
    except TypeError as e:
        print(f"Deal not found in database : {e} , --Ignoring -- ")
        pass


def get_avg_price(cfg, deal):
    """Check how many deals are open and if they are less than MAX Deals in config INI"""
    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    try:
        if dbcursor.execute(f"SELECT dealpair FROM deals WHERE dealpair = '{deal}'").fetchone()[0]:
            price = db.execute(f"SELECT avg_price FROM deals WHERE dealpair = '{deal}'").fetchone()[0]
            db.commit()
            db.close()
            return float(price)
    except sqlite3.OperationalError as e:
        pass
        return False

    except IndexError as e:
        pass
        return False
    except TypeError as e:
        print(f"Deal not found in database : {e} , --Ignoring -- ")
        pass


def get_deals(cfg):
    """GET DEALS"""
    pairs = []
    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    data = dbcursor.execute(f"SELECT dealpair FROM deals").fetchall()
    for pair in data:
        pairs.append(pair[0])
    return pairs


def check_deal(cfg, pair):
    """GET DEALS"""
    pairs = []
    dbname = f'{cfg.get("settings", "database-name")}.sqlite3'
    db = sqlite3.connect(dbname)
    dbcursor = db.cursor()
    try:
        data = dbcursor.execute(f"SELECT qnty FROM deals WHERE dealpair = '{pair}'").fetchone()[0]
        if data:
            return True
    except sqlite3.OperationalError as e:
        pass
        return False

    except IndexError as e:
        pass
        return False
    except TypeError as e:
        print(f"Deal not found in database : {e} , --Ignoring -- ")
        pass
        return False
