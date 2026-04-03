from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB = "expenses.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        with open("schema.sql") as f:
            conn.executescript(f.read())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    conn = get_db()
    rows = conn.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/transactions", methods=["POST"])
def add_transaction():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO transactions (amount, description, category_id, date) VALUES (?, ?, ?, ?)",
        (data["amount"], data["description"], data.get("category_id"), data["date"])
    )
    conn.commit()
    return jsonify({"message": "Transaction added"}), 201

if __name__ == "__main__":
    init_db()
    app.run(debug=True)