CREATE TABLE orders (
  orderid BIGINT PRIMARY KEY,
  shopid INTEGER,
  userid INTEGER,
  event_time TIMESTAMP
);

CREATE INDEX shopid_idx ON orders (shopid);
CREATE INDEX userid_idx ON orders (userid);

\COPY orders FROM 'order_brush_order.csv' DELIMITER ',' CSV HEADER;

