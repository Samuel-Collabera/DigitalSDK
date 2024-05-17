import streamlit as st
from uuid import uuid4

class ChatHandler:
    
    def __init__(self, callback_function=None, add_clear_button=False):
        self.add_clear_button = add_clear_button
        self.callback = callback_function
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

    def add_message(self, content, role):
        st.session_state['chat_history'].append({
            'role':role,
            'content':content,
            'message_id':uuid4(),
            'feedback':None,
            'comment':None
        })

    def clear_messages(self):
        st.session_state['chat_history'] = []

    def send_message(self):
        pass