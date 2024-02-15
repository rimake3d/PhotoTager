import streamlit as st

st.header("Feel free to Contact Us")

contact_form = """
<form action="https://formsubmit.co/984bef4ae96a159a7247d4318d39aa09" method="POST">
     <input type="text" name="name" placeholder="Your Name" required>
     <input type="email" name="email" placeholder = "Yourn email address"  required>
     <textarea name="message" placeholder="Details of your problem"></textarea>
     <input type="hidden" name="_autoresponse" value="Thank you for reaching out to us! This is a quick note to let you know we've received your message and appreciate you taking the time to write to us.">
     <button type="submit">Send</button>
</form>


"""
st.markdown(contact_form, unsafe_allow_html=True)

def local_css(file_name):
     with open(file_name) as f:
          st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
          
local_css("/workspaces/PhotoTager/pages/style/style.css")