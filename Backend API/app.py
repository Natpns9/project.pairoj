# app.py (แก้ไขสำหรับกรณีไม่มีข้อมูลสาขา)
from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

SERVER_NAME = 'PairojS2'
DATABASE_NAME = 'SSalakDB'
USERNAME = 'sa'
PASSWORD = 'Abc1234'
TABLE_NAME = 'dbo.SClient'

# --- ใช้ชื่อคอลัมน์ที่เราค้นพบ ---
TABLE_NAME = 'dbo.SClient' 
COL_CNAME = 'Cname'
COL_TAXID = 'Taxid'
COL_BRANCH_TYPE = 'Abbre' # <-- แก้ไขเป็นชื่อที่ถูกต้อง
COL_BRANCH_NO = 'Pkey'  # <-- แก้ไขเป็นชื่อที่ถูกต้อง

connection_string = (f"DRIVER={{ODBC Driver 17 for SQL Server}};" f"SERVER={SERVER_NAME};" f"DATABASE={DATABASE_NAME};" f"UID={USERNAME};" f"PWD={PASSWORD};")

def get_companies_from_db():
    companies = []
    try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        # --- แก้ไข Query ให้ดึงเฉพาะคอลัมน์ที่มีอยู่จริง ---
        query = f"SELECT {COL_CNAME}, {COL_TAXID} FROM {TABLE_NAME}"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            companies.append({
                "CompanyName": getattr(row, COL_CNAME, ''),
                "TaxID": getattr(row, COL_TAXID, ''),
                # --- ส่งค่า default สำหรับข้อมูลสาขาไปแทน ---
                "BranchType": "สำนักงานใหญ่", 
                "BranchNo": ""
            })
        cnxn.close()
        print(f"✅ (Backend) ดึงข้อมูลบริษัทมาได้ {len(companies)} รายการ")
    except Exception as e:
        print(f"❌ (Backend) เกิดข้อผิดพลาด: {e}")
    return companies

@app.route('/api/companies')
def get_companies():
    return jsonify(get_companies_from_db())

if __name__ == '__main__':
    app.run(debug=True)