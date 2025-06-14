import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import json
import os
import time
import random
import hashlib
import math

# ตรวจสอบและ import libraries เพิ่มเติม
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# PWA-Ready Configuration (ต้องเป็นคำสั่ง Streamlit แรกสุด)
st.set_page_config(
    page_title="💰 Personal Financial App - Multi-User",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PWA Features และ CSS
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#1e3a8a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Financial App">

<style>
/* PWA Mobile Optimization */
@media (max-width: 768px) {
    .main-header h1 { font-size: 1.3em; }
    .main-header p { font-size: 0.9em; }
    .stButton button { 
        height: 48px; 
        font-size: 16px; 
        border-radius: 8px;
        width: 100%;
        margin: 5px 0;
    }
    .stMetric { 
        background: #f8fafc; 
        padding: 10px; 
        border-radius: 8px; 
        margin: 5px 0;
        text-align: center;
    }
}

/* Hide Streamlit elements for PWA */
.stDeployButton { display: none; }
header[data-testid="stHeader"] { display: none; }
footer { display: none; }

/* PWA Install Button */
.pwa-install-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #1e3a8a;
    color: white;
    border: none;
    padding: 12px 16px;
    border-radius: 25px;
    font-size: 14px;
    cursor: pointer;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    display: none;
}

.pwa-status {
    position: fixed;
    top: 10px;
    right: 10px;
    background: #10b981;
    color: white;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
    z-index: 1000;
}

/* CSS เดิมของคุณ */
.main-header {
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}

.streaming-live {
    background: #ef4444;
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8em;
    animation: pulse 2s infinite;
    display: inline-block;
    margin-left: 10px;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.portfolio-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.price-up {
    color: #16a34a !important;
    font-weight: bold;
}

.price-down {
    color: #dc2626 !important;
    font-weight: bold;
}

.price-neutral {
    color: #6b7280 !important;
}

.auth-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 30px 25px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    border: 2px solid #e2e8f0;
}

.register-highlight {
    background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    border-left: 4px solid #38a169;
}

.dca-calculator {
    background: linear-gradient(135deg, #f3e8ff 0%, #e0e7ff 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
}

.stock-tracker-card {
    background: linear-gradient(135deg, #fff7ed 0%, #fef3c7 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border-left: 5px solid #f59e0b;
}

.averaging-down-card {
    background: linear-gradient(135deg, #fef7f7 0%, #fed7d7 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border-left: 5px solid #e53e3e;
}

.user-info {
    background: linear-gradient(135deg, #e6fffa 0%, #bee3f8 100%);
    padding: 10px 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>

<script>
console.log('🚀 PWA Features Loading...');

// PWA Service Worker
if ('serviceWorker' in navigator) {
    const swCode = `
        const CACHE_NAME = 'financial-app-v1';
        self.addEventListener('install', (event) => {
            self.skipWaiting();
        });
        self.addEventListener('activate', (event) => {
            self.clients.claim();
        });
        self.addEventListener('fetch', (event) => {
            event.respondWith(fetch(event.request));
        });
    `;
    
    const blob = new Blob([swCode], { type: 'application/javascript' });
    const swUrl = URL.createObjectURL(blob);
    
    navigator.serviceWorker.register(swUrl)
        .then(() => console.log('✅ PWA Service Worker registered'))
        .catch(() => console.log('❌ PWA Service Worker failed'));
}

// PWA Install Prompt
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    const installBtn = document.createElement('button');
    installBtn.className = 'pwa-install-btn';
    installBtn.innerHTML = '📱 ติดตั้งแอป';
    installBtn.style.display = 'block';
    
    installBtn.addEventListener('click', async () => {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            if (outcome === 'accepted') {
                installBtn.style.display = 'none';
                showPWAInstalled();
            }
            deferredPrompt = null;
        }
    });
    
    document.body.appendChild(installBtn);
});

function showPWAInstalled() {
    const statusDiv = document.createElement('div');
    statusDiv.className = 'pwa-status';
    statusDiv.innerHTML = '📱 PWA Mode';
    document.body.appendChild(statusDiv);
    setTimeout(() => statusDiv.style.display = 'none', 3000);
}

// PWA Detection
if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('🎉 Running as PWA!');
    document.addEventListener('DOMContentLoaded', () => {
        showPWAInstalled();
        document.body.style.overscrollBehavior = 'none';
    });
}

console.log('✅ PWA Features loaded successfully');
</script>
""", unsafe_allow_html=True)

# ฟังก์ชันสำหรับการเข้ารหัสรหัสผ่าน
def hash_password(password):
    """เข้ารหัสรหัสผ่านด้วย SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """ตรวจสอบรหัสผ่าน"""
    return hash_password(password) == hashed

# ฟังก์ชันจัดการผู้ใช้
def create_user(username, password, email):
    """สร้างผู้ใช้ใหม่"""
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    
    # ตรวจสอบว่า username ซ้ำหรือไม่
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        conn.close()
        return False, "ชื่อผู้ใช้นี้มีอยู่แล้ว"
    
    # สร้างผู้ใช้ใหม่
    try:
        hashed_password = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, password_hash, email, created_at)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_password, email, datetime.now()))
        conn.commit()
        conn.close()
        return True, "สร้างบัญชีสำเร็จ!"
    except Exception as e:
        conn.close()
        return False, f"เกิดข้อผิดพลาด: {str(e)}"

def authenticate_user(username, password):
    """ตรวจสอบการล็อกอิน"""
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(password, user[1]):
        return True, user[0]  # Return success and user_id
    return False, None

def get_user_info(user_id):
    """ดึงข้อมูลผู้ใช้"""
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, created_at FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# ฟังก์ชันดึงข้อมูลหุ้น
def get_real_stock_price_yahoo(symbol):
    """ดึงราคาหุ้นจริงจาก Yahoo Finance"""
    if not YFINANCE_AVAILABLE:
        return None
    
    try:
        # สำหรับหุ้นไทย เพิ่ม .BK
        thai_stocks = ["BBL", "KBANK", "SCB", "PTT", "PTTEP", "ADVANC", "TRUE", "CPALL", "CPN", "AOT", "BTS", "SCC", "TCAP", "TU", "MINT"]
        if symbol.upper() in thai_stocks:
            ticker_symbol = f"{symbol.upper()}.BK"
        else:
            ticker_symbol = symbol.upper()
        
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.history(period="1d", interval="1m")
        
        if not info.empty:
            current_price = info['Close'].iloc[-1]
            open_price = info['Open'].iloc[0]
            high_price = info['High'].max()
            low_price = info['Low'].min()
            volume = info['Volume'].sum()
            
            change = current_price - open_price
            change_percent = (change / open_price) * 100 if open_price > 0 else 0
            
            return {
                "symbol": symbol.upper(),
                "current_price": round(float(current_price), 2),
                "open_price": round(float(open_price), 2),
                "change": round(float(change), 2),
                "change_percent": round(float(change_percent), 2),
                "volume": int(volume),
                "high": round(float(high_price), 2),
                "low": round(float(low_price), 2),
                "last_updated": datetime.now()
            }
        else:
            return None
    except Exception as e:
        return None

def get_simulated_stock_data(symbol):
    """จำลองข้อมูลหุ้นแบบ real-time"""
    base_prices = {
        "BBL": 180.0, "KBANK": 140.0, "SCB": 100.0, "PTT": 35.0, "PTTEP": 120.0,
        "ADVANC": 200.0, "TRUE": 4.0, "CPALL": 60.0, "CPN": 50.0, "AOT": 70.0,
        "BTS": 8.0, "SCC": 400.0, "TCAP": 45.0, "TU": 15.0, "MINT": 30.0,
        "AAPL": 150.0, "GOOGL": 2500.0, "MSFT": 300.0, "TSLA": 200.0, "NVDA": 400.0
    }
    
    base_price = base_prices.get(symbol.upper(), 50.0)
    change_percent = random.uniform(-3, 3)
    current_price = base_price * (1 + change_percent/100)
    open_price = base_price
    
    volume = random.randint(1000000, 10000000)
    high = current_price * random.uniform(1.001, 1.03)
    low = current_price * random.uniform(0.97, 0.999)
    
    return {
        "symbol": symbol.upper(),
        "current_price": round(current_price, 2),
        "open_price": round(open_price, 2),
        "change": round(current_price - open_price, 2),
        "change_percent": round(change_percent, 2),
        "volume": volume,
        "high": round(high, 2),
        "low": round(low, 2),
        "last_updated": datetime.now()
    }

def get_stock_data(symbol, use_real_data=True):
    """ดึงข้อมูลหุ้น - ใช้ข้อมูลจริงหรือจำลอง"""
    if use_real_data:
        real_data = get_real_stock_price_yahoo(symbol)
        if real_data:
            return real_data
    return get_simulated_stock_data(symbol)

# ฟังก์ชันคำนวณการถั่วหุ้น
def calculate_averaging_down(existing_shares, existing_avg_price, new_shares, new_price):
    """คำนวณการถั่วหุ้น (Averaging Down)"""
    total_shares = existing_shares + new_shares
    total_cost = (existing_shares * existing_avg_price) + (new_shares * new_price)
    new_avg_price = total_cost / total_shares
    
    return {
        "total_shares": total_shares,
        "new_avg_price": new_avg_price,
        "total_cost": total_cost,
        "cost_reduction": existing_avg_price - new_avg_price,
        "cost_reduction_percent": ((existing_avg_price - new_avg_price) / existing_avg_price) * 100
    }

# ฟังก์ชันคำนวณ DCA
def calculate_dca_strategy(symbol, current_price, target_amount, investment_per_period, periods):
    """คำนวณกลยุทธ์การถั่วเฉลี่ย (Dollar Cost Averaging)"""
    total_investment = investment_per_period * periods
    shares_per_period = investment_per_period / current_price
    total_shares = shares_per_period * periods
    average_price = total_investment / total_shares
    current_value = total_shares * current_price
    
    scenarios = []
    for price_change in [-20, -10, 0, 10, 20]:
        future_price = current_price * (1 + price_change/100)
        future_value = total_shares * future_price
        profit_loss = future_value - total_investment
        profit_percent = (profit_loss / total_investment) * 100
        
        scenarios.append({
            "price_change": price_change,
            "future_price": future_price,
            "future_value": future_value,
            "profit_loss": profit_loss,
            "profit_percent": profit_percent
        })
    
    return {
        "total_investment": total_investment,
        "shares_per_period": shares_per_period,
        "total_shares": total_shares,
        "average_price": average_price,
        "current_value": current_value,
        "current_profit_loss": current_value - total_investment,
        "scenarios": scenarios
    }

