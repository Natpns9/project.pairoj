from flask import Flask, jsonify
import pyodbc

# --- ส่วนของการตั้งค่า Flask ---
app = Flask(__name__)

# --- ส่วนของการตั้งค่าการเชื่อมต่อฐานข้อมูล (เหมือนเดิม) ---
SERVER_NAME = 'PairojS2'
DATABASE_NAME = 'SSalakDB'
USERNAME = 'sa'
PASSWORD = 'Abc1234'
TABLE_NAME = 'dbo.SClient' # <--- !!! แก้เป็นชื่อตารางที่เก็บข้อมูลบริษัท

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)

def get_companies_from_db():
    """ฟังก์ชันสำหรับดึงข้อมูลบริษัทจากฐานข้อมูล"""
    companies = []
    try:
        cnxn = pyodbc.connect(connection_string)
        print("✅ (Backend) เชื่อมต่อฐานข้อมูลสำเร็จ!") 
        cursor = cnxn.cursor()
        # !!! แก้ชื่อคอลัมน์ CompanyName, TaxID ให้ตรงกับในตารางของพี่ก้อ
        query = f"SELECT Taxid, CName, TrCName FROM {TABLE_NAME}"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            companies.append({"CompanyName": row.CompanyName, "TaxID": row.TaxID})
        cnxn.close()
               # --- บรรทัดที่เพิ่มเข้ามา เพื่อบอกว่าดึงข้อมูลมาได้กี่รายการ ---
        print(f"✅ (Backend) ดึงข้อมูลบริษัทมาได้ {len(companies)} รายการ")
    except pyodbc.Error as ex:
        # --- บรรทัดเดิมที่มีอยู่แล้ว เราแค่เติม (Backend) เข้าไปให้ชัดเจน ---
        print(f"❌ (Backend) เชื่อมต่อฐานข้อมูลล้มเหลว: {ex}")
    return companies

# --- สร้าง API Endpoint ---
@app.route('/api/companies')
def get_companies():
    """นี่คือ 'ท่อส่งข้อมูล' ของเรา"""
    company_data = get_companies_from_db()
    return jsonify(company_data)

# --- ส่วนสำหรับรันโปรแกรม ---
if __name__ == '__main__':
    # debug=True ทำให้เซิร์ฟเวอร์รีสตาร์ทเองเมื่อเราแก้ไขโค้ด
    app.run(debug=True)