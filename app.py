import streamlit as st
import time
import uuid
from datetime import datetime
import requests
import json
import os
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Configure Streamlit page
st.set_page_config(
    page_title="Multilingual Chat",
    page_icon="💬",
    layout="wide"
)

# Configure a simple file-based database for multi-user support
DATA_FILE = "chat_data.json"

# Helper functions for data management
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except:
            return {"messages": [], "users": {}}
    else:
        return {"messages": [], "users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Load data at startup
if 'data_loaded' not in st.session_state:
    data = load_data()
    st.session_state.all_messages = data["messages"]
    st.session_state.all_users = data["users"]
    st.session_state.data_loaded = True
    st.session_state.last_update = datetime.now().timestamp()
    
# Create user ID if not exists
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Function to translate text
def translate_text(text, target_language):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text  # Return the translated text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return f"{text} [Translation failed]"

# Function to get new messages
def check_for_updates():
    # In a real app, this would check a database or API
    # For our file-based solution, we'll just reload the file
    data = load_data()
    
    # Check if there are new messages
    if len(data["messages"]) > len(st.session_state.all_messages):
        st.session_state.all_messages = data["messages"]
        st.session_state.all_users = data["users"]
        return True
    
    # Also update users
    if data["users"] != st.session_state.all_users:
        st.session_state.all_users = data["users"]
        return True
        
    return False

# Main app layout
st.title("Multilingual Chat App")

# Sidebar for user settings
with st.sidebar:
    st.header("User Settings")
    username = st.text_input("Username", key="username_input", value="User" + st.session_state.user_id[-4:])
    
    language = st.selectbox(
        "Your Language",
        options=["English", "Spanish", "French", "German", "Chinese", "Japanese", "Russian", "Arabic", "Hindi"],
        index=0,
        key="language_select"
    )
    
    # Map selected language to language code
    language_codes = {
        "English": "en",
        "Spanish": "es", 
        "French": "fr",
        "German": "de",
        "Chinese": "zh-CN",
        "Japanese": "ja",
        "Russian": "ru",
        "Arabic": "ar",
        "Hindi": "hi"
    }
    
    language_code = language_codes[language]
    
    room = st.text_input("Chat Room", value="default", key="room_input")
    
    if st.button("Join/Update"):
        # Update user info
        st.session_state.all_users[st.session_state.user_id] = {
            "username": username,
            "language": language_code,
            "room": room,
            "last_active": datetime.now().timestamp()
        }
        
        # Save updated users
        save_data({
            "messages": st.session_state.all_messages,
            "users": st.session_state.all_users
        })
        
        # Add system message for joining
        new_message = {
            "user_id": st.session_state.user_id,
            "username": "System",
            "content": f"{username} has joined the room.",
            "room": room,
            "timestamp": datetime.now().timestamp(),
            "type": "system"
        }
        
        st.session_state.all_messages.append(new_message)
        save_data({
            "messages": st.session_state.all_messages,
            "users": st.session_state.all_users
        })
        
        st.success(f"Joined room: {room} as {username}")
        
    # Check for updates button
    if st.button("Refresh Chat"):
        if check_for_updates():
            st.success("New messages loaded!")
        else:
            st.info("No new messages.")
            
    st.divider()
    
    # Display users in the current room
    st.subheader("Users in Room")
    current_room = st.session_state.all_users.get(st.session_state.user_id, {}).get("room", "default")
    
    # Filter users by current room and active recently (within last hour)
    current_time = datetime.now().timestamp()
    room_users = [
        user["username"] 
        for user_id, user in st.session_state.all_users.items()
        if user.get("room") == current_room and 
        (current_time - user.get("last_active", 0)) < 3600  # 1 hour
    ]
    
    if room_users:
        for user in room_users:
            st.text(f"• {user}")
    else:
        st.text("No other users in this room")

# Display chat room
current_room = st.session_state.all_users.get(st.session_state.user_id, {}).get("room", "default")
st.subheader(f"Chat Room: {current_room}")

# Display chat messages
chat_container = st.container(height=400)

with chat_container:
    # Filter messages for current room
    current_language = st.session_state.all_users.get(st.session_state.user_id, {}).get("language", "en")
    room_messages = [msg for msg in st.session_state.all_messages if msg["room"] == current_room]
    
    # Display messages
    for msg in room_messages:
        if msg["type"] == "system":
            st.info(msg["content"])
        else:
            is_user = msg["user_id"] == st.session_state.user_id
            
            # Handle translation
            if is_user:
                # Own messages don't need translation
                st.chat_message("user").write(f"**You**: {msg['content']}")
            else:
                # Translate messages from others
                translated = translate_text(msg["content"], current_language)
                original_lang = msg.get("language", "en")
                
                # Only show translation indicator if languages differ
                if original_lang != current_language:
                    st.chat_message("assistant").write(
                        f"**{msg['username']}**: {translated} *(translated from {original_lang})*"
                    )
                else:
                    st.chat_message("assistant").write(
                        f"**{msg['username']}**: {msg['content']}"
                    )

# Message input
with st.form("message_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", key="user_message")
    submitted = st.form_submit_button("Send")
    
    if submitted and user_input:
        user_info = st.session_state.all_users.get(st.session_state.user_id, {})
        
        if not user_info:
            st.error("Please join a room first!")
        else:
            # Create new message
            new_message = {
                "user_id": st.session_state.user_id,
                "username": user_info.get("username", "Anonymous"),
                "content": user_input,
                "room": user_info.get("room", "default"),
                "language": user_info.get("language", "en"),
                "timestamp": datetime.now().timestamp(),
                "type": "message"
            }
            
            # Add message to storage
            st.session_state.all_messages.append(new_message)
            
            # Update last active time
            if st.session_state.user_id in st.session_state.all_users:
                st.session_state.all_users[st.session_state.user_id]["last_active"] = datetime.now().timestamp()
            
            # Save data
            save_data({
                "messages": st.session_state.all_messages,
                "users": st.session_state.all_users
            })
            
            # Force a rerun
            st.rerun()

# Auto-refresh mechanism (every 5 seconds)
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now().timestamp()

current_time = datetime.now().timestamp()
if current_time - st.session_state.last_update > 5:  # 5 seconds
    st.session_state.last_update = current_time
    if check_for_updates():
        st.rerun()

# Help info
st.divider()