# ฟังก์ชันฐานข้อมูลพร้อม Migration
def init_database():
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    
    # สร้างตาราง users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ตรวจสอบและ migrate ตาราง transactions
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'user_id' not in columns and 'id' in columns:
        # ตารางเก่าที่ไม่มี user_id - ต้อง migrate
        st.warning("🔄 กำลังอัพเกรดฐานข้อมูลเพื่อรองรับ Multi-User System...")
        
        # สร้างตารางใหม่
        cursor.execute('''
            CREATE TABLE transactions_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL DEFAULT 1,
                date DATE NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # สร้าง default user หากไม่มี
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            default_password = hash_password("defaultpass123")
            cursor.execute('''
                INSERT INTO users (id, username, password_hash, email) 
                VALUES (1, 'legacy_user', ?, 'legacy@example.com')
            ''', (default_password,))
        
        # คัดลอกข้อมูลเก่า
        cursor.execute('''
            INSERT INTO transactions_new (date, type, category, amount, description, created_at)
            SELECT date, type, category, amount, description, created_at FROM transactions
        ''')
        
        # ลบตารางเก่าและเปลี่ยนชื่อ
        cursor.execute('DROP TABLE transactions')
        cursor.execute('ALTER TABLE transactions_new RENAME TO transactions')
        
        st.success("✅ อัพเกรดฐานข้อมูลสำเร็จ! ข้อมูลเก่าถูกรักษาไว้")
        st.info("🔑 ข้อมูลเก่าถูกกำหนดให้ผู้ใช้: `legacy_user` รหัสผ่าน: `defaultpass123`")
    
    elif 'user_id' not in columns:
        # สร้างตารางใหม่
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    
    # Migration สำหรับตารางอื่นๆ ด้วยวิธีเดียวกัน
    def migrate_table(table_name, create_sql):
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns and 'id' in columns:
            # ถ้ามีตารางเก่าแต่ไม่มี user_id
            cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        
        # สร้างตารางใหม่
        cursor.execute(create_sql)
    
    # Migrate ตารางอื่นๆ
    migrate_table('stocks', '''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            buy_price REAL NOT NULL,
            current_price REAL DEFAULT 0,
            dividend_rate REAL DEFAULT 0,
            buy_date DATE DEFAULT CURRENT_DATE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    migrate_table('goals', '''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL DEFAULT 0,
            target_date DATE,
            goal_type TEXT DEFAULT 'general',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # สร้างตารางใหม่ที่ไม่เคยมีมาก่อน
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS real_stock_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            quantity REAL NOT NULL,
            buy_price REAL NOT NULL,
            buy_date DATE NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS averaging_down_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            price REAL NOT NULL,
            transaction_date DATE NOT NULL,
            notes TEXT,
            running_avg_price REAL,
            running_total_shares REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dca_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            investment_per_period REAL NOT NULL,
            periods INTEGER NOT NULL,
            current_period INTEGER DEFAULT 0,
            start_date DATE NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # สร้างตาราง portfolio_history หากยังไม่มี
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER DEFAULT 1,
            symbol TEXT NOT NULL,
            price REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# ฟังก์ชันจัดการข้อมูลตามผู้ใช้
def add_real_stock(user_id, symbol, quantity, buy_price, buy_date, notes=""):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO real_stock_tracking (user_id, symbol, quantity, buy_price, buy_date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, symbol.upper(), quantity, buy_price, buy_date, notes))
    conn.commit()
    conn.close()

def get_real_stocks(user_id):
    conn = sqlite3.connect('financial_data.db')
    df = pd.read_sql_query('SELECT * FROM real_stock_tracking WHERE user_id = ? ORDER BY created_at DESC', conn, params=(user_id,))
    conn.close()
    return df

def delete_real_stock(user_id, stock_id):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM real_stock_tracking WHERE id = ? AND user_id = ?', (stock_id, user_id))
    conn.commit()
    conn.close()

def add_averaging_down_transaction(user_id, symbol, transaction_type, quantity, price, transaction_date, notes=""):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    
    # คำนวณค่าเฉลี่ยใหม่
    cursor.execute('''
        SELECT SUM(quantity), SUM(quantity * price) FROM averaging_down_transactions 
        WHERE user_id = ? AND symbol = ? AND transaction_type = 'buy'
    ''', (user_id, symbol))
    
    existing_data = cursor.fetchone()
    existing_shares = existing_data[0] if existing_data[0] else 0
    existing_total_cost = existing_data[1] if existing_data[1] else 0
    
    if transaction_type == 'buy':
        new_total_shares = existing_shares + quantity
        new_total_cost = existing_total_cost + (quantity * price)
        new_avg_price = new_total_cost / new_total_shares if new_total_shares > 0 else price
    else:  # sell
        new_total_shares = existing_shares - quantity
        new_total_cost = existing_total_cost - (quantity * (existing_total_cost / existing_shares if existing_shares > 0 else price))
        new_avg_price = new_total_cost / new_total_shares if new_total_shares > 0 else 0
    
    cursor.execute('''
        INSERT INTO averaging_down_transactions 
        (user_id, symbol, transaction_type, quantity, price, transaction_date, notes, running_avg_price, running_total_shares)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, symbol.upper(), transaction_type, quantity, price, transaction_date, notes, new_avg_price, new_total_shares))
    
    conn.commit()
    conn.close()

def get_averaging_down_transactions(user_id, symbol=None):
    conn = sqlite3.connect('financial_data.db')
    if symbol:
        df = pd.read_sql_query('''
            SELECT * FROM averaging_down_transactions 
            WHERE user_id = ? AND symbol = ? 
            ORDER BY transaction_date DESC, created_at DESC
        ''', conn, params=(user_id, symbol))
    else:
        df = pd.read_sql_query('''
            SELECT * FROM averaging_down_transactions 
            WHERE user_id = ? 
            ORDER BY transaction_date DESC, created_at DESC
        ''', conn, params=(user_id,))
    conn.close()
    return df

def get_averaging_down_summary(user_id):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    
    # ดึงข้อมูลสรุปของแต่ละหุ้น
    cursor.execute('''
        SELECT symbol, 
               SUM(CASE WHEN transaction_type = 'buy' THEN quantity ELSE -quantity END) as net_shares,
               AVG(CASE WHEN transaction_type = 'buy' THEN running_avg_price END) as avg_price,
               SUM(CASE WHEN transaction_type = 'buy' THEN quantity * price ELSE 0 END) as total_cost
        FROM averaging_down_transactions 
        WHERE user_id = ? 
        GROUP BY symbol
        HAVING net_shares > 0
    ''', (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{"symbol": r[0], "shares": r[1], "avg_price": r[2], "total_cost": r[3]} for r in results]

# ฟังก์ชันอื่นๆ (เพิ่ม user_id parameter)
def add_transaction(user_id, date_val, type_val, category, amount, description=""):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (user_id, date, type, category, amount, description)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, date_val, type_val, category, amount, description))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = sqlite3.connect('financial_data.db')
    df = pd.read_sql_query('SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC', conn, params=(user_id,))
    conn.close()
    return df

def delete_transaction(user_id, transaction_id):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', (transaction_id, user_id))
    conn.commit()
    conn.close()

def add_goal(user_id, name, target_amount, target_date, goal_type='general'):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO goals (user_id, name, target_amount, target_date, goal_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, name, target_amount, target_date, goal_type))
    conn.commit()
    conn.close()

def get_goals(user_id):
    conn = sqlite3.connect('financial_data.db')
    df = pd.read_sql_query('SELECT * FROM goals WHERE user_id = ? ORDER BY created_at DESC', conn, params=(user_id,))
    conn.close()
    return df

def add_dca_plan(user_id, symbol, investment_per_period, periods, start_date):
    conn = sqlite3.connect('financial_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO dca_plans (user_id, symbol, investment_per_period, periods, start_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, symbol.upper(), investment_per_period, periods, start_date))
    conn.commit()
    conn.close()

def get_dca_plans(user_id):
    conn = sqlite3.connect('financial_data.db')
    df = pd.read_sql_query('SELECT * FROM dca_plans WHERE user_id = ? ORDER BY created_at DESC', conn, params=(user_id,))
    conn.close()
    return df

def calculate_balance(user_id):
    try:
        df = get_transactions(user_id)
        if df.empty:
            return 0, 0, 0
        
        income = df[df['type'] == 'รายรับ']['amount'].sum()
        expense = df[df['type'] == 'รายจ่าย']['amount'].sum()
        balance = income - expense
        
        return balance, income, expense
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการคำนวณยอดเงิน: {str(e)}")
        return 0, 0, 0

# ฟังก์ชันช่วยเหลือ
def format_currency(amount):
    return "฿{:,.2f}".format(amount)

def format_percentage(value):
    return "{:.2f}%".format(value)

def get_price_color_class(change):
    if change > 0:
        return "price-up"
    elif change < 0:
        return "price-down"
    else:
        return "price-neutral"

# เริ่มต้นฐานข้อมูล
if 'db_initialized' not in st.session_state:
    try:
        init_database()
        st.session_state.db_initialized = True
    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการเริ่มต้นฐานข้อมูล: {str(e)}")
        
        # ให้ตัวเลือกรีเซ็ตฐานข้อมูล
        if st.button("🔄 รีเซ็ตฐานข้อมูล (ลบข้อมูลทั้งหมด)", type="secondary"):
            try:
                import os
                if os.path.exists('financial_data.db'):
                    os.remove('financial_data.db')
                init_database()
                st.session_state.db_initialized = True
                st.success("✅ รีเซ็ตฐานข้อมูลสำเร็จ!")
                st.rerun()
            except Exception as reset_error:
                st.error(f"❌ ไม่สามารถรีเซ็ตฐานข้อมูลได้: {str(reset_error)}")
        
        st.stop()  # หยุดการทำงานของแอปหากฐานข้อมูลมีปัญหา

# ระบบ Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None

if not st.session_state.logged_in:
    st.markdown("""
    <div class="main-header">
        <h1>💰 Personal Financial App - Multi-User System</h1>
        <p>ระบบจัดการการเงินส่วนบุคคลที่แยกข้อมูลตามผู้ใช้</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ตรวจสอบว่ามีข้อมูลเก่าหรือไม่
    try:
        conn = sqlite3.connect('financial_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        users_table_exists = cursor.fetchone() is not None
        
        if users_table_exists:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'legacy_user'")
            has_legacy_user = cursor.fetchone()[0] > 0
            
            if has_legacy_user:
                st.info("""
                🔄 **ระบบได้ทำการอัพเกรดข้อมูลเก่าแล้ว!**
                
                หากคุณเคยใช้ระบบเวอร์ชันเก่า ข้อมูลของคุณยังอยู่และสามารถเข้าถึงได้ด้วย:
                - **ชื่อผู้ใช้:** `legacy_user`
                - **รหัสผ่าน:** `defaultpass123`
                
                หรือสมัครสมาชิกใหม่เพื่อเริ่มต้นใหม่
                """)
        
        conn.close()
    except:
        pass
    
    # แสดงแท็บให้เห็นชัดเจน
    tab1, tab2 = st.tabs(["🔐 เข้าสู่ระบบ", "📝 สมัครสมาชิก"])
    
    with tab1:
        st.markdown("### 🔐 เข้าสู่ระบบ")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            
            login_username = st.text_input("👤 ชื่อผู้ใช้", placeholder="กรอกชื่อผู้ใช้", key="login_username")
            login_password = st.text_input("🔒 รหัสผ่าน", type="password", placeholder="กรอกรหัสผ่าน", key="login_password")
            
            if st.button("🚀 เข้าสู่ระบบ", type="primary", use_container_width=True):
                if login_username and login_password:
                    success, user_id = authenticate_user(login_username, login_password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = login_username
                        st.success("✅ เข้าสู่ระบบสำเร็จ!")
                        st.rerun()
                    else:
                        st.error("❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
                else:
                    st.error("❌ กรุณากรอกข้อมูลให้ครบถ้วน")
            
            st.markdown("---")
            st.info("🆕 ยังไม่มีบัญชี? ไปที่แท็บ 'สมัครสมาชิก' เพื่อสร้างบัญชีใหม่")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📝 สมัครสมาชิกใหม่")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-container">', unsafe_allow_html=True)
            
            st.info("💡 สร้างบัญชีใหม่เพื่อเริ่มใช้งานระบบจัดการการเงินส่วนบุคคล")
            
            new_username = st.text_input("👤 ชื่อผู้ใช้ใหม่", placeholder="ตัวอย่าง: john_doe", key="new_username", 
                                       help="ชื่อผู้ใช้ต้องไม่ซ้ำกับผู้อื่น")
            new_email = st.text_input("📧 อีเมล", placeholder="example@email.com", key="new_email",
                                    help="ใช้สำหรับการติดต่อ (ไม่บังคับ)")
            new_password = st.text_input("🔒 รหัสผ่าน", type="password", placeholder="อย่างน้อย 6 ตัวอักษร", 
                                       key="new_password", help="รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร")
            confirm_password = st.text_input("🔒 ยืนยันรหัสผ่าน", type="password", placeholder="กรอกรหัสผ่านอีกครั้ง", 
                                           key="confirm_password")
            
            if st.button("📝 สร้างบัญชีใหม่", type="primary", use_container_width=True):
                if new_username and new_password and confirm_password:
                    if len(new_username) < 3:
                        st.error("❌ ชื่อผู้ใช้ต้องมีอย่างน้อย 3 ตัวอักษร")
                    elif new_password != confirm_password:
                        st.error("❌ รหัสผ่านไม่ตรงกัน")
                    elif len(new_password) < 6:
                        st.error("❌ รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร")
                    else:
                        success, message = create_user(new_username, new_password, new_email)
                        if success:
                            st.success("🎉 " + message)
                            st.balloons()
                            st.info("💡 กลับไปที่แท็บ 'เข้าสู่ระบบ' เพื่อเข้าใช้งาน")
                        else:
                            st.error("❌ " + message)
                else:
                    st.error("❌ กรุณากรอกข้อมูลให้ครบถ้วน")
            
            st.markdown("---")
            st.success("✨ สมัครสมาชิกฟรี! ไม่มีค่าใช้จ่าย")
            
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # ดึงข้อมูลผู้ใช้
    user_info = get_user_info(st.session_state.user_id)
    
    # หัวข้อหลักสำหรับผู้ที่ login แล้ว
    st.markdown(f"""
    <div class="main-header">
        <h1>💰 Personal Financial App - ยินดีต้อนรับ {user_info[0]}!</h1>
        <p>ระบบจัดการการเงินส่วนบุคคลที่ครอบคลุมและแม่นยำ • เฉพาะข้อมูลของคุณเท่านั้น</p>
        <span class="streaming-live">🔴 LIVE DATA</span>
    </div>
    """, unsafe_allow_html=True)
    
    # แสดงข้อมูลผู้ใช้
    st.markdown(f"""
    <div class="user-info">
        👤 <strong>ผู้ใช้:</strong> {user_info[0]} | 📧 <strong>อีเมล:</strong> {user_info[1] or 'ไม่ระบุ'} | 
        📅 <strong>สมาชิกตั้งแต่:</strong> {user_info[2][:10]}
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 ออกจากระบบ"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()

    # Sidebar Navigation
    st.sidebar.title("📋 เมนูหลัก")
    page = st.sidebar.selectbox(
        "เลือกหน้าที่ต้องการ",
        ["📊 Dashboard", "🎯 Smart Stock Tracker", "🔄 การถั่วหุ้น", "💳 รายการธุรกรรม", 
         "🧮 DCA Calculator", "🎯 เป้าหมาย", "📋 รายงาน", "⚙️ การตั้งค่า"]
    )

    # Auto-refresh settings
    with st.sidebar:
        st.subheader("⚙️ ตั้งค่าการอัพเดท")
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=False)
        refresh_interval = st.selectbox("⏰ ความถี่ (วินาที)", [5, 10, 15, 30], index=1)
        use_real_data = st.checkbox("📡 ใช้ข้อมูลจริง", value=True, help="ดึงข้อมูลจาก Yahoo Finance")
        
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()

    # หน้า Smart Stock Tracker
    if page == "🎯 Smart Stock Tracker":
        st.header("🎯 Smart Stock Tracker - ระบบติดตามหุ้นอัจฉริยะ")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('📈 **ติดตามหุ้นแบบ Real-time พร้อมคำนวณกำไร-ขาดทุน**')
        with col2:
            if st.button("🔄 อัพเดทราคาทั้งหมด"):
                st.rerun()
        
        # ฟอร์มเพิ่มหุ้นใหม่
        with st.expander("➕ เพิ่มหุ้นลงใน Tracker", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                stock_symbol = st.text_input("📛 รหัสหุ้น", placeholder="เช่น AAPL, BBL, GOOGL")
                quantity = st.number_input("📊 จำนวนหุ้น", min_value=0.01, step=0.01, format="%.2f")
                buy_price = st.number_input("💰 ราคาซื้อ", min_value=0.01, step=0.01, format="%.2f")
            
            with col2:
                buy_date = st.date_input("📅 วันที่ซื้อ", value=date.today())
                notes = st.text_area("📝 หมายเหตุ", placeholder="บันทึกเพิ่มเติม เช่น เหตุผลการซื้อ")
            
            if st.button("💾 เพิ่มหุ้นใน Tracker", type="primary"):
                if stock_symbol and quantity > 0 and buy_price > 0:
                    add_real_stock(st.session_state.user_id, stock_symbol, quantity, buy_price, buy_date, notes)
                    st.success(f"✅ เพิ่มหุ้น {stock_symbol.upper()} จำนวน {quantity} หุ้น เรียบร้อยแล้ว!")
                    st.rerun()
                else:
                    st.error("❌ กรุณากรอกข้อมูลให้ครบถ้วน")
        
        # แสดงรายการหุ้นที่ติดตาม
        stocks_df = get_real_stocks(st.session_state.user_id)
        
        if not stocks_df.empty:
            st.subheader("📊 หุ้นที่กำลังติดตาม")
            
            total_investment = 0
            total_current_value = 0
            total_profit_loss = 0
            
            for index, stock in stocks_df.iterrows():
                current_data = get_stock_data(stock['symbol'], use_real_data)
                
                investment = stock['quantity'] * stock['buy_price']
                current_value = stock['quantity'] * current_data['current_price']
                profit_loss = current_value - investment
                profit_loss_percent = (profit_loss / investment) * 100 if investment > 0 else 0
                
                total_investment += investment
                total_current_value += current_value
                total_profit_loss += profit_loss
                
                # แสดงข้อมูลแต่ละหุ้น
                st.markdown(f"""
                <div class="stock-tracker-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3>{stock['symbol']} 📈</h3>
                            <p><strong>จำนวน:</strong> {stock['quantity']:,.2f} หุ้น</p>
                            <p><strong>ซื้อวันที่:</strong> {stock['buy_date']} ที่ราคา ฿{stock['buy_price']:,.2f}</p>
                            <p><strong>ลงทุน:</strong> {format_currency(investment)}</p>
                            {f'<p><strong>หมายเหตุ:</strong> {stock["notes"]}</p>' if stock.get('notes') else ''}
                        </div>
                        <div style="text-align: right;">
                            <h2 class="{get_price_color_class(current_data['change'])}">
                                ฿{current_data['current_price']:,.2f}
                            </h2>
                            <p class="{get_price_color_class(current_data['change'])}">
                                {current_data['change']:+.2f} ({current_data['change_percent']:+.2f}%)
                            </p>
                            <p><strong>มูลค่าปัจจุบัน:</strong> {format_currency(current_value)}</p>
                            <h4 class="{get_price_color_class(profit_loss)}">
                                กำไร/ขาดทุน: {format_currency(profit_loss)} ({profit_loss_percent:+.2f}%)
                            </h4>
                            <small>อัพเดท: {current_data['last_updated'].strftime('%H:%M:%S')}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # ปุ่มลบ
                if st.button(f"🗑️ ลบ {stock['symbol']}", key=f"delete_{stock['id']}"):
                    delete_real_stock(st.session_state.user_id, stock['id'])
                    st.success(f"✅ ลบหุ้น {stock['symbol']} เรียบร้อยแล้ว!")
                    st.rerun()
            
            # สรุปรวม
            st.divider()
            st.subheader("📊 สรุปรวม Portfolio")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💰 เงินลงทุนรวม", format_currency(total_investment))
            with col2:
                st.metric("📈 มูลค่าปัจจุบัน", format_currency(total_current_value))
            with col3:
                overall_percent = (total_profit_loss / total_investment * 100) if total_investment > 0 else 0
                st.metric("💹 กำไร/ขาดทุนรวม", format_currency(total_profit_loss), 
                         delta=f"{overall_percent:+.2f}%")
            with col4:
                days_held = (date.today() - pd.to_datetime(stocks_df['buy_date']).dt.date.min()).days
                st.metric("📅 ระยะเวลาถือครอง", f"{days_held} วัน")
        
        else:
            st.info("📈 ยังไม่มีหุ้นในระบบ Tracker ลองเพิ่มหุ้นแรกดูสิ! 🚀")

    # หน้าการถั่วหุ้น (ใหม่)
    elif page == "🔄 การถั่วหุ้น":
        st.header("🔄 ระบบคำนวณการถั่วหุ้น (Averaging Down)")
        
        st.markdown("""
        <div class="averaging-down-card">
            <h3>💡 การถั่วหุ้น (Averaging Down) คืออะไร?</h3>
            <p>เป็นกลยุทธ์การซื้อหุ้นเพิ่มเติมเมื่อราคาลดลงจากราคาที่ซื้อครั้งแรก 
            เพื่อลดราคาต้นทุนเฉลี่ยต่อหุ้น ทำให้ต้องการราคาหุ้นขึ้นน้อยลงเพื่อทำกำไร</p>
            <p><strong>⚠️ ข้อควรระวัง:</strong> ใช้เฉพาะกับหุ้นที่มีปัจจัยพื้นฐานดี และมั่นใจในแนวโน้มระยะยาว</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🔢 คำนวณการถั่วหุ้น", "📝 บันทึกธุรกรรม", "📊 สรุปการถั่วหุ้น"])
        
        with tab1:
            st.subheader("🔢 เครื่องคำนวณการถั่วหุ้น")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 ข้อมูลปัจจุบัน**")
                existing_shares = st.number_input("จำนวนหุ้นที่มีอยู่", min_value=0.0, step=0.01, format="%.2f")
                existing_avg_price = st.number_input("ราคาเฉลี่ยปัจจุบัน", min_value=0.0, step=0.01, format="%.2f")
                current_market_price = st.number_input("ราคาตลาดปัจจุบัน", min_value=0.0, step=0.01, format="%.2f")
            
            with col2:
                st.markdown("**🛒 การซื้อเพิ่ม**")
                new_shares = st.number_input("จำนวนหุ้นที่จะซื้อเพิ่ม", min_value=0.0, step=0.01, format="%.2f")
                new_price = st.number_input("ราคาที่จะซื้อเพิ่ม", min_value=0.0, step=0.01, format="%.2f")
            
            if st.button("🔍 คำนวณการถั่วหุ้น", type="primary"):
                if existing_shares > 0 and existing_avg_price > 0 and new_shares > 0 and new_price > 0:
                    result = calculate_averaging_down(existing_shares, existing_avg_price, new_shares, new_price)
                    
                    st.markdown("### 📊 ผลการคำนวณ")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🔢 หุ้นรวมใหม่", f"{result['total_shares']:,.2f}")
                        st.metric("💰 ราคาเฉลี่ยใหม่", f"฿{result['new_avg_price']:,.2f}")
                    
                    with col2:
                        st.metric("💸 เงินลงทุนรวม", f"฿{result['total_cost']:,.2f}")
                        st.metric("📉 ลดต้นทุนเฉลี่ย", f"฿{result['cost_reduction']:,.2f}")
                    
                    with col3:
                        current_value = result['total_shares'] * current_market_price if current_market_price > 0 else 0
                        unrealized_pnl = current_value - result['total_cost']
                        st.metric("📈 มูลค่าปัจจุบัน", f"฿{current_value:,.2f}")
                        st.metric("💹 กำไร/ขาดทุนที่ยังไม่ขาย", f"฿{unrealized_pnl:,.2f}")
                    
                    # แสดงเปอร์เซ็นต์การลดลง
                    reduction_percent = result['cost_reduction_percent']
                    if reduction_percent > 0:
                        st.success(f"✅ ลดต้นทุนเฉลี่ยได้ {reduction_percent:.2f}%")
                    else:
                        st.warning(f"⚠️ ราคาซื้อเพิ่มสูงกว่าราคาเฉลี่ยเดิม จะเพิ่มต้นทุนเฉลี่ย {abs(reduction_percent):.2f}%")
                    
                    # กราฟเปรียบเทียบ
                    if current_market_price > 0:
                        break_even_old = existing_avg_price
                        break_even_new = result['new_avg_price']
                        
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            name='ก่อนถั่วหุ้น',
                            x=['ราคาคุ้มทุน'],
                            y=[break_even_old],
                            marker_color='red'
                        ))
                        fig.add_trace(go.Bar(
                            name='หลังถั่วหุ้น',
                            x=['ราคาคุ้มทุน'],
                            y=[break_even_new],
                            marker_color='green'
                        ))
                        fig.add_hline(y=current_market_price, line_dash="dash", 
                                    annotation_text=f"ราคาปัจจุบัน: ฿{current_market_price:,.2f}")
                        
                        fig.update_layout(title="📊 เปรียบเทียบราคาคุ้มทุน", barmode='group')
                        st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.error("❌ กรุณากรอกข้อมูลให้ครบถ้วน")
        
        with tab2:
            st.subheader("📝 บันทึกธุรกรรมการถั่วหุ้น")
            
            col1, col2 = st.columns(2)
            
            with col1:
                trans_symbol = st.text_input("📛 รหัสหุ้น", placeholder="เช่น AAPL, BBL")
                trans_type = st.selectbox("📋 ประเภทธุรกรรม", ["buy", "sell"])
                trans_quantity = st.number_input("📊 จำนวนหุ้น", min_value=0.01, step=0.01, format="%.2f")
            
            with col2:
                trans_price = st.number_input("💰 ราคาต่อหุ้น", min_value=0.01, step=0.01, format="%.2f")
                trans_date = st.date_input("📅 วันที่ธุรกรรม", value=date.today())
                trans_notes = st.text_area("📝 หมายเหตุ", placeholder="บันทึกเหตุผลการซื้อ/ขาย")
            
            if st.button("💾 บันทึกธุรกรรม", type="primary"):
                if trans_symbol and trans_quantity > 0 and trans_price > 0:
                    add_averaging_down_transaction(
                        st.session_state.user_id, trans_symbol, trans_type, 
                        trans_quantity, trans_price, trans_date, trans_notes
                    )
                    st.success(f"✅ บันทึกการ{trans_type} {trans_symbol.upper()} เรียบร้อยแล้ว!")
                    st.rerun()
                else:
                    st.error("❌ กรุณากรอกข้อมูลให้ครบถ้วน")
        
        with tab3:
            st.subheader("📊 สรุปการถั่วหุ้นทั้งหมด")
            
            # แสดงสรุปแต่ละหุ้น
            summary = get_averaging_down_summary(st.session_state.user_id)
            
            if summary:
                for stock in summary:
                    symbol = stock['symbol']
                    current_data = get_stock_data(symbol, use_real_data)
                    current_price = current_data['current_price']
                    
                    current_value = stock['shares'] * current_price
                    profit_loss = current_value - stock['total_cost']
                    profit_percent = (profit_loss / stock['total_cost']) * 100 if stock['total_cost'] > 0 else 0
                    
                    st.markdown(f"""
                    <div class="averaging-down-card">
                        <h4>{symbol} - การถั่วหุ้น</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
                            <div>
                                <p><strong>จำนวนหุ้น:</strong> {stock['shares']:,.2f}</p>
                                <p><strong>ราคาเฉลี่ย:</strong> ฿{stock['avg_price']:,.2f}</p>
                            </div>
                            <div>
                                <p><strong>ต้นทุนรวม:</strong> ฿{stock['total_cost']:,.2f}</p>
                                <p><strong>ราคาปัจจุบัน:</strong> ฿{current_price:,.2f}</p>
                            </div>
                            <div>
                                <p><strong>มูลค่าปัจจุบัน:</strong> ฿{current_value:,.2f}</p>
                                <p class="{get_price_color_class(profit_loss)}">
                                    <strong>กำไร/ขาดทุน:</strong> ฿{profit_loss:,.2f} ({profit_percent:+.2f}%)
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # แสดงประวัติธุรกรรม
                    with st.expander(f"📋 ประวัติธุรกรรม {symbol}"):
                        transactions = get_averaging_down_transactions(st.session_state.user_id, symbol)
                        if not transactions.empty:
                            st.dataframe(
                                transactions[['transaction_date', 'transaction_type', 'quantity', 'price', 'running_avg_price', 'notes']],
                                use_container_width=True
                            )
                        else:
                            st.info("ยังไม่มีธุรกรรมสำหรับหุ้นนี้")
            
            else:
                st.info("📝 ยังไม่มีการบันทึกธุรกรรมการถั่วหุ้น")

    # หน้า DCA Calculator
    elif page == "🧮 DCA Calculator":
        st.header("🧮 DCA Calculator - เครื่องคำนวณการถั่วเฉลี่ย")
        
        st.markdown("""
        <div class="dca-calculator">
            <h3>💡 Dollar Cost Averaging (DCA) คืออะไร?</h3>
            <p>เป็นกลยุทธ์การลงทุนที่ลงทุนเป็นจำนวนเงินคงที่ในช่วงเวลาที่กำหนด ไม่ว่าราคาจะขึ้นหรือลง 
            ช่วยลดความเสี่ยงจากความผันผวนของตลาด</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 ตั้งค่าการคำนวณ DCA")
            
            dca_symbol = st.text_input("📛 รหัสหุ้น", placeholder="เช่น AAPL, BBL")
            investment_per_period = st.number_input("💰 เงินลงทุนต่องวด (บาท)", 
                                                  min_value=100, step=100, value=1000)
            periods = st.number_input("📅 จำนวนงวด", min_value=1, max_value=120, step=1, value=12)
            period_type = st.selectbox("⏰ ประเภทงวด", ["รายเดือน", "รายสัปดาห์", "รายวัน"])
            
            if st.button("🔍 คำนวณ DCA", type="primary") and dca_symbol:
                current_data = get_stock_data(dca_symbol, use_real_data)
                current_price = current_data['current_price']
                
                dca_result = calculate_dca_strategy(
                    dca_symbol, current_price, 
                    investment_per_period * periods, 
                    investment_per_period, periods
                )
                
                st.session_state.dca_result = dca_result
                st.session_state.dca_symbol = dca_symbol
                st.session_state.current_price = current_price
                st.session_state.investment_per_period = investment_per_period
                st.session_state.periods = periods
        
        with col2:
            st.subheader("📈 ผลการคำนวณ")
            
            if 'dca_result' in st.session_state:
                result = st.session_state.dca_result
                symbol = st.session_state.dca_symbol
                current_price = st.session_state.current_price
                
                st.metric("📛 หุ้น", symbol)
                st.metric("💰 ราคาปัจจุบัน", f"฿{current_price:,.2f}")
                st.metric("💸 เงินลงทุนรวม", f"฿{result['total_investment']:,.2f}")
                st.metric("📊 หุ้นที่ได้ต่องวด", f"{result['shares_per_period']:.4f}")
                st.metric("🎯 หุ้นรวมทั้งหมด", f"{result['total_shares']:.4f}")
                st.metric("⚖️ ราคาเฉลี่ย", f"฿{result['average_price']:.2f}")
                
                profit_loss = result['current_profit_loss']
                profit_percent = (profit_loss / result['total_investment']) * 100
                
                st.metric("💹 กำไร/ขาดทุนปัจจุบัน", 
                         f"฿{profit_loss:,.2f}", 
                         delta=f"{profit_percent:+.2f}%")
                
                # บันทึกแผน DCA
                if st.button("💾 บันทึกแผน DCA"):
                    add_dca_plan(st.session_state.user_id, symbol, st.session_state.investment_per_period, 
                               st.session_state.periods, date.today())
                    st.success("✅ บันทึกแผน DCA เรียบร้อยแล้ว!")
            
            else:
                st.info("👆 กรอกข้อมูลด้านซ้ายและกดคำนวณเพื่อดูผลลัพธ์")
        
        # แสดง Scenario Analysis
        if 'dca_result' in st.session_state:
            st.divider()
            st.subheader("🎭 Scenario Analysis - วิเคราะห์สถานการณ์")
            
            scenarios = st.session_state.dca_result['scenarios']
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("📊 ผลตอบแทนในสถานการณ์ต่างๆ")
                for scenario in scenarios:
                    change = scenario['price_change']
                    profit = scenario['profit_loss']
                    profit_pct = scenario['profit_percent']
                    
                    color = "🟢" if profit >= 0 else "🔴"
                    st.write(f"{color} หากราคา{change:+}%: กำไร/ขาดทุน ฿{profit:,.0f} ({profit_pct:+.1f}%)")
            
            with col2:
                fig_scenario = px.bar(
                    x=[f"{s['price_change']:+}%" for s in scenarios],
                    y=[s['profit_loss'] for s in scenarios],
                    title="📈 กำไร/ขาดทุนในสถานการณ์ต่างๆ",
                    color=[s['profit_loss'] for s in scenarios],
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                st.plotly_chart(fig_scenario, use_container_width=True)

    # หน้า Dashboard
    elif page == "📊 Dashboard":
        st.header("📊 Financial Dashboard")
        
        balance, total_income, total_expense = calculate_balance(st.session_state.user_id)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 ยอดคงเหลือ", format_currency(balance))
        with col2:
            st.metric("📈 รายรับรวม", format_currency(total_income))
        with col3:
            st.metric("📉 รายจ่ายรวม", format_currency(total_expense))
        with col4:
            savings_rate = (balance / total_income * 100) if total_income > 0 else 0
            st.metric("💾 อัตราการออม", format_percentage(savings_rate))
        
        # Portfolio Summary
        real_stocks_df = get_real_stocks(st.session_state.user_id)
        if not real_stocks_df.empty:
            st.subheader("💼 Portfolio Summary")
            
            total_portfolio_value = 0
            total_portfolio_cost = 0
            
            for _, stock in real_stocks_df.iterrows():
                current_data = get_stock_data(stock['symbol'], use_real_data)
                current_value = stock['quantity'] * current_data['current_price']
                cost = stock['quantity'] * stock['buy_price']
                
                total_portfolio_value += current_value
                total_portfolio_cost += cost
            
            portfolio_pnl = total_portfolio_value - total_portfolio_cost
            portfolio_pnl_percent = (portfolio_pnl / total_portfolio_cost * 100) if total_portfolio_cost > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📈 มูลค่า Portfolio", format_currency(total_portfolio_value))
            with col2:
                st.metric("💰 ต้นทุน Portfolio", format_currency(total_portfolio_cost))
            with col3:
                st.metric("💹 กำไร/ขาดทุน", format_currency(portfolio_pnl), 
                         delta=f"{portfolio_pnl_percent:+.2f}%")

    # หน้าอื่นๆ ที่เหลือ (รายการธุรกรรม, เป้าหมาย, รายงาน, การตั้งค่า)
    elif page == "💳 รายการธุรกรรม":
        st.header("💳 จัดการรายการธุรกรรม")
        
        # ฟอร์มเพิ่มรายการใหม่
        with st.expander("➕ เพิ่มรายการใหม่", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                transaction_date = st.date_input("📅 วันที่", value=date.today())
                transaction_type = st.selectbox("📝 ประเภท", ["รายรับ", "รายจ่าย"])
            
            with col2:
                if transaction_type == "รายรับ":
                    categories = ["💼 เงินเดือน", "🎁 โบนัส", "🏢 ธุรกิจ", "📈 การลงทุน", "💻 งานอิสระ", "💰 อื่นๆ"]
                else:
                    categories = ["🍽️ อาหาร", "🚗 ค่าเดินทาง", "🏠 ที่อยู่อาศัย", "🛒 ช็อปปิ้ง", 
                                "🏥 สุขภาพ", "🎬 บันเทิง", "📚 การศึกษา", "💡 สาธารณูปโภค", "💸 อื่นๆ"]
                
                category = st.selectbox("📂 หมวดหมู่", categories)
                amount = st.number_input("💵 จำนวนเงิน", min_value=0.0, step=1.0)
            
            description = st.text_input("📝 รายละเอียด", placeholder="รายละเอียดเพิ่มเติม (ไม่บังคับ)")
            
            if st.button("💾 บันทึกรายการ", type="primary"):
                if amount > 0:
                    add_transaction(st.session_state.user_id, transaction_date, transaction_type, category, amount, description)
                    st.success("✅ เพิ่ม{} {} เรียบร้อยแล้ว!".format(
                        transaction_type, format_currency(amount)
                    ))
                    st.rerun()
                else:
                    st.error("❌ กรุณากรอกจำนวนเงินที่มากกว่า 0")
        
        st.divider()
        
        # แสดงรายการธุรกรรม
        st.subheader("📋 รายการธุรกรรมล่าสุด")
        df = get_transactions(st.session_state.user_id)
        
        if not df.empty:
            for index, row in df.head(20).iterrows():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    icon = "💰" if row['type'] == 'รายรับ' else "💸"
                    color = "🟢" if row['type'] == 'รายรับ' else "🔴"
                    
                    st.write("{} {} {} - {} - {} - {}".format(
                        color, icon, row['category'], 
                        format_currency(row['amount']), 
                        row['description'], row['date']
                    ))
                
                with col2:
                    if st.button("🗑️", key="delete_{}".format(row['id']), help="ลบรายการนี้"):
                        delete_transaction(st.session_state.user_id, row['id'])
                        st.success("✅ ลบรายการเรียบร้อยแล้ว!")
                        st.rerun()
        else:
            st.info("📝 ยังไม่มีรายการธุรกรรม ลองเพิ่มรายการแรกดูสิ!")

    elif page == "🎯 เป้าหมาย":
        st.header("🎯 เป้าหมายการเงิน")
        
        # เพิ่มเป้าหมายใหม่
        with st.expander("➕ เพิ่มเป้าหมายใหม่"):
            col1, col2 = st.columns(2)
            with col1:
                goal_name = st.text_input("🎯 ชื่อเป้าหมาย", placeholder="เช่น ซื้อบ้าน, เที่ยวต่างประเทศ")
                target_amount = st.number_input("💰 จำนวนเงินเป้าหมาย", min_value=0.0, step=1000.0)
            with col2:
                target_date = st.date_input("📅 วันที่เป้าหมาย")
                goal_type = st.selectbox("📂 ประเภทเป้าหมาย", 
                                       ["เงินฉุกเฉิน", "ที่อยู่อาศัย", "การลงทุน", "การเดินทาง", "การศึกษา", "อื่นๆ"])
            
            if st.button("💾 เพิ่มเป้าหมาย", type="primary"):
                if goal_name and target_amount > 0:
                    add_goal(st.session_state.user_id, goal_name, target_amount, target_date, goal_type)
                    st.success("✅ เพิ่มเป้าหมาย '{}' เรียบร้อยแล้ว!".format(goal_name))
                    st.rerun()
        
        # แสดงเป้าหมายปัจจุบัน
        st.subheader("📊 เป้าหมายปัจจุบัน")
        goals_df = get_goals(st.session_state.user_id)
        
        if not goals_df.empty:
            for index, goal in goals_df.iterrows():
                progress = min(goal['current_amount'] / goal['target_amount'] * 100, 100) if goal['target_amount'] > 0 else 0
                
                st.subheader("{} ({})".format(goal['name'], goal.get('goal_type', 'general')))
                st.progress(progress / 100)
                st.write("{} / {} ({})".format(
                    format_currency(goal['current_amount']),
                    format_currency(goal['target_amount']),
                    format_percentage(progress)
                ))
        else:
            st.info("🎯 ยังไม่มีเป้าหมาย ลองเพิ่มเป้าหมายแรกดูสิ!")

    elif page == "📋 รายงาน":
        st.header("📋 รายงานการเงิน")
        
        balance, income, expense = calculate_balance(st.session_state.user_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 ยอดคงเหลือ", format_currency(balance))
        with col2:
            st.metric("📈 รายรับรวม", format_currency(income))
        with col3:
            st.metric("📉 รายจ่ายรวม", format_currency(expense))

    elif page == "⚙️ การตั้งค่า":
        st.header("⚙️ การตั้งค่าระบบ")
        
        st.subheader("👤 ข้อมูลผู้ใช้")
        st.write(f"ชื่อผู้ใช้: {user_info[0]}")
        st.write(f"อีเมล: {user_info[1] or 'ไม่ระบุ'}")
        st.write(f"สมาชิกตั้งแต่: {user_info[2][:10]}")
        
        st.subheader("📊 สถิติการใช้งาน")
        st.write(f"จำนวนธุรกรรม: {len(get_transactions(st.session_state.user_id))}")
        st.write(f"จำนวนหุ้นใน Tracker: {len(get_real_stocks(st.session_state.user_id))}")
        st.write(f"จำนวนเป้าหมาย: {len(get_goals(st.session_state.user_id))}")

# Footer
st.markdown("---")
st.write("💰 Personal Financial App - Multi-User System | Advanced Portfolio & Stock Management")
st.write("📊 Real-time Data • 🎯 Smart Tracking • 🔄 Averaging Down • 🧮 DCA Calculator • 👥 Multi-User Support")
st.write("🔒 Secure & Private • Last Updated: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))