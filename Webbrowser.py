import google.genai as genai
import urllib.parse
import time
import streamlit as st
import sys

st.title("NoSchool")
IO = st.text_input("The Official Browser Of: Michael Johnathan Ecklund (A Student Who Hates being taught by Karens)").lower()

if IO:
    if "youtube.com" in IO:
        search_term = IO.replace("youtube.com", "").strip()
        if not search_term:
            st.write("Here's the link: https://www.youtube.com/")
        else:
            safe_search = urllib.parse.quote_plus(search_term)
            try2 = f"https://www.youtube.com/results?search_query={safe_search}"
            st.write(f"Searching YouTube for: *{search_term}*")
            st.write(f"Click here to see the search results for {search_term}: {try2}")
            
    elif "+" in IO or "plus" in IO or "-" in IO or "minus" in IO or "*" in IO or "times" in IO or "divided by" in IO or "/" in IO or "to the power of" in IO or "raised to" in IO or "cubed" in IO or "sqaured" in IO:
        try:
            sys.set_int_max_str_digits(99999)
            math = IO.lower().replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/").replace("hello", "hi").replace("hi", "").replace("to the power of", "**").replace("raised to", "**").replace("squared", "**2").replace("cubed", "**3").replace("the", "").replace("solve", "").replace("math", "").replace("do", "").replace("can ", "h").replace("you", "i").replace(".", "").replace("?", "").replace("!", "").replace(" ", "").replace("me", "").replace("for", "").replace("whatis ", "")
            
            if "hi" in math:
                st.write("Yes I can do that for you!")
                time.sleep(1)
                math = math.replace("hi", "")
                
            elif "a" in math or "b" in math or "c" in math or "d" in math or "e" in math or "f" in math or "g" in math or "h" in math or "i" in math or "j" in math or "k" in math or "l" in math or "m" in math or "n" in math or "o" in math or "p" in math or "q" in math or "r" in math or "s" in math or "t" in math or "u" in math or "v" in math or "w" in math or "x" in math or "y" in math or "z" in math:
                st.write("You can't do math with letters/I don't know algebra lol")
                
            elif "/" in math and "0" in math:
                st.write("Hey dude you know you cant divide by 0 right?")
                
            else:
                answer = eval(math)
                st.write(f"{math} = {answer}")
                
            sys.set_int_max_str_digits(4300)
        except Exception as e:
            st.write(f"An Error has been reported in the calculator: {e}")
            
    else:
        try:
            client = genai.Client()
            response = client.models.generate_content(model="gemini-2.5-flash", contents=IO)
            st.write(f"I don't know what that means yet but heres a response from Gemini:")
            st.write(response.text)
        except Exception as e:
            st.write("NoSchool Fallback: Couldn't reach the Gemini API core link.")
            st.caption(f"Error Details: {e}")
