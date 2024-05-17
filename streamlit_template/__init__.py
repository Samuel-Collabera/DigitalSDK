import streamlit as st
import os
import __main__
from PIL import Image
from .utils import *
from pathlib import Path
import asyncio
from uuid import uuid4
import pandas as pd
import datetime


project_path = Path(__main__.__file__).parent
module_path = Path(__file__).parent

streamlit_config_folder = project_path / ".streamlit"
streamlit_config_file = streamlit_config_folder / 'config.toml'

image_folder = module_path / "images"


if not os.path.exists(streamlit_config_folder):
    os.mkdir(streamlit_config_folder)

if not os.path.exists(streamlit_config_file):
    print("Please restart streamlit to get the new themes")

with open(streamlit_config_file, 'w') as f:
    f.write("""
[theme]
primaryColor="#E63B60"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#d8dff3"
textColor="#31333F"
font="sans serif"
""")


class TitleTemplate:

    def __init__(self, page_title='Untitled App', layout='wide', image=image_folder / 'C_for_Collabera.png'):
        im = Image.open(image)
        try:
            st.set_page_config(
                page_title=page_title, 
                layout=layout,
                page_icon = im,
            )
        except Exception as e:
            if "can only be called once per app page" in str(e):
                st.rerun()
            else: 
                raise e
        st.start_chat_message = self.start_chat_message
    
    def __enter__(self):
        return st

    def start_chat_message(self, history_id=0):
        """
        Start a chat session with a history ID. The same history ID has to be given later to display the chat.
        If no history ID is given, a default id 0 will be used and need not be given later to display the chat.
        """
        h_id = hash(history_id)
        if h_id not in st.session_state:
            st.session_state[h_id] = []
        return st.session_state[h_id]

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

class SidebarTemplate:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def write(self, markdown_text, unsafe_allow_html=False):
        import markdown
        if not unsafe_allow_html:
            markdown_html = f'<div style="color:white">{markdown.markdown(markdown_text)}</div>'
        else:
            markdown_html = markdown_text
        st.markdown(markdown_html, unsafe_allow_html=True)
        

    def __enter__(self):
        st.markdown(
        """
        <style>
            div[data-testid="stHeading"] {
                position: fixed;
                width: 100%;
                background-color: #ffffff; /* Set the background color to white */
                z-index: 1000;
                padding: 10px;
                top: 6%;
                
            }
            
        </style>
        """,
        unsafe_allow_html=True
    )

        st.markdown('<style>div.block-container {padding-top:5rem;}</style>', unsafe_allow_html=True)
        st.markdown(""" <style> section[data-testid=stSidebar] {background-color: #0E052D;} </style>""", unsafe_allow_html=True)

        sidebar = st.sidebar
        self.sidebar = st.sidebar
        image_path = image_folder / "collabera_logo.png"
        sidebar.image(str(image_path))

        if 'title' in self.kwargs:
            sidebar.markdown(f"""<div style='color:white; padding: 6% 2% 0px 15%; font-size:40px'>{self.kwargs['title']}</div>""", unsafe_allow_html=True)

        col1, col2= sidebar.columns([2,1])
        if "subtitle" in self.kwargs:
            col1.markdown(f"""<div style='color:white; padding: 6% 2% 15% 15%;'>{self.kwargs['subtitle']}</div>""", unsafe_allow_html=True)
        
        if 'logo' in self.kwargs:
            col2.image(self.kwargs['logo'])
        
        # sidebar.write = self.write
        return sidebar

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.sidebar.markdown("""<div style='color: white; 
            left: 2%;
            width: 100%;
            padding-top: 5%;
            font-size: 80%;
            text-align: center;'>
            <a href="https://www.collaberadigital.com/" style="color: white;">Click here to Know more</a>""", 
            unsafe_allow_html=True
        )
        self.sidebar.markdown("""<div style='color: white; 
            position: fixed;
            bottom: 5%;
            left: 2%;
            width: 100%;
            font-size: 90%;
            text-a: center;'>
            ©2024 Collabera Digital | All Rights Reserved</div>""", 
            unsafe_allow_html=True
        )
    
