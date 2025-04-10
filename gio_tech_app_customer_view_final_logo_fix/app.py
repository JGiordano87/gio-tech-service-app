
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "contracts.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    con = get_db()
    contracts = con.execute("SELECT id, name FROM contracts").fetchall()
    return render_template("index.html", contracts=contracts)

@app.route("/contract/<int:id>")
def view_contract(id):
    con = get_db()
    contract = con.execute("SELECT * FROM contracts WHERE id=?", (id,)).fetchone()
    return render_template("detail.html", contract=contract)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        data = request.form
        con = get_db()
        con.execute("""INSERT INTO contracts (name, address, email, phone, start_date, due_months, notes, renewal_date)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                      (data["name"], data["address"], data["email"], data["phone"],
                       data["start_date"], data["due_months"], data["notes"], data["renewal_date"]))
        con.commit()
        return redirect("/")
    return render_template("form.html")

@app.route("/delete/<int:id>")
def delete(id):
    con = get_db()
    con.execute("DELETE FROM contracts WHERE id=?", (id,))
    con.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    con = get_db()
    if request.method == "POST":
        data = request.form
        con.execute("""UPDATE contracts SET name=?, address=?, email=?, phone=?, start_date=?, due_months=?, notes=?, renewal_date=?
                      WHERE id=?""",
                      (data["name"], data["address"], data["email"], data["phone"],
                       data["start_date"], data["due_months"], data["notes"], data["renewal_date"], id))
        con.commit()
        return redirect("/")
    contract = con.execute("SELECT * FROM contracts WHERE id=?", (id,)).fetchone()
    return render_template("form.html", contract=contract)

if __name__ == "__main__":
    import os
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as con:
            con.execute("""CREATE TABLE contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, address TEXT, email TEXT, phone TEXT,
                start_date TEXT, due_months TEXT, notes TEXT, renewal_date TEXT
            )""")
    app.run(debug=True)
