# File: app.py
# This is the final, corrected version ready for deployment on Render.
# It uses Environment Variables for security.

import os
from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

# --- 1. Initialize Flask App and Enable CORS ---
app = Flask(__name__)
# This line is crucial for allowing the HTML file to access the API
CORS(app) 

# --- 2. Database Connection Details (Loaded from Environment Variables) ---
# These will be set in the Render dashboard, not in the code.
SERVER_NAME = os.environ.get('DB_SERVER')
DATABASE_NAME = os.environ.get('DB_NAME')
USERNAME = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASS')
TABLE_NAME = 'dbo.SClient'

# --- 3. Correct Column Names ---
COL_CNAME = 'Cname'
COL_TAXID = 'Taxid'
COL_BRANCH_TYPE = 'Abbre'
COL_BRANCH_NO = 'Pkey'

# Create the connection string for SQL Server
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)

def get_companies_from_db():
    """
    Connects to the SQL Server database, fetches all client data,
    and formats it into a list of dictionaries.
    """
    companies = []
    try:
        # Establish a connection to the database
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        # --- 4. SQL Query ---
        query = f"SELECT {COL_CNAME}, {COL_TAXID}, {COL_BRANCH_TYPE}, {COL_BRANCH_NO} FROM {TABLE_NAME}"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Process each row from the database
        for row in rows:
            # --- 5. Map database columns to JSON fields ---
            companies.append({
                "CompanyName": getattr(row, COL_CNAME, '').strip() if getattr(row, COL_CNAME) else '',
                "TaxID": getattr(row, COL_TAXID, '').strip() if getattr(row, COL_TAXID) else '',
                "BranchType": getattr(row, COL_BRANCH_TYPE, 'สำนักงานใหญ่').strip() if getattr(row, COL_BRANCH_TYPE) else 'สำนักงานใหญ่',
                "BranchNo": getattr(row, COL_BRANCH_NO, '').strip() if getattr(row, COL_BRANCH_NO) else ''
            })
            
        # Close the connection
        cnxn.close()
        print(f"✅ (Backend) Successfully fetched {len(companies)} companies from the database.")
    except Exception as e:
        # Print any error that occurs during the process
        print(f"❌ (Backend) An error occurred: {e}")
    
    return companies

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """
    API endpoint that returns the company list in JSON format.
    """
    return jsonify(get_companies_from_db())

# Note: The if __name__ == '__main__': block has been removed 
# as Render uses Gunicorn to run the app.