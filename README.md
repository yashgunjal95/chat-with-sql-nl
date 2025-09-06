# Chat with SQL in Natural Language

This project is a Streamlit web app that lets you interact with SQL databases using natural language queries powered by LLMs (Groq Llama-3). You can connect to a local SQLite database or your own MySQL database, ask questions, and get answers directly from your data.

## Features

- **Natural Language SQL Queries:** Ask questions about your database in plain English.
- **Supports SQLite and MySQL:** Easily switch between a local SQLite database (`student.db`) and your own MySQL database.
- **LLM-Powered:** Uses Groq's Llama-3 model for query understanding and generation.
- **Chat History:** Keeps track of your conversation for context.
- **Streamlit UI:** Simple, interactive web interface.

## Getting Started

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Groq API Key](https://groq.com/)
- MySQL database (optional)

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/yashgunjal95/chat-with-sql-nl.git
   cd chat-with-sql-nl/Chat_with_SQL
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Add your SQLite database:**
   - Place your `student.db` file in the same folder as `app.py`.

4. **(Optional) Prepare MySQL database:**
   - Make sure your MySQL server is running and accessible.

### Running the App

```
streamlit run app.py
```

### Usage

1. Open the app in your browser (Streamlit will provide a local URL).
2. Choose your database (SQLite or MySQL) from the sidebar.
3. Enter your Groq API key.
4. For MySQL, enter your connection details.
5. Start chatting with your database!

## Example Queries

- "Show all students with marks above 80."
- "How many students are enrolled in Computer Science?"
- "List the top 5 students by grade."

## Troubleshooting

- **Database not found:** Make sure `student.db` is in the correct folder.
- **API errors:** Check your Groq API key and internet connection.
- **MySQL connection issues:** Verify your credentials and database server status.

## Credits

- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
