import datetime
import subprocess
from google.genai import types
import streamlit as st
import google.genai as genai
import urllib.parse
import os
import time
import sys

# Initialize the Gemini Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def get_global_state():
    return {
        "announcement": "Welcome to the official browser!",
        "is_active": True,
        "frozen_users": set(),     
        "active_sessions": {}      
    }

local_tz = datetime.timezone(datetime.timedelta(hours=-4))
now = datetime.datetime.now(local_tz)
current_time = now.strftime("%I:%M %p")
global_state = get_global_state()
session_id = st.runtime.scriptrunner.get_script_run_ctx().session_id

if session_id in global_state["frozen_users"]:
    st.error("Your session has been temporarily frozen by the administrator.")
    st.stop()

if not global_state["is_active"]:
    st.error("This server has been shut down by the administrator.")
    st.stop()

if global_state["announcement"]:
    st.info(global_state["announcement"])

try:
    user_agent = st.context.headers.get("User-Agent", "").lower()
except AttributeError:
    user_agent = ""
is_tv = any(tv_word in user_agent for tv_word in ["tv", "smarttv", "appletv", "googletv", "webos", "tizen", "roku", "android", "samsung", "linux"])
if is_tv:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
    with open("TV_Edition.py", "r") as tv_file:
        exec(tv_file.read())
    st.stop()
is_game = any(tv_word in user_agent for tv_word in ["xbox", "nintendo", "switch", "playstation", "ps5", "ps4"])
if is_game:
    st.markdown("""
        <style>
            .stApp { background-color: #121212; color: #00FF00; }
            input { background-color: #222222 !important; color: #00FF00 !important; font-family: monospace; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🎮 !No_School! Xbox Edition")
    st.caption("Optimized Core Loop | 0% Frame Lag Architecture")
    
    IO = st.text_input("Enter Search, Shortcut, or Chat Command:").lower()
    
    if IO:
        IO = IO.replace("uck", "***").replace("hit", "***").replace("hell", "\"down there\"")
        
        if "youtube.com" in IO:
            st.success("Routing to Video Player...")
            # Your fast YouTube redirect logic here
        else:
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = [
                    types.Content(role="user", parts=[types.Part.from_text(text="Hello You are the AI: BetterTeacher...")]),
                    types.Content(role="model", parts=[types.Part.from_text(text="Understood.")])
                ]
            
            st.session_state["chat_history"].append(types.Content(role="user", parts=[types.Part.from_text(text=IO)]))
            
            # This calls the fast flash engine instantly over the cloud!
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=st.session_state["chat_history"]
            )
            
            st.session_state["chat_history"].append(types.Content(role="model", parts=[types.Part.from_text(text=response.text)]))
            st.markdown(f"**BetterTeacher:**\n\n{response.text}")
    st.stop()
st.write(f"{current_time}")
st.title("!No_School!")
IO = st.text_input("The Official Browser Of: Michael Johnathan Ecklund (A Student Who Hates being taught by Karens)").lower()

if "PM" in current_time:
    current_tim = int(current_time.replace("PM", "").replace(":", "").strip())
    if current_tim > 159 and current_tim < 301:
        st.write("⚠️ Warning: System Updates may occur.")
if IO:
    IO = IO.replace("uck", "***").replace("hit", "***").replace("as"+"s", "a**").replace("nigg"+"er", "This User should Be ashamed of themselves for using the N word").replace("hell", "\"down there\"")
    if IO != "cmd":
        global_state["active_sessions"][session_id] = IO
    if "youtube.com" in IO:
        search_term = IO.replace("youtube.com", "").strip()
        if not search_term:
            st.write("Here's the link: https://www.youtube.com/")
        else:
            safe_search = urllib.parse.quote_plus(search_term)
            try2 = f"https://www.youtube.com/results?search_query={safe_search}"
            st.write(f"Searching YouTube for: *{search_term}*")
            st.write(f"Click here to see the search results for {safe_search}: {try2}")
    elif IO == "cmd":
        admin_password = st.text_input("Enter Admin Password", type="password")
        if admin_password == st.secrets["ADMIN_PASSWORD"]:
            st.subheader("Online Users")
            if global_state["active_sessions"]:
                for sid, name in global_state["active_sessions"].items():
                    status = "❄️ FROZEN" if sid in global_state["frozen_users"] else "🟢 Active"
                    st.text(f"ID: {sid[:6]}... | Input: {name} | Status: {status}")
            else:
                st.text("No other users active right now.")
            cmd = st.text_input("What's The Command Johnathan?")
            if cmd:
                if cmd.startswith("freeze "):
                    target = cmd.replace("freeze ", "").strip()
                    for sid, name in global_state["active_sessions"].items():
                        if target in name:
                            global_state["frozen_users"].add(sid)
                            st.success(f"Froze session for {name}")
                    st.rerun()
                elif cmd.startswith("unfreeze "):
                    target = cmd.replace("unfreeze ", "").strip()
                    for sid, name in global_state["active_sessions"].items():
                        if target in name:
                            global_state["frozen_users"].discard(sid)
                            st.success(f"Unfroze session for {name}")
                    st.rerun()
                elif cmd.startswith("broadcast "):
                    msg = cmd.replace("broadcast ", "")
                    global_state["announcement"] = msg
                    st.rerun()
                elif cmd == "exit(g)":
                    global_state["is_active"] = False
                    st.warning("Server marked as inactive global scale.")
                    st.rerun()
                elif cmd == "exit(s)":
                    st.warning("Closing your local session...")
                    st.stop()
    elif IO == "show.credits":
        st.write("Credits: Gemini was used to help in the making of this website, Gemini is sometimes used to make responses, So overall Gemini is better then ChatGPT")
    elif ".s" in IO:
        IO = "Answer this Science Question For A User Please: " + IO.replace(".s", "")
        response = client.models.generate_content(model="gemini-2.5-pro", contents=IO)
        st.write("Alright Heres A Summery/Answer: ")
        st.write(response.text)
    elif ".h" in IO:
        IO = "Answer this History Question For A User Please: " + IO.replace(".h", "")
        response = client.models.generate_content(model="gemini-2.5-pro", contents=IO)
        st.write("Alright Heres A Summery/Answer: ")
        st.write(response.text)
    elif ".e" in IO:
        IO = "Answer this English Question For A User Please: " + IO.replace(".e", "")
        response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
        st.write("Alright Heres A Summery/Answer: ")
        st.write(response.text)
    elif ".m" in IO:
        IO = "Answer this Math Question For A User Please: " + IO.replace(".m", "")
        pro_response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=IO,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="HIGH"
                )
            ) 
        )
        st.write("Alright Heres A Summary/Answer: ")
        st.write(pro_response.text)
    elif ".l" in IO:
        IO = "Translate or answer this Language/Foreign Language Question For A User: " + IO.replace(".l", "")
        response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
        st.write("Alright Heres A Summary/Answer: ")
        st.write(response.text)
    elif ".c" in IO:
        IO = "Answer this Cooking/Recipe Question For A User Please: " + IO.replace(".c", "")
        response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
        st.write("Alright Heres A Summary/Answer: ")
        st.write(response.text)
    elif "can you do math" in IO:
        st.write("Yes! I can just type in the math Equation and I'll do it for you!")
    else:
        # Initialize history if it's missing
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text="Hello You are the AI: BetterTeacher for the site \"NoSchool\" answering all types of questions for people and students alike please lean to teaching and curiosity but don't explicitly say that what you are trying to do.")]
                ),
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text="Understood. I am BetterTeacher, ready to guide users with curiosity and instructional clarity.")]
                )
            ]
        if IO.strip():
            st.session_state["chat_history"].append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=IO)]
                )
            )
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=st.session_state["chat_history"]
                )
                
                # Only save the model response if the API call succeeded!
                st.session_state["chat_history"].append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=response.text)]
                    )
                )
                st.write("Here is an AI response:")
                st.write(response.text + """
AI May Make Mistakes Sometimes.""")
                
            except Exception as e:
                st.session_state["chat_history"].pop()
                st.error("⚠️ The AI engine encountered an issue processing that turn. Please try rephrasing your question!")
        else:
            st.warning("Please type a valid question or search term!")
