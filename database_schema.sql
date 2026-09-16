-- ========================================================
-- POKI MEGA ENTERPRISE - DATABASE SCHEMA & MASTER TABLES
-- إدارة وتطوير وإشراف هندسي: أبو العز العمري
-- ========================================================

-- جدول تخزين الألعاب وتفاصيل المطورين وسنة الإصدار
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    dev_name TEXT NOT NULL, 
    title TEXT NOT NULL, 
    link TEXT NOT NULL, 
    year TEXT NOT NULL, 
    category TEXT NOT NULL, 
    status TEXT DEFAULT 'قيد المراجعة', 
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- جدول المستخدمين الحقيقيين وتخزين النقاط والبيانات الأمنية المشفرة
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email TEXT UNIQUE NOT NULL, 
    password TEXT NOT NULL, 
    points INTEGER DEFAULT 150,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
