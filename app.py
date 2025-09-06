import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.callbacks import StreamlitCallbackHandler
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
import os

st.set_page_config(page_title="Chat with SQL")
st.write("Chat with SQL DB")

LOCAL_DB = 'USE_LOCALDB'
MYSQL = "USE_MYSQL"

# Database selection
radio_opt = ["Use Sqlite3 db - student.db", "Connect to your SQL Database"]
selected_opt = st.sidebar.radio(label="Choose the db which you want to chat", options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Enter SQL Host")
    mysql_user = st.sidebar.text_input("Enter SQL User")
    mysql_password = st.sidebar.text_input("Enter SQL password", type="password")
    mysql_db = st.sidebar.text_input("My SQL Database")
else:
    db_uri = LOCAL_DB

api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not db_uri:
    st.info("Please enter the database information")

if not api_key:
    st.info("Please enter the GROQ API")
    st.stop()

@st.cache_resource(ttl='2h')
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCAL_DB:
        # Get absolute path to the database file
        dbfilepath = Path(__file__).parent / 'student.db'
        dbfilepath = dbfilepath.absolute()
        
        # Verify the file exists
        if not dbfilepath.exists():
            st.error(f"Database file not found at: {dbfilepath}")
            st.stop()
            
        # Create SQLite connection string
        sqlite_uri = f"sqlite:///{dbfilepath}"
        return SQLDatabase.from_uri(sqlite_uri)
        
    elif db_uri == MYSQL:
        if not (mysql_db and mysql_host and mysql_password and mysql_user):
            st.error("Please provide all the sql connection details")
            st.stop()
        return SQLDatabase.from_uri(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")

# Initialize LLM
llm = ChatGroq(api_key=api_key, model='llama-3.3-70b-versatile', streaming=True)

# Configure database
try:
    if db_uri == MYSQL:
        db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
    else:
        db = configure_db(db_uri)
except Exception as e:
    st.error(f"Failed to connect to database: {str(e)}")
    st.stop()

# Initialize agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Initialize chat history
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state.messages = [{"role": "assistant", "content": "Hi, How may I help you?"}]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# Handle user input
if user_query := st.chat_input(placeholder="Ask anything to the database"):
    st.session_state.messages.append({'role': 'user', 'content': user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(user_query, callbacks=[streamlit_callback])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            st.error(f"Error processing your query: {str(e)}")