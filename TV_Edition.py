import streamlit as st
import datetime
import google.genai as genai
from google.genai import types
import urllib.parse
import sys
import time

# 1. Pull the variables down from the main traffic controller script
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
global_state = get_global_state()
session_id = st.runtime.scriptrunner.get_script_run_ctx().session_id

st.write(f"📺 {current_time}")
st.title("!Welcome To NoSchool!")
st.subheader("On the Big Screen!")

IO = st.text_input("The Official TV Browser Of: Michael Johnathan Ecklund (A Student Who Hates being taught by Karens)").lower()

if "PM" in current_time:
    current_tim = int(current_time.replace("PM", "").replace(":", "").strip())
    if current_tim > 159 and current_tim < 301:
        st.write("⚠️ Warning: System Updates may occur.")

if IO:
    IO = IO.replace("uck", "***").replace("hit", "***").replace("as"+"s", "a**").replace("nigg"+"er", "This User should Be ashamed of themselves for using the N word").replace("hell", "\"down there\"")
    
    if IO != "cmd":
        global_state["active_sessions"][session_id] = IO + " (TV)"
        
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
            answer = eval(math)
            st.write(f"{math} = {answer}")
            sys.set_int_max_str_digits(4300)
        except Exception as E:
            st.write(f"An Error has been reported in the calculator: {E}")
            
    elif ".s" in IO:
        IO = "Answer this Science Question For A User Please: " + IO.replace(".s", "")
        response = client.models.generate_content(model="gemini-2.5-pro", contents=IO)
        st.write("Alright Heres A Summary/Answer: ")
        st.write(response.text)
        
    elif ".h" in IO:
        IO = "Answer this History Question For A User Please: " + IO.replace(".h", "")
        response = client.models.generate_content(model="gemini-2.5-pro", contents=IO)
        st.write("Alright Heres A Summary/Answer: ")
        st.write(response.text)
        
    elif ".e" in IO:
        IO = "Answer this English Question For A User Please: " + IO.replace(".e", "")
        response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
        st.write("Alright Heres A Summary/Answer: ")
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
        st.write("Yes! Just type in a math equation or use .m for deep problems, and I'll do it for you!")
        
    else:
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
        st.session_state["chat_history"].append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=IO)]
            )
        )
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
        st.write(response.text)
