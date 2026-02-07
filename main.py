from fastapi import FastAPI, HTTPException
from database import init_db, get_db
from models import User, Lead
from auth import hash_password, verify_password, create_token
from datetime import datetime

app = FastAPI(title="CREATIVE API")

@app.get("/")
def root():
    return {"status": "CREATIVE API ONLINE 🚀"}

# ========== REGISTER ==========
@app.post("/register")
def register(user: User):
    conn = get_db()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (NULL,?,?,?)",
                  (user.username, hash_password(user.password), "admin"))
        conn.commit()
        return {"status": "ok"}
    except:
        raise HTTPException(400, "User already exists")

# ========== LOGIN ==========
@app.post("/login")
def login(user: User):
    conn = get_db()
    c = conn.cursor()

    db_user = c.execute("SELECT * FROM users WHERE username=?", (user.username,)).fetchone()
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({"user": user.username})
    return {"token": token}

# ========== CREATE LEAD ==========
@app.post("/lead")
def create_lead(lead: Lead):
    score = 0
    if lead.phone: score += 20
    if lead.email: score += 20
    if lead.company: score += 20
    if lead.city: score += 10

    conn = get_db()
    c = conn.cursor()

    c.execute("""
        INSERT INTO leads VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        lead.name,
        lead.phone,
        lead.email,
        lead.company,
        lead.city,
        lead.niche,
        lead.source,
        lead.status,
        score,
        lead.notes,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    return {"status": "Lead saved", "score": score}

# ========== LIST LEADS ==========
@app.get("/leads")
def list_leads():
    conn = get_db()
    rows = conn.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]

# ========== DASHBOARD ==========
@app.get("/dashboard")
def dashboard():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    hot = conn.execute("SELECT COUNT(*) FROM leads WHERE score >= 70").fetchone()[0]

    return {
        "total_leads": total,
        "hot_leads": hot
    }
