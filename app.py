import os
import sqlite3
import secrets
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = os.environ.get("CAMPUSFIND_SECRET", "campusfind-change-this-secret")
app.config["DATABASE"] = os.path.join(BASE_DIR, "campusfind.db")
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

CATEGORIES = ["Devices/Electronics", "Books", "Bags", "Clothing", "Accessories", "Other"]
DEPARTMENTS = ["BCA", "BBA", "CS IT", "VISCOM", "BCOM"]
COLORS = ["Black", "White", "Red", "Blue", "Green", "Silver", "Other"]
LOCATIONS = ["Library", "Canteen", "Classroom", "Ground", "Parking", "Other"]


def db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        department TEXT,
        year TEXT,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        item_type TEXT NOT NULL CHECK(item_type IN ('lost','found')),
        category TEXT NOT NULL,
        department TEXT,
        color TEXT,
        location TEXT,
        description TEXT,
        image TEXT,
        poster_id TEXT NOT NULL,
        poster_name TEXT NOT NULL,
        poster_phone TEXT,
        poster_email TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(poster_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS favorites (
        user_id TEXT NOT NULL,
        item_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        PRIMARY KEY(user_id, item_id),
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        item_id INTEGER,
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()


def next_user_id(conn):
    while True:
        uid = f"CF-{secrets.token_hex(3).upper()}"
        if conn.execute("SELECT 1 FROM users WHERE id=?", (uid,)).fetchone() is None:
            return uid


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    conn = db()
    row = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return row


@app.context_processor
def inject_user():
    user = current_user()
    return {"current_user": user, "categories": CATEGORIES, "departments": DEPARTMENTS, "colors": COLORS, "locations": LOCATIONS}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def serialize_item(row, user_id=None, include_private=False):
    item = dict(row)
    item["is_favorite"] = False
    if user_id:
        item["is_favorite"] = bool(row["favorite_count"]) if "favorite_count" in row.keys() else False
    if not include_private:
        item.pop("poster_phone", None)
        item.pop("poster_email", None)
    return item


@app.route("/login")
def login():
    if session.get("user_id"):
        return redirect(url_for("index"))
    return render_template("login.html", mode=request.args.get("mode", "login"))


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    department = request.form.get("department", "").strip()
    year = request.form.get("year", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    if not name or not email or not password:
        flash("Name, email and password are required.", "error")
        return redirect(url_for("login", mode="register"))
    if password != confirm:
        flash("Passwords do not match.", "error")
        return redirect(url_for("login", mode="register"))
    if len(password) < 6:
        flash("Password must contain at least 6 characters.", "error")
        return redirect(url_for("login", mode="register"))

    conn = db()
    try:
        uid = next_user_id(conn)
        conn.execute(
            """INSERT INTO users(id,name,email,phone,department,year,password_hash,created_at)
               VALUES(?,?,?,?,?,?,?,?)""",
            (uid, name, email, phone, department, year, generate_password_hash(password), datetime.now().isoformat())
        )
        conn.commit()
        session.clear()
        session["user_id"] = uid
        flash("Account created successfully.", "success")
        return redirect(url_for("index"))
    except sqlite3.IntegrityError:
        flash("That email is already registered. Please log in.", "error")
        return redirect(url_for("login", mode="login"))
    finally:
        conn.close()


@app.route("/login", methods=["POST"])
def do_login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    conn = db()
    user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid email or password.", "error")
        return redirect(url_for("login", mode="login"))
    session.clear()
    session["user_id"] = user["id"]
    return redirect(request.form.get("next") or url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/api/items")
@login_required
def api_items():
    user_id = session["user_id"]
    conn = db()
    rows = conn.execute("""
        SELECT i.*,
               EXISTS(SELECT 1 FROM favorites f WHERE f.item_id=i.id AND f.user_id=?) AS is_favorite,
               (SELECT COUNT(*) FROM favorites f2 WHERE f2.item_id=i.id) AS favorite_count
        FROM items i
        ORDER BY RANDOM()
    """, (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/items/<int:item_id>")
@login_required
def api_item(item_id):
    conn = db()
    row = conn.execute("""
        SELECT i.*,
               EXISTS(SELECT 1 FROM favorites f WHERE f.item_id=i.id AND f.user_id=?) AS is_favorite,
               (SELECT COUNT(*) FROM favorites f2 WHERE f2.item_id=i.id) AS favorite_count
        FROM items i WHERE i.id=?
    """, (session["user_id"], item_id)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(dict(row))


@app.route("/api/items", methods=["POST"])
@login_required
def create_item():
    form = request.form
    title = form.get("title", "").strip()
    item_type = form.get("item_type", "lost").lower()
    category = form.get("category", "").strip()
    department = form.get("department", "").strip()
    color = form.get("color", "").strip()
    location = form.get("location", "").strip()
    description = form.get("description", "").strip()
    image_name = None

    if item_type not in {"lost", "found"}:
        return jsonify({"error": "Invalid item type."}), 400
    if not title or not category:
        return jsonify({"error": "Item name and category are required."}), 400

    uploaded = request.files.get("image")
    if uploaded and uploaded.filename:
        if not allowed_file(uploaded.filename):
            return jsonify({"error": "Only image files are allowed."}), 400
        safe = secure_filename(uploaded.filename)
        image_name = f"{secrets.token_hex(6)}_{safe}"
        uploaded.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))

    user = current_user()
    conn = db()
    cur = conn.execute("""
        INSERT INTO items(title,item_type,category,department,color,location,description,image,
                          poster_id,poster_name,poster_phone,poster_email,created_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (title, item_type, category, department, color, location, description, image_name,
          user["id"], user["name"], user["phone"], user["email"], datetime.now().isoformat()))
    item_id = cur.lastrowid

    # Notify the poster when a new opposite-type item is posted with a matching category.
    opposite = "found" if item_type == "lost" else "lost"
    matches = conn.execute(
        "SELECT poster_id FROM items WHERE item_type=? AND category=? AND id<>? GROUP BY poster_id",
        (opposite, category, item_id)
    ).fetchall()
    for m in matches:
        conn.execute(
            "INSERT INTO notifications(user_id,title,message,item_id,created_at) VALUES(?,?,?,?,?)",
            (m["poster_id"], "Possible match found", f"A new {item_type} item in {category} was posted.", item_id, datetime.now().isoformat())
        )
    conn.commit()
    row = conn.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@app.route("/api/items/<int:item_id>/favorite", methods=["POST"])
@login_required
def toggle_favorite(item_id):
    uid = session["user_id"]
    conn = db()
    exists = conn.execute("SELECT 1 FROM items WHERE id=?", (item_id,)).fetchone()
    if not exists:
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    fav = conn.execute("SELECT 1 FROM favorites WHERE user_id=? AND item_id=?", (uid, item_id)).fetchone()
    if fav:
        conn.execute("DELETE FROM favorites WHERE user_id=? AND item_id=?", (uid, item_id))
        active = False
    else:
        conn.execute("INSERT INTO favorites(user_id,item_id,created_at) VALUES(?,?,?)", (uid, item_id, datetime.now().isoformat()))
        active = True
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM favorites WHERE item_id=?", (item_id,)).fetchone()[0]
    conn.close()
    return jsonify({"favorite": active, "count": count})


@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def profile_api():
    uid = session["user_id"]
    if request.method == "GET":
        user = current_user()
        return jsonify({k: user[k] for k in ["id","name","email","phone","department","year","created_at"]})

    data = request.form
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    department = data.get("department", "").strip()
    year = data.get("year", "").strip()
    if not name or not email:
        return jsonify({"error": "Name and email are required."}), 400

    conn = db()
    try:
        conn.execute(
            "UPDATE users SET name=?, email=?, phone=?, department=?, year=? WHERE id=?",
            (name, email, phone, department, year, uid)
        )
        conn.execute(
            "UPDATE items SET poster_name=?, poster_phone=?, poster_email=? WHERE poster_id=?",
            (name, phone, email, uid)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "That email is already used by another account."}), 400
    conn.close()
    return jsonify({"success": True})


@app.route("/api/notifications")
@login_required
def notifications():
    conn = db()
    rows = conn.execute(
        "SELECT * FROM notifications WHERE user_id=? ORDER BY id DESC LIMIT 20",
        (session["user_id"],)
    ).fetchall()
    unread = conn.execute(
        "SELECT COUNT(*) FROM notifications WHERE user_id=? AND is_read=0",
        (session["user_id"],)
    ).fetchone()[0]
    conn.close()
    return jsonify({"items": [dict(r) for r in rows], "unread": unread})


@app.route("/api/notifications/read", methods=["POST"])
@login_required
def notifications_read():
    conn = db()
    conn.execute("UPDATE notifications SET is_read=1 WHERE user_id=?", (session["user_id"],))
    conn.commit()
    conn.close()
    return jsonify({"success": True})


@app.route("/api/my-items")
@login_required
def my_items():
    conn = db()
    rows = conn.execute(
        "SELECT * FROM items WHERE poster_id=? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
