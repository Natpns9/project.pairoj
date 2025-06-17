# File: pnd.py

import os
from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

# --- 1. Initialize Flask App and Enable CORS ---
app = Flask(__name__)
CORS(app)

# --- 2. กรุณากรอกรายละเอียดการเชื่อมต่อฐานข้อมูลของคุณ ---
SERVER_NAME = "pairojs2"          # <--- แก้ไขตรงนี้!! เช่น "DESKTOP-ABC\SQLEXPRESS"
DATABASE_NAME = "SCSA"        # <--- ตรวจสอบชื่อฐานข้อมูล
USERNAME = "sa"               # <--- ตรวจสอบชื่อผู้ใช้
PASSWORD = "Abc1234"          # <--- ตรวจสอบรหัสผ่าน

# --- 3. ตรวจสอบชื่อตารางและคอลัมน์ในฐานข้อมูลของคุณ ---
# ค่าเหล่านี้ต้องตรงกับชื่อในฐานข้อมูลจริง
# ผมได้เพิ่มคอลัมน์ที่อยู่ต่างๆ เข้ามา โดยอ้างอิงจากที่ Frontend ต้องการ
# หากชื่อคอลัมน์ในฐานข้อมูลของคุณแตกต่างไป กรุณาแก้ไขให้ถูกต้อง
TABLE_NAME = 'dbo.CSAC'
COL_CNAME = 'Cname'                 # ชื่อบริษัท/กิจการ
COL_TAXID = 'Taxid'                 # เลขผู้เสียภาษี
COL_BRANCH = 'Branch'               # ชื่อสาขา/สถานประกอบการ
COL_ADDRESS = 'Address'             # เลขที่
COL_MOO = 'Moo'                     # หมู่ที่
COL_SOI = 'Soi'                     # ซอย
COL_ROAD = 'Road'                   # ถนน
COL_TAMBOL = 'Tambol'               # ตำบล/แขวง
COL_AMPHUR = 'Amphur'             # อำเภอ/เขต
COL_PROVINCE = 'Province'           # จังหวัด
COL_ZIPCODE = 'Zipcode'             # รหัสไปรษณีย์
COL_PREFIX = 'Prefix' # 'บริษัท', 'หจก.' (ถ้ามีใน DB)
# หากไม่มีคอลัมน์ Prefix สามารถลบออกได้ แล้ว Frontend จะจัดการเอง

# --- 4. สร้าง Connection String (ส่วนนี้จะทำงานอัตโนมัติ) ---
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
    เชื่อมต่อฐานข้อมูลและดึงข้อมูลบริษัทพร้อมที่อยู่ทั้งหมด
    """
    companies = []
    try:
        if "SCSA" in SERVER_NAME and DATABASE_NAME == "CSAC":
             print("⚠️ (Backend) Warning: Using default credentials. Please update your connection details in app.py.")
             
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        # สร้าง Query โดยเลือกคอลัมน์ทั้งหมดที่ Frontend ต้องการ
        query = f"""
            SELECT
                {COL_PREFIX},
                {COL_CNAME},
                {COL_TAXID},
                {COL_BRANCH},
                {COL_ADDRESS},
                {COL_MOO},
                {COL_SOI},
                {COL_ROAD},
                {COL_TAMBOL},
                {COL_AMPHUR},
                {COL_PROVINCE},
                {COL_ZIPCODE}
            FROM {TABLE_NAME}
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # จัดรูปแบบข้อมูล JSON ให้ตรงกับที่ Frontend (JavaScript) ต้องการ
        for row in rows:
            companies.append({
                "prefix": getattr(row, COL_PREFIX, '').strip(),
                "mainName": getattr(row, COL_CNAME, '').strip(),
                "taxId": getattr(row, COL_TAXID, '').strip(),
                "establishmentName": getattr(row, COL_BRANCH, '').strip(),
                "number": getattr(row, COL_ADDRESS, '').strip(),
                "moo": getattr(row, COL_MOO, '').strip(),
                "soi": getattr(row, COL_SOI, '').strip(),
                "road": getattr(row, COL_ROAD, '').strip(),
                "subdistrict": getattr(row, COL_TAMBOL, '').strip(),
                "district": getattr(row, COL_AMPHUR, '').strip(),
                "province": getattr(row, COL_PROVINCE, '').strip(),
                "postalCode": getattr(row, COL_ZIPCODE, '').strip(),
            })

        cnxn.close()
        print(f"✅ (Backend) ดึงข้อมูลสำเร็จ: {len(companies)} รายการ")
        return companies, None

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        error_message = f"Database Error: {sqlstate} - {ex}"
        print(f"❌ (Backend) เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {error_message}")
        return [], error_message
    except Exception as e:
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
        return jsonify({
            "error": "ไม่สามารถดึงข้อมูลจากฐานข้อมูลได้",
            "details": error
        }), 500
    return jsonify(companies)

if __name__ == '__main__':
    app.run(debug=True, port=5000)