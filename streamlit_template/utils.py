import base64
import streamlit as st
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    return image_base64

async def agent_loading_mssg(placeholder, image_path):
    loading_css = """
    <style>
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 20px;
    }
    
    .dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: black;
        margin: 0 4px;
        animation: dot-animation 1.5s infinite;
    }
    
    .dot:nth-child(1) {
        animation-delay: 0s;
    }
    
    .dot:nth-child(2) {
        animation-delay: 0.5s;
    }
    
    .dot:nth-child(3) {
        animation-delay: 1s;
    }
    
    @keyframes dot-animation {
        0%, 60%, 100% {
            opacity: 0;
        }
        30% {
            opacity: 1;
        }
    }
    </style>
    """
    
    st.markdown(loading_css, unsafe_allow_html=True)
    image_path = image_path
    image_base64 = image_to_base64(image_path)
    icon_src = f"data:image/png;base64,{image_base64}"
    
    with placeholder.container():
        st.markdown(f"<div class='chat-row' style='justify-content: flex-start;'><img src='{icon_src}' width=40 height=40 class='avatar'><div class='agent-message'><div class='loading'><span class='dot'>.</span><span class='dot'>.</span><span class='dot'>.</span></div></div>", unsafe_allow_html=True)
