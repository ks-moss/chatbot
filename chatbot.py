import sqlite3
import nltk
from nltk.chat.util import Chat, reflections
from spellchecker import SpellChecker


# Initialize the database connection
db_connection = sqlite3.connect("chatbot_data.db")
cursor = db_connection.cursor()

# Create an instance of SpellChecker
spell = SpellChecker()

# Check and Correct Typos
def correct_typos(user_input):
    words = user_input.split()
    corrected_words = [spell.correction(word) for word in words]
    corrected_input = ' '.join(corrected_words)
    return corrected_input


# Define pairs of patterns and responses
pairs = [
    ["hi|hello|hey", ["Hello!", "Hi there!"]],
    ["how are you?", ["I'm good, thanks!", "I'm just a chatbot, but I'm here to help!"]],
    ["bye|goodbye", ["Goodbye!", "Have a great day!"]],
    ["None", ["I'm sorry, I don't have information on that.", "I can't provide details about that."]],
]

# Create a chatbot
chatbot = Chat(pairs, reflections)

# Function to fetch data from the database
def get_info_from_database(topic):
    cursor.execute("SELECT response FROM knowledge_base WHERE topic=?", (topic,))
    result = cursor.fetchone()
    return result[0] if result else None

# Function to interact with the chatbot
def chat_with_bot():
    print("Bot: Hi! How can I help you today?")
    while True:
        user_input = input("You: ")
        corrected_input = correct_typos(user_input)

        if corrected_input.lower() == 'exit':
            print("Bot: Goodbye!")
            break
        elif corrected_input.startswith("tell me about"):
            topic = corrected_input[13:].strip()
            response = get_info_from_database(topic)
            if response is None:
                response = chatbot.respond("None")
        else:
            response = chatbot.respond(corrected_input)
            if response is None:
                response = get_info_from_database(corrected_input)
                if response is None:
                    response = chatbot.respond("None")
        print("Bot:", response)

# Start the conversation
if __name__ == "__main__":
    chat_with_bot()

# Close the database connection when done
db_connection.close()
