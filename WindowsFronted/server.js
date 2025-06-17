// --- Import Libraries ---
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');

// --- Basic Setup ---
const app = express();
const PORT = 3001;
const JWT_SECRET = 'your-super-secret-key-change-this'; // ควรเปลี่ยนเป็นค่าที่ซับซ้อนและเก็บเป็นความลับ

// --- Middleware ---
app.use(cors()); // อนุญาตให้ Frontend (จากต่าง port) เรียกมาได้
app.use(express.json()); // ให้ Express อ่านข้อมูลแบบ JSON ได้

// --- Database Setup (SQLite) ---
const db = new sqlite3.Database('./database.db', (err) => {
    if (err) {
        console.error("Error opening database", err.message);
    } else {
        console.log("Connected to the SQLite database.");
        // สร้างตาราง users ถ้ายังไม่มี
        db.run(`CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )`);
    }
});

// --- API Routes ---

// 1. Signup Route
app.post('/api/auth/signup', async (req, res) => {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
        return res.status(400).json({ message: 'กรุณากรอกข้อมูลให้ครบทุกช่อง' });
    }

    try {
        // เข้ารหัสผ่านก่อนบันทึก
        const hashedPassword = await bcrypt.hash(password, 10); // 10 คือ salt rounds

        const sql = `INSERT INTO users (username, email, password) VALUES (?, ?, ?)`;
        db.run(sql, [username, email, hashedPassword], function(err) {
            if (err) {
                // ตรวจสอบว่ามี username หรือ email ซ้ำหรือไม่
                if (err.message.includes('UNIQUE constraint failed')) {
                    return res.status(409).json({ message: 'ชื่อผู้ใช้หรืออีเมลนี้มีอยู่ในระบบแล้ว' });
                }
                return res.status(500).json({ message: 'ไม่สามารถสมัครสมาชิกได้', error: err.message });
            }
            res.status(201).json({ message: 'สมัครสมาชิกสำเร็จ!', userId: this.lastID });
        });
    } catch (error) {
        res.status(500).json({ message: 'เกิดข้อผิดพลาดบนเซิร์ฟเวอร์', error: error.message });
    }
});

// 2. Login Route
app.post('/api/auth/login', (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ message: 'กรุณากรอกชื่อผู้ใช้และรหัสผ่าน' });
    }

    const sql = `SELECT * FROM users WHERE username = ?`;
    db.get(sql, [username], async (err, user) => {
        if (err) {
            return res.status(500).json({ message: 'เกิดข้อผิดพลาดบนเซิร์ฟเวอร์', error: err.message });
        }
        if (!user) {
            return res.status(401).json({ message: 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง' });
        }

        // เปรียบเทียบรหัสผ่านที่ผู้ใช้ส่งมากับที่เข้ารหัสไว้ใน DB
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(401).json({ message: 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง' });
        }

        // สร้าง JSON Web Token (JWT)
        const token = jwt.sign(
            { id: user.id, username: user.username },
            JWT_SECRET,
            { expiresIn: '1h' } // Token หมดอายุใน 1 ชั่วโมง
        );

        res.status(200).json({
            message: 'เข้าสู่ระบบสำเร็จ!',
            token: token,
            userId: user.id,
            username: user.username
        });
    });
});

// --- Start Server ---
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});