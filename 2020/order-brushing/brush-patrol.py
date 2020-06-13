#!/usr/bin/python3

import csv
import psycopg2
from collections import OrderedDict
from configparser import ConfigParser
from datetime import timedelta

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_shops(cur):
    cur.execute("SELECT DISTINCT shopid FROM orders")

    data = cur.fetchall()
    shops = []

    for datum in data:
        shops.append(datum[0])

    return shops

def get_orders(cur, shopid):
    cur.execute("SELECT * FROM orders WHERE shopid = %s", (shopid,))

    data = cur.fetchall()
    orders = []

    for datum in data:
        formatted_datum = {
            "orderid": datum[0],
            "shopid": datum[1],
            "userid": datum[2],
            "event_time": datum[3],
        }
        orders.append(formatted_datum)

    return orders

def get_next_1h_orders(cur, order):
    shopid = order["shopid"]
    event_time = order["event_time"]
    next_1h_event_time = event_time + timedelta(hours = 1)

    cur.execute("""
        SELECT *
        FROM orders
        WHERE
            shopid = %s
        AND
            event_time BETWEEN %s AND %s
    """, (shopid, event_time, next_1h_event_time))

    data = cur.fetchall()
    next_1h_orders = []

    for datum in data:
        formatted_datum = {
            "orderid": datum[0],
            "shopid": datum[1],
            "userid": datum[2],
            "event_time": datum[3],
        }
        next_1h_orders.append(formatted_datum)

    return next_1h_orders

if __name__ == '__main__':
    try:
        params = config()
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        shops = get_shops(cur)
        answer = {}

        for shop in shops:
            print("Checking shopid", shop)

            orders = get_orders(cur, shop)
            suspects = {}

            for order in orders:
                print("  Checking orderid", order["orderid"])

                next_1h_orders = get_next_1h_orders(cur, order)

                proportions = {}
                max_freq = 0

                for next_order in next_1h_orders:
                    if not next_order["userid"] in proportions:
                        proportions[next_order["userid"]] = 0

                    proportions[next_order["userid"]] += 1

                    max_freq = max(max_freq, proportions[next_order["userid"]])

                total_order = len(next_1h_orders)
                unique_users = len(proportions)
                concentrate_rate = total_order / unique_users

                if concentrate_rate >= 3:
                    for user, freq in proportions.items():
                        if freq == max_freq:
                            if (not user in suspects) or (freq > suspects[user]):
                                suspects[user] = freq

            max_freq = 0
            for _, freq in suspects.items():
                max_freq = max(max_freq, freq)

            real_suspects = []
            for suspect, freq in suspects.items():
                if freq == max_freq:
                    real_suspects.append(suspect)

            print("  Suspect(s) for this shop are:")
            print("   ", real_suspects)

            real_suspects.sort()
            answer[shop] = real_suspects

        cur.close()
        conn.close()

        sorted_answer = OrderedDict(sorted(answer.items()))

        with open('busted.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['shopid', 'userid'])

            for shopid, suspects in sorted_answer.items():
                sorted_suspects = [str(suspect) for suspect in suspects]
                formatted_suspects = 0 if len(sorted_suspects) == 0 else "&".join(sorted_suspects)

                writer.writerow([shopid, formatted_suspects])
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
