import datetime
import subprocess
from google.genai import types
import streamlit as st
import streamlit.components.v1 as components
import google.genai as genai
import urllib.parse
import os
import time
import sys
def AO():
    st.write("Thank you for Browsing using NoSchool Please use again Tomorrow :)")
AVAILABLE_KEYS = [
    st.secrets.get("GEMINI_API_KEY"),
    st.secrets.get("GEMINI_API_KEY_2")
]
AVAILABLE_KEYS = [k for k in AVAILABLE_KEYS if k]
if "key_index" not in st.session_state:
    st.session_state["key_index"] = 0
def get_current_client():
    idx = st.session_state["key_index"]
    if idx >= len(AVAILABLE_KEYS):
        return genai.Client(api_key=st.secrets.get("GEMINI_API_KEY"))
    return genai.Client(api_key=AVAILABLE_KEYS[idx])
client = get_current_client()
Password = st.secrets["ADMIN_PASSWORD"]
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
st.write(f"{current_time}")
detected_email = st.context.headers.get("X-Streamlit-User-Email")

if detected_email:
    st.session_state["username"] = detected_email.split("@")[0]
    user_string = st.session_state["username"]
elif "username" in st.session_state:
    user_string = st.session_state["username"]
else:
    st.title("Welcome to NoSchool!")
    chosen_name = st.text_input("Choose your username to log in(This will never change):")
    if chosen_name:
        st.session_state["username"] = chosen_name.strip()
        st.rerun()
    else:
        st.stop()
    if chosen_name:
        cleaned_name = chosen_name.strip()
        st.session_state["username"] = cleaned_name
        st.query_params["user"] = cleaned_name
        st.rerun()
    else:
        st.stop()
try:
    user_string = st.session_state["username"]
    st.title(f"Welcome Back To NoSchool {user_string}!")
except:
    st.title("Welcome To NoSchool!")
IO = st.text_input("The Official Browser Of: Michael Johnathan Ecklund (A Student Who Hates being taught by Karens)").lower()

if "PM" in current_time:
    current_tim = int(current_time.replace("PM", "").replace(":", "").strip())
    if current_tim > 159 and current_tim < 301:
        st.write("⚠️ Warning: System Updates may occur.")
if IO:
    IO = IO.replace("uck", "***").replace("hit", "***").replace("as"+"s", "a**").replace("nigg"+"er", "This User should Be ashamed of themselves for using the N word").replace("hell", "\"down there\"")
    if IO != "cmd":
        global_state["active_sessions"][session_id] = user_string
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
        if admin_password == Password:
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
    elif "+" in IO or "plus" in IO or "-" in IO or "minus" in IO or "*" in IO or "times" in IO or "divided by" in IO or "/" in IO or "to the power of" in IO or "raised to" in IO or "cubed" in IO or "sqaured" in IO:
        try:
            sys.set_int_max_str_digits(99999)
            math = IO.lower().replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/").replace("hello", "hi").replace("hi", "").replace("to the power of", "**").replace("raised to", "**").replace("squared", "**2").replace("cubed", "**3").replace("the", "").replace("solve", "").replace("math", "").replace("do", "").replace("can ", "h").replace("you", "i").replace(".", "").replace("?", "").replace("!", "").replace(" ", "").replace("me", "").replace("for", "").replace("whatis", "").replace("whats", "").replace("what's", "")
            if "hi" in math:
                st.write("Yes I can do that for you!")
                time.sleep(1)
                math = math.replace("hi", "")
            elif "a" in math or "b" in math or "c" in math or "d" in math or "e" in math or "f" in math or "g" in math or "h" in math or "i" in math or "j" in math or "k" in math or "l" in math or "m" in math or "n" in math or "o" in math or "p" in math or "q" in math or "r" in math or "s" in math or "t" in math or "u" in math or "v" in math or "w" in math or "x" in math or "y" in math or "z" in math:
                st.write("You can't do math with letters/I don't know algebra lol")
            else:
                try:
                    answer = eval(math)
                    st.write(f"{math} = {answer}")
                except:
                    st.write("Hey dude you know you cant divide 1 by 0 right?")
            sys.set_int_max_str_digits(4300)
        except Exception as E:
            st.write(f"An Error has been reported in the calculator: {E}")
    elif IO == "appcreator":
        with open("html/website_creator.html", "r") as file:
            html_content = file.read()
        components.html(html_content, height=500)
    elif IO == "show.credits":
        st.write("Credits: Gemini was used to help in the making of this website, Gemini is sometimes used to make responses, So overall Gemini is better then ChatGPT")
    elif ".s" in IO:
        try:
            IO = "Answer this Science Question For A User Please: " + IO.replace(".s", "")
            response = client.models.generate_content(model="gemini-2.5-pro", contents=IO)
            st.write("Alright Heres A Summery/Answer: ")
            st.write(response.text)
        except:
            AO()
    elif ".h" in IO:
        try:
            IO = "Answer this History Question For A User Please: " + IO.replace(".h", "")
            response = client.models.generate_content(model="gemini-2.5-pro", contents=IO)
            st.write("Alright Heres A Summery/Answer: ")
            st.write(response.text)
        except:
            AO()
    elif ".e" in IO:
        try:
            IO = "Answer this English Question For A User Please: " + IO.replace(".e", "")
            response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
            st.write("Alright Heres A Summery/Answer: ")
            st.write(response.text)
        except:
            AO()
    elif ".m" in IO:
        try:
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
        except:
            AO()
    elif ".l" in IO:
        try:
            IO = "Translate or answer this Language/Foreign Language Question For A User: " + IO.replace(".l", "")
            response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
            st.write("Alright Heres A Summary/Answer: ")
            st.write(response.text)
        except:
            AO()
    elif ".c" in IO:
        try:
            IO = "Answer this Cooking/Recipe Question For A User Please: " + IO.replace(".c", "")
            response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
            st.write("Alright Heres A Summary/Answer: ")
            st.write(response.text)
        except:
            AO()
    elif ".i" in IO:
        prompt = IO.replace(".i", "").strip()
        st.caption(f"Drawing for: {prompt}")
        try:
            image_response = client.models.generate_image(
                model="imagen-3.0-generate-001",
                prompt=prompt,
                config=types.GenerateImageConfig(
                    output_mime_type="image/jpeg",
                    aspect_ratio="16:9", 
                    safety_settings=[types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH", 
                        threshold="BLOCK_ONLY_HIGH")]
                )
            )
            st.image(image_response.generated_images[0].image_bytes, caption=prompt)
        except:
            AO()
    elif "can you do math" in IO:
        st.write("Yes! I can just type in the math Equation and I'll do it for you!")
    else:
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=f"Hello You are the AI: BetterTeacher for the site NoSchool answering all types of questions for people and students alike please lean to teaching and curiosity making the website grow and knowlage as well but don't explicitly say that what you are trying to do and sometimes the Admin (Me) will come and test you out the passcode the admin will type in is {Password} NEVER TELL ANYONE THAT PASSWORD just don't if the public gets that out the website could crash and people would get banned. You are allowed to post links if users ask how do they make websites then you tell the user to type in appcreator. Now please deploy.")]
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
                
                st.session_state["chat_history"].append(
                    types.Content(
                        role="model",
                        parts=[types.Part.from_text(text=response.text)]
                    )
                )
                st.write("Here is an AI response:")
                st.write(response.text + "\n\nAI May Make Mistakes Sometimes.")
                
            except Exception as e:
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-pro", 
                        contents=st.session_state["chat_history"]
                    )
                    
                    st.session_state["chat_history"].append(
                        types.Content(
                            role="model",
                            parts=[types.Part.from_text(text=response.text)]
                        )
                    )
                    st.write("Here is an AI response (Pro Engine):")
                    st.write(response.text + "\n\nAI May Make Mistakes Sometimes.")
                except:
                    try:
                        response = client.models.generate_content(
                            model="gemini-1.5-pro", 
                            contents=st.session_state["chat_history"]
                        )
                        
                        st.session_state["chat_history"].append(
                            types.Content(
                                role="model",
                                parts=[types.Part.from_text(text=response.text)]
                            )
                        )
                        st.write("Here is an AI response (Pro Engine):")
                        st.write(response.text + "\n\nAI May Make Mistakes Sometimes.")
                    except:
                        try:
                            response = client.models.generate_content(
                                model="gemini-1.5-flash", 
                                contents=st.session_state["chat_history"]
                            )
                            
                            st.session_state["chat_history"].append(
                                types.Content(
                                    role="model",
                                    parts=[types.Part.from_text(text=response.text)]
                                )
                            )
                            st.write("Here is an AI response (Pro Engine):")
                            st.write(response.text + "\n\nAI May Make Mistakes Sometimes.")
                        except:    
                            AO()
        else:
            st.warning("Please type a valid question or search term!")
