# File: app.py

import os
from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

# --- 1. Initialize Flask App and Enable CORS ---
# ส่วนนี้ถูกต้องแล้ว ไม่ต้องแก้ไข
app = Flask(__name__)
CORS(app) 

# --- (จุดสำคัญที่ต้องแก้ไข) ---
# --- 2. กรุณากรอกรายละเอียดการเชื่อมต่อฐานข้อมูลของคุณ ---
# ให้แทนที่ค่าในเครื่องหมายคำพูด ("...") ด้วยข้อมูลจริงของคุณ
# คุณสามารถหา Server Name ได้จากโปรแกรม SQL Server Management Studio (SSMS) ตอนที่คุณเชื่อมต่อ
SERVER_NAME = "pairojs2"  # <--- แก้ไขตรงนี้!! เช่น "DESKTOP-ABC\SQLEXPRESS" หรือ "192.168.1.5"
DATABASE_NAME = "SSalakDB"             # <--- ตรวจสอบชื่อฐานข้อมูล
USERNAME = "sa"                        # <--- ตรวจสอบชื่อผู้ใช้
PASSWORD = "Abc1234"                   # <--- ตรวจสอบรหัสผ่าน
# --- (จบส่วนที่ต้องแก้ไข) ---


# --- 3. ตรวจสอบชื่อตารางและคอลัมน์ ---
# ค่าเหล่านี้ต้องตรงกับชื่อในฐานข้อมูลของคุณทุกตัวอักษร
TABLE_NAME = 'dbo.SClient'
COL_CNAME = 'Cname'
COL_TAXID = 'Taxid'
COL_BRANCH_TYPE = 'Abbre' # ในโค้ดเก่าคือ 'Pkey' ซึ่งอาจไม่ถูกต้องสำหรับประเภทสาขา
COL_BRANCH_NO = 'Pkey'    # ในโค้ดเก่าคือ 'Abbre' ซึ่งอาจไม่ถูกต้องสำหรับเลขที่สาขา


# --- 4. สร้าง Connection String (ส่วนนี้จะทำงานอัตโนมัติ ไม่ต้องแก้ไข) ---
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;"
)

def get_companies_from_db():
    """
    เชื่อมต่อฐานข้อมูลและดึงข้อมูลบริษัท
    """
    companies = []
    try:
        # ตรวจสอบว่าได้กรอกข้อมูลครบถ้วนหรือไม่
        if "YOUR_SERVER_NAME_HERE" in SERVER_NAME:
            raise ValueError("กรุณาแก้ไข SERVER_NAME ในไฟล์ app.py ก่อนรัน")

        # เริ่มการเชื่อมต่อ
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        # สร้างและรันคำสั่ง SQL
        query = f"SELECT {COL_CNAME}, {COL_TAXID}, {COL_BRANCH_TYPE}, {COL_BRANCH_NO} FROM {TABLE_NAME}"
        cursor.execute(query)
        rows = cursor.fetchall()

        # จัดรูปแบบข้อมูลสำหรับส่งให้ Frontend
        for row in rows:
            # ใช้ getattr เพื่อป้องกัน Error หากคอลัมน์ไม่มีข้อมูล (NULL)
            company_name = getattr(row, COL_CNAME, '')
            tax_id = getattr(row, COL_TAXID, '')
            branch_type = getattr(row, COL_BRANCH_TYPE, '')
            branch_no = getattr(row, COL_BRANCH_NO, '')

            companies.append({
                "CompanyName": company_name.strip() if company_name else '',
                "TaxID": tax_id.strip() if tax_id else '',
                # แปลงค่า Abbre เป็น 'สำนักงานใหญ่' หรือ 'สาขา'
                "BranchType": 'สาขา' if 'สาขา' in (branch_type or '') else 'สำนักงานใหญ่',
                "BranchNo": branch_no.strip() if branch_no else ''
            })
            
        cnxn.close()
        print(f"✅ (Backend) ดึงข้อมูลสำเร็จ: {len(companies)} รายการ")
        return companies, None

    except pyodbc.Error as ex:
        # จัดการ Error จาก pyodbc โดยเฉพาะ
        sqlstate = ex.args[0]
        error_message = f"Database Error: {sqlstate} - {ex}"
        print(f"❌ (Backend) เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {error_message}")
        return [], error_message
    except Exception as e:
        # จัดการ Error ทั่วไป
        error_message = str(e)
        print(f"❌ (Backend) เกิดข้อผิดพลาด: {error_message}")
        return [], error_message

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """
    API endpoint สำหรับให้หน้าเว็บเรียกข้อมูล
    """
    companies, error = get_companies_from_db()

    if error:
        # หากมี Error เกิดขึ้น จะส่งข้อความแจ้งเตือนกลับไป
        return jsonify({
            "error": "ไม่สามารถดึงข้อมูลจากฐานข้อมูลได้",
            "details": error
        }), 500
    
    # หากสำเร็จ จะส่งข้อมูลบริษัทกลับไป
    return jsonify(companies)

if __name__ == '__main__':
    # รันเซิร์ฟเวอร์ที่ Port 5000 และเปิด Debug Mode
    app.run(debug=True, port=5000)