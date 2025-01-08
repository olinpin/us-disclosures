import sqlite3


class DB:
    def __init__(self, db_path, schema_path="schema.sql", seed_path="seed.sql"):
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        with open(schema_path) as f:
            self.cur.executescript(f.read())

        with open(seed_path) as f:
            self.cur.executescript(f.read())

    def __del__(self):
        self.con.close()

    def query(self, query, params=[]):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def insertDisclosures(self, disclosures):
        sql = "INSERT INTO disclosures (member_id, filing_year, filing, link) VALUES (?, ?, ?, ?)"
        self.cur.executemany(sql, disclosures)
        self.con.commit()
