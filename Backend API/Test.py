import pyodbc

# --- กรุณาแก้ไขข้อมูลการเชื่อมต่อให้ถูกต้อง ---
SERVER_NAME = 'PairojS2'  # เช่น 'LAPTOP-OF-GOR\SQLEXPRESS' หรือ IP Address
DATABASE_NAME = 'SSalakDB'
USERNAME = 'sa' # เช่น 'sa'
PASSWORD = 'Abc1234'

# สร้าง Connection String สำหรับเชื่อมต่อกับ SQL Server
# Driver อาจจะต้องเปลี่ยนไปตามเวอร์ชันที่ติดตั้งในเครื่อง
# สำหรับ SQL Server 2008 โดยทั่วไปจะใช้ 'SQL Server Native Client 10.0' หรือ 'SQL Server'
connection_string = (
    f"DRIVER=ODBC Driver 17 for SQL Server;"
    f"SERVER=PairojS2;"
    f"DATABASE=SSalakDB;"
    f"UID=sa;"
    f"PWD=Abc1234;"
)

try:
    # เริ่มทำการเชื่อมต่อ
    cnxn = pyodbc.connect(connection_string)
    print("✅ เย้! เชื่อมต่อกับ SQL Server สำเร็จแล้วค่ะ")
    
    # สร้าง Cursor object เพื่อใช้ส่งคำสั่ง SQL
    cursor = cnxn.cursor()
    print("✅ สร้าง Cursor สำเร็จ พร้อมรับคำสั่ง SQL ค่ะ")
    
    # ปิดการเชื่อมต่อเมื่อไม่ใช้งาน
    cnxn.close()
    print("🚪 ปิดการเชื่อมต่อเรียบร้อย")

except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(f"❌ โอ๊ะ! การเชื่อมต่อล้มเหลว: {sqlstate}")
    print(ex)