import sqlite3 as sql

con = sql.connect('auto.db')
with con:
    cur = con.cursor()

    #
    # cur.execute("""CREATE TABLE IF NOT EXISTS auto(
    #    id INT PRIMARY KEY,
    #    brand TEXT,
    #    model TEXT,
    #    company TEXT);
    # """)
    #
    # cur.execute("""CREATE TABLE IF NOT EXISTS price(
    #          id INT PRIMARY KEY,
    #          auto_id INT,
    #          price TEXT,
    #          FOREIGN  KEY (auto_id) REFERENCES auto (id)
    #          );
    #       """)

    # records_to_insert = [(2, 'Audi', 'A6', 'Deutsche Auto'),
    #                      (3, 'Audi', 'A5', 'Deutsche Auto'),
    #                      (4, 'Mercedes', 'C-class', 'Deutsche Auto'),
    #                      (5, 'Mercedes', 'S-class', 'Deutsche Auto'),
    #                      (6, 'Mercedes', 'E-class', 'Deutsche Auto'),
    #                      (7, 'Mercedes', 'D-class', 'Deutsche Auto'),
    #                      (8, 'Skoda', 'SuperB', 'Czech Auto'),
    #                      (9, 'Skoda', 'Octavia', 'Czech Auto'),
    #                      (10, 'BMW', '3series', 'Deutsche Auto'),
    #                      (11, 'BMW', '6series', 'Deutsche Auto'),
    #                      (12, 'Honda', 'Civic', 'Japan Auto'),
    #                      (13, 'Honda', 'Accord', 'Japan Auto'),
    #                      (14, 'Acura', 'TLX', 'Japan Auto'),
    #                      (15, 'BMW', 'M5', 'Deutsche Auto'),
    #                      (16, 'BMW', 'M6', 'Deutsche Auto')
    #                      ]
    #
    # cur.executemany('insert into auto values (?,?,?,?)', records_to_insert)

    # records_to_insert_p = [(1, 1, '25000'),
    #                       (2, 16, '23000'),
    #                       (3, 10, '25000'),
    #                       (4, 12, '235000'),
    #                       (5, 13, '66000'),
    #                       (6, 14, '24000'),
    #                       (7, 15, '10000'),
    #                       (8, 9, '21300'),
    #                       (9, 8, '25050'),
    #                       (10, 7, '252300'),
    #                       (11, 6, '25000'),
    #                       (12, 5, '26000'),
    #                       (13, 4, '27000'),
    #                       (14, 3, '28000'),
    #                       (15, 2, '21000'),
    #                       (16, 11, '25030'),
    #                      ]
    #
    # cur.executemany('insert into price values (?,?,?)', records_to_insert_p)





    con.commit()






