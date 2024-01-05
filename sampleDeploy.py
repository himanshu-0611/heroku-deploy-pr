from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/sample')
def index():
    try:
        # Retrieve the DATABASE_URL from the environment variable
        DATABASE_URL = "postgres://yluddpdreetfxc:c3bc12cbcdb8c8b3f02ef99fe73a56256c7b7e05da1a6daf9f8d27c664a7e419@ec2-107-21-67-46.compute-1.amazonaws.com:5432/db7pdq6ndq5hpt"

        # Check if the DATABASE_URL is not None
        if DATABASE_URL is not None:
            # Connect to the database
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Define the SQL query to select data from the "persons" table
            select_data_query = '''
            SELECT * FROM persons;
            '''

            # Execute the SQL query to retrieve data
            cursor.execute(select_data_query)

            # Fetch all the rows from the result set
            rows = cursor.fetchall()

            # Close the cursor and connection
            cursor.close()
            conn.close()

            # Convert data to a dictionary for JSON response
            data_dict = {"persons": [{"id": row[0], "full_name": row[1]} for row in rows]}
            return jsonify(data_dict)

        else:
            return "DATABASE_URL environment variable is not set."

    except Exception as e:
        # Return an error message if there's an issue connecting to the database or executing queries
        return jsonify({"error": f"Error: {e}"}), 500

if __name__ == '__main__':
    # Use 0.0.0.0 as the host to make it externally accessible
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
