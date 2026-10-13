import sqlite3, json, pathlib
DB="datascout.db"
def init_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, query TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP, results TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS saved (id TEXT PRIMARY KEY, title TEXT, url TEXT)")
    con.commit(); con.close()
def save_search(query, results):
    init_db()
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO history (query, results) VALUES (?,?)",(query, json.dumps(results[:3])))
    con.commit(); con.close()
def get_history(limit=10):
    init_db()
    con=sqlite3.connect(DB)
    cur=con.execute("SELECT query, ts FROM history ORDER BY ts DESC LIMIT ?", (limit,))
    rows=cur.fetchall(); con.close(); return rows