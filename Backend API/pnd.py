import os
from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

# --- 1. Initialize Flask App and Enable CORS ---
app = Flask(__name__)
CORS(app)

# --- 2. กรุณากรอกรายละเอียดการเชื่อมต่อฐานข้อมูลของคุณ ---
SERVER_NAME = "pairojs2"
DATABASE_NAME = "SCSA"
USERNAME = "sa"
PASSWORD = "Abc1234"

# --- 3. ตรวจสอบชื่อตารางและคอลัมน์ในฐานข้อมูลของคุณ ---
TABLE_NAME = 'dbo.CSAC'
COL_PREFIX = 'Cabbre'
COL_CNAME = 'Cname'
COL_TAXID = 'Ctid'
COL_BRANCH = 'Atower'
COL_ADDRESS = 'Ano'
# COL_MOO = 'Amno' # หากมีคอลัมน์ "หมู่ที่" ให้ลบ # แล้วแก้ชื่อให้ถูกต้อง
COL_SOI = 'Asoi'
COL_ROAD = 'Ard'
COL_TAMBOL = 'Asdis'
COL_AMPHUR = 'Adis'
COL_PROVINCE = 'Aprov'
COL_ZIPCODE = 'APCode'

# --- 4. สร้าง Connection String ---
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;"
)

# --- START: ส่วนที่แก้ไขและปรับปรุง ---
def get_companies_from_db():
    companies = []
    try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        # สร้าง Query โดยเลือกคอลัมน์ทั้งหมดที่ Frontend ต้องการ
        query = f"""
            SELECT
                {COL_PREFIX}, {COL_CNAME}, {COL_TAXID}, {COL_BRANCH},
                {COL_ADDRESS}, {COL_SOI}, {COL_ROAD}, {COL_TAMBOL},
                {COL_AMPHUR}, {COL_PROVINCE}, {COL_ZIPCODE}
            FROM {TABLE_NAME}
        """
        cursor.execute(query)
        
        # ดึงชื่อคอลัมน์จาก cursor.description เพื่อความยืดหยุ่น
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        for row in rows:
            # สร้าง dictionary จากชื่อคอลัมน์และข้อมูลในแถวโดยอัตโนมัติ
            row_dict = dict(zip(columns, row))
            
            # (จุดที่แก้ไข) แปลงค่าที่อาจเป็นตัวเลขหรือค่าว่างให้เป็น string ก่อน .strip()
            # เพื่อป้องกัน error: 'float' object has no attribute 'strip'
            companies.append({
                "prefix": str(row_dict.get(COL_PREFIX) or '').strip(),
                "mainName": str(row_dict.get(COL_CNAME) or '').strip(),
                "taxId": str(row_dict.get(COL_TAXID) or '').strip(),
                "establishmentName": str(row_dict.get(COL_BRANCH) or '').strip(),
                "number": str(row_dict.get(COL_ADDRESS) or '').strip(),
                "soi": str(row_dict.get(COL_SOI) or '').strip(),
                "road": str(row_dict.get(COL_ROAD) or '').strip(),
                "subdistrict": str(row_dict.get(COL_TAMBOL) or '').strip(),
                "district": str(row_dict.get(COL_AMPHUR) or '').strip(),
                "province": str(row_dict.get(COL_PROVINCE) or '').strip(),
                "postalCode": str(row_dict.get(COL_ZIPCODE) or '').strip(),
            })

        cnxn.close()
        print(f"✅ (Backend) ดึงข้อมูลสำเร็จ: {len(companies)} รายการ")
        return companies, None

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        error_message = f"Database Error: {sqlstate} - {ex}"
        print(f"❌ (Backend) เกิดข้อผิดพลาด: {error_message}")
        return [], error_message
    except Exception as e:
        error_message = str(e)
        print(f"❌ (Backend) เกิดข้อผิดพลาด: {error_message}")
        return [], error_message
# --- END: ส่วนที่แก้ไขและปรับปรุง ---


@app.route('/api/companies', methods=['GET'])
def get_companies():
    companies, error = get_companies_from_db()
    if error:
        return jsonify({
            "error": "ไม่สามารถดึงข้อมูลจากฐานข้อมูลได้",
            "details": error
        }), 500
    return jsonify(companies)


if __name__ == '__main__':
    # เปลี่ยน port เป็น 5000 ตามมาตรฐาน Flask ทั่วไป
    app.run(debug=True, port=5000)