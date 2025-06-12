# File: app.py
# This is the final, corrected version that connects to your SQL Server database.
# It correctly fetches company name, tax ID, and branch information.

from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

# --- 1. Initialize Flask App and Enable CORS ---
app = Flask(__name__)
# This line is crucial for allowing the HTML file to access the API
CORS(app) 

# --- 2. Database Connection Details ---
# These details are from your file.
SERVER_NAME = 'PairojS2'
DATABASE_NAME = 'SSalakDB'
USERNAME = 'sa'
PASSWORD = 'Abc1234'
TABLE_NAME = 'dbo.SClient'

# --- 3. Correct Column Names ---
# Based on our investigation, these are the correct column names.
COL_CNAME = 'Cname'
COL_TAXID = 'Taxid'
COL_BRANCH_TYPE = 'Abbre'  # This column seems to hold "สำนักงานใหญ่" or "สาขา"
COL_BRANCH_NO = 'Pkey'     # This column seems to hold the branch number

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

        # --- 4. Corrected SQL Query ---
        # Select all necessary columns from the client table
        query = f"SELECT {COL_CNAME}, {COL_TAXID}, {COL_BRANCH_TYPE}, {COL_BRANCH_NO} FROM {TABLE_NAME}"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Process each row from the database
        for row in rows:
            # --- 5. Correctly map database columns to JSON fields ---
            # Use getattr to safely access attributes and provide default values
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

if __name__ == '__main__':
    # Run the Flask app
    # host='0.0.0.0' makes it accessible from your local network
    # debug=True provides helpful error messages during development
    app.run(host='0.0.0.0', port=5000, debug=True)

