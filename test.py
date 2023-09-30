import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('chatbot_data.db')
cursor = conn.cursor()

# Execute the SQL query to fetch the data
def get_info_from_database(topic):
    cursor.execute("SELECT response FROM knowledge_base WHERE topic=?", (topic,))
    data = cursor.fetchall()
    print(data)

# Close the database connection
get_info_from_database("yourself")
conn.close()
