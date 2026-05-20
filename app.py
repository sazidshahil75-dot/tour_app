from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "tour_db"),
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ---------- routes ----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/trips", methods=["GET"])
def list_trips():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT t.*, COUNT(p.id) AS tourist_count
        FROM trips t
        LEFT JOIN tourists p ON p.trip_id = t.id
        GROUP BY t.id
        ORDER BY t.created_at DESC
    """)
    trips = cur.fetchall()
    for tr in trips:
        if isinstance(tr.get("created_at"), datetime):
            tr["created_at"] = tr["created_at"].strftime("%d %b %Y")
    cur.close(); db.close()
    return jsonify(trips)


@app.route("/api/trips", methods=["POST"])
def create_trip():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO trips
          (destination, duration_days, transport_type, transport_detail,
           cost_transport, cost_hotel, cost_food, cost_tickets,
           cost_guide, cost_misc, split_method, total_cost)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["destination"], data["duration_days"],
        data["transport_type"], data.get("transport_detail",""),
        data["cost_transport"], data["cost_hotel"],
        data["cost_food"], data["cost_tickets"],
        data["cost_guide"], data["cost_misc"],
        data["split_method"], data["total_cost"],
    ))
    trip_id = cur.lastrowid

    for t in data.get("tourists", []):
        cur.execute("""
            INSERT INTO tourists (trip_id, name, share_pct, share_amount)
            VALUES (%s, %s, %s, %s)
        """, (trip_id, t["name"], t["share_pct"], t["share_amount"]))

    db.commit()
    cur.close(); db.close()
    return jsonify({"id": trip_id, "message": "Trip saved!"})


@app.route("/api/trips/<int:trip_id>", methods=["GET"])
def get_trip(trip_id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM trips WHERE id=%s", (trip_id,))
    trip = cur.fetchone()
    if not trip:
        cur.close(); db.close()
        return jsonify({"error": "Not found"}), 404
    if isinstance(trip.get("created_at"), datetime):
        trip["created_at"] = trip["created_at"].strftime("%d %b %Y")
    cur.execute("SELECT * FROM tourists WHERE trip_id=%s ORDER BY id", (trip_id,))
    trip["tourists"] = cur.fetchall()
    cur.close(); db.close()
    return jsonify(trip)


@app.route("/api/trips/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM tourists WHERE trip_id=%s", (trip_id,))
    cur.execute("DELETE FROM trips WHERE id=%s", (trip_id,))
    db.commit()
    cur.close(); db.close()
    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
