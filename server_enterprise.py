# -*- coding: utf-8 -*-
# POKI MEGA ENTERPRISE - BACKEND SERVER
# إدارة وتطوير وإشراف هندسي: أبو العز العمري
import os, sqlite3, hashlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Poki Mega Enterprise", version="2026.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DB = "poki_enterprise_master.db"

def init_db():
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    dev_name TEXT, 
                    title TEXT, 
                    link TEXT, 
                    year TEXT, 
                    category TEXT, 
                    status TEXT, 
                    score INTEGER DEFAULT 0
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    email TEXT UNIQUE, 
                    password TEXT, 
                    points INTEGER DEFAULT 150
                )''')
    db.commit()
    db.close()

init_db()

class GameModel(BaseModel):
    dev_name: str
    title: str
    link: str
    year: str
    category: str

class AuthModel(BaseModel):
    email: str
    password: str

@app.post('/api/games/add')
def add_game(g: GameModel):
    db = sqlite3.connect(DB)
    c = db.cursor()
    c.execute('INSERT INTO games (dev_name, title, link, year, category, status, score) VALUES (?, ?, ?, ?, ?, ?, ?)', 
              (g.dev_name, g.title, g.link, g.year, g.category, 'قيد المراجعة', 0))
    db.commit()
    db.close()
    return {'success': True, 'message': 'تم إرسال اللعبة بنجاح وحفظها في قاعدة البيانات الدائمة!'}

@app.get('/api/games/all')
def get_all_games():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute('SELECT * FROM games ORDER BY id DESC')
    res = [dict(r) for r in c.fetchall()]
    db.close()
    return res

@app.post('/api/admin/action')
def admin_action(d: dict):
    gid = d.get('id')
    action = d.get('action')
    db = sqlite3.connect(DB)
    c = db.cursor()
    if action == 'approve':
        c.execute('UPDATE games SET status = "تمت الموافقة" WHERE id = ?', (gid,))
    elif action == 'reject':
        c.execute('UPDATE games SET status = "مرفوضة" WHERE id = ?', (gid,))
    elif action == 'delete':
        c.execute('DELETE FROM games WHERE id = ?', (gid,))
    db.commit()
    db.close()
    return {'success': True}

@app.post('/api/auth/register')
def register(u: AuthModel):
    try:
        db = sqlite3.connect(DB)
        c = db.cursor()
        hashed_pass = hashlib.sha256(u.password.encode()).hexdigest()
        c.execute('INSERT INTO users (email, password, points) VALUES (?, ?, ?)', (u.email, hashed_pass, 150))
        db.commit()
        db.close()
        return {'success': True, 'message': 'تم إنشاء الحساب بنجاح ومنحك 150 نقطة ترحيبية!'}
    except:
        return {'success': False, 'message': 'البريد الإلكتروني مسجل مسبقاً!'}

@app.post('/api/auth/login')
def login(u: AuthModel):
    db = sqlite3.connect(DB)
    c = db.cursor()
    hashed_pass = hashlib.sha256(u.password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE email = ? AND password = ?', (u.email, hashed_pass))
    res = c.fetchone()
    db.close()
    if res:
        return {'success': True, 'message': 'تم تسجيل الدخول بنجاح!'}
    raise HTTPException(status_code=401, detail='بيانات الدخول غير صحيحة!')

@app.get('/api/leaderboard')
def leaderboard():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    c.execute('SELECT email, points FROM users ORDER BY points DESC LIMIT 10')
    res = [dict(r) for r in c.fetchall()]
    db.close()
    return res

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Frontend index.html not found!</h1>"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_enterprise:app", host="127.0.0.1", port=8000, reload=True)
