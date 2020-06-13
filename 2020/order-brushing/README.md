# Order Brushing

A data analytics challenge by Shopee Code League 2020.

We are participated in this challenge as AnakRantauMenderita.

## Requirements

* Python ^= 3.6.9
* pip ^= 9.0.1 (Python 3.6)
* psql (PostgreSQL) ^= 10.12
* psycopg2 ^= 2.8.5

Please run `pip3 install -r requirements.txt`.

## How to Reproduce

First, you need to prepare the database.
Create a database first and then fill out `database.ini` configuration
by copying `database.ini.sample` into a new file named `database.ini`.
The command is `cp database.ini.sample database.ini`.

Next, login to your `psql` and then run all the queries in the `orders.sql`.

The data in the `order_brush_order.csv` should have imported to your database.

You may now run `brush-patrol.py` by running `python3 brush-patrol.py` command
(or `python brush-patrol.py` if your default Python version is 3.6).
Wait until it is finished.

Lastly, when the program is finished, `busted.csv` should have created.
You can now submit it!

## Scores

This approach achieved **0.89933** scores.

## Why Using DBMS?

We are using DBMS such as PostgreSQL to ease the needs of querying data.
As you may see that this challenge is relying on time range to solve the
problem.
The run time also quite fast than processing it directly.

## License

The ugly code is licensed under [The MIT License](LICENSE).