class MainPageTemplate:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.container = st
        st.show_about_app = self.show_about_app
        if 'title' in kwargs:
            st.title(kwargs['title'])

    def display_chats(self, history, avatar={"user":image_folder/f'userlogo.png', "assistant":image_folder/f'C_for_Collabera.png' }):
        chat_styles = """
            <style>
                .chat-row {
                    display: flex;
                    align-items: flex-start;
                    margin-bottom: 10px;
                }

                .user-message {
                    background: linear-gradient(135deg, rgb(0, 178, 255) 0%, rgb(0, 106, 255) 100%);
                    color: white;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: right;
                    word-wrap: break-word;
                    max-width: 500px;
                    margin-right: 10px;
                }

                .agent-message {
                    background: rgb(240, 242, 246);
                    color: black;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: left;
                    word-wrap: break-word;
                    max-width: 500px;
                    margin-left: 10px;
                }
                
                .avatar {
                    border-radius: 50%;
                }
            </style>
        """
        st.markdown(chat_styles, unsafe_allow_html=True)
        for message in history:
            self._display_chat(message, avatar)

    def _display_chat(self, message, avatar, is_latest=False, feedback_file=None):
        is_user = message["role"] == "user"

        with st.container():
            if is_user:
                msg_style = "user-message"
                image_path = avatar['user']
                image_base64 = image_to_base64(image_path)
                icon_src = f"data:image/png;base64,{image_base64}"
                st.markdown(f"""
                <div class="chat-row" style="justify-content: flex-end;">
                    <div class="{msg_style}">{message['content']}</div>
                    <img src="{icon_src}" width=40 height=40 class="avatar">
                </div>
                """, unsafe_allow_html=True)
            else:
                msg_style = "agent-message"
                image_path = avatar['assistant']
                image_base64 = image_to_base64(image_path)
                feedback_value = message.get('feedback', '')
                icon_src = f"data:image/png;base64,{image_base64}"
                st.markdown(f"""
                <div class="chat-row" style="justify-content: flex-start;">
                    <img src="{icon_src}" width=40 height=40 class="avatar">
                    <div class="{msg_style}">{message['content']}</div>
                    <p>{feedback_value}</p>
                </div>
                """, unsafe_allow_html=True)
                if not is_latest:
                    if 'feedback' in message:
                        pass
                    else:
                        message['feedback'] = '👍'
                        message['comment'] = "Good"

                        if feedback_file:
                            if not os.path.exists(feedback_file):
                                with open(feedback_file, 'w') as f:
                                    f.write("uuid,user_query,llm_content,feedback,comment,timestamp")
                            df = pd.read_csv(feedback_file)
                            df.loc[len(df)] = [message['uuid'], message['content'], message['feedback'], message['feedback_content'], datetime.datetime.now()]
                            df.to_csv(feedback_file, index=False)
                else:
                    pass
    
    def display_loading(self, callback, query, feedback_file=None):
        """
        Display loading response till answer is generated. Similar to st.spinner.
        """
        loading_placeholder = st.empty()
        asyncio.run(agent_loading_mssg(loading_placeholder, image_folder/f'C_for_Collabera.png'))
        result = callback(query)
        loading_placeholder.empty()
        agent_message = {"role": "assistant", "content": result, "message_id": str(uuid4()), 'query':query}
        self._display_chat(agent_message, {'assistant':image_folder/f'C_for_Collabera.png'})

        return agent_message

    

    def show_about_app(self, data):
        if type(data) == str:
            data = [{"heading":"About the app", "description":data}]
        items = len(data)
        cols = st.columns(items)
        st.markdown('<div style="padding: 2% 2%;"></div>', unsafe_allow_html=True)
        for i in range(items):
            with cols[i]:
                with st.container(border=True, height=250):
                    st.markdown(f"#### {data[i]['heading']}")
                    st.markdown(data[i]['description'])

    def __enter__(self):
        self.container.display_chats = self.display_chats
        self.container.display_loading = self.display_loading
        if self.kwargs.get("hide_uploader", False):
            st.markdown("<style>div[data-testid=stFileUploader]{display:none;}</style>",unsafe_allow_html=True)
        return self.container
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass
