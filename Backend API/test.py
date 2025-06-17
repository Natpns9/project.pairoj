# Test.py - โค้ดสำหรับค้นหาชื่อคอลัมน์ทั้งหมดในตาราง
import pyodbc

# --- ข้อมูลการเชื่อมต่อ ---
SERVER_NAME = 'PairojS2'
DATABASE_NAME = 'SSalakDB'
USERNAME = 'sa'
PASSWORD = 'Abc1234'
TABLE_NAME = 'SClient'  # ระบุแค่ชื่อตาราง ไม่ต้องมี dbo.
SCHEMA_NAME = 'dbo'     # ระบุ schema แยกต่างหาก

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)

print(f"🚀 กำลังค้นหารายชื่อคอลัมน์ทั้งหมดในตาราง '{SCHEMA_NAME}.{TABLE_NAME}'...")

try:
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    print("✅ เชื่อมต่อสำเร็จ!")

    # ใช้ฟังก์ชันพิเศษของ pyodbc เพื่อดึงรายชื่อคอลัมน์
    columns = cursor.columns(table=TABLE_NAME, schema=SCHEMA_NAME)

    print("\n" + "="*40)
    print("🎉 ผลการตรวจสอบ: พบรายชื่อคอลัมน์ทั้งหมดดังนี้:")
    print("="*40)

    count = 0
    for row in columns:
        print(f"  - {row.column_name}")
        count += 1

    if count == 0:
        print("ไม่พบคอลัมน์ใดๆ หรืออาจจะหาตารางไม่เจอ")

    print("="*40)
    cnxn.close()

except pyodbc.Error as ex:
    print(f"❌ เกิดข้อผิดพลาด: {ex}")