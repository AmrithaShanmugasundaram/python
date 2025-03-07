from flask import Flask, request, jsonify
import mysql.connector
import pdfplumber
import pandas as pd
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Train@1234",
        database="emp_report"  # Change this to your actual database name
    )

def create_table_if_not_exists(cursor, headers):
    column_definitions = ", ".join([f"`{col}` VARCHAR(255)" for col in headers])  # Assuming all data as VARCHAR
    create_table_sql = f"CREATE TABLE IF NOT EXISTS emp_report ({column_definitions})"
    print("Executing SQL:", create_table_sql)
    cursor.execute(create_table_sql)

def process_pdf_and_insert(pdf_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            table = page.extract_table()
            print(f"Extracted Table from Page {page_num + 1}:", table)

            if not table:
                print(f"No table found on Page {page_num + 1}.")
                continue

            headers = table[0]  # Extract column names
            df = pd.DataFrame(table[1:], columns=headers)
            df.dropna(how="all", inplace=True)

            print(f"DataFrame from Page {page_num + 1}:\n", df)

            # Create table dynamically if not exists
            create_table_if_not_exists(cursor, headers)

            # Prepare INSERT query
            column_names = ", ".join([f"`{col}`" for col in headers])  # Handle column names with spaces
            placeholders = ", ".join(["%s"] * len(headers))
            sql = f"INSERT INTO emp_report ({column_names}) VALUES ({placeholders})"

            for _, row in df.iterrows():
                values = tuple(row)
                print(f"Inserting row from Page {page_num + 1}:", values)
                cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()

    return "Successfully inserted data from all pages!"

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(file_path)

    result = process_pdf_and_insert(file_path)

    return jsonify({"message": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
