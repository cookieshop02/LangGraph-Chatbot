
#importing streamlit for frontend
import streamlit as st

from langgraph_backend import chatbot #for backend connection
from langchain_core.messages import HumanMessage


thread_id = 1
config = {'configurable':{'thread_id': thread_id}}

#session_state(to keep history as it is)
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


#loading convo history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#chat_input where we can give input to the chatbot
user_input = st.chat_input("Type here")

if user_input:

    #adding message in the history
    st.session_state['message_history'].append({'role':'user', 'content': user_input})
    
    #displaying message now in chatbot
    with st.chat_message('user'):
        st.text(user_input)




    #now let's make for ai message with streaming
    with st.chat_message('Ai'):

        ai_message = st.write_stream(
                message_chunk.content for message_chunk,metadata in chatbot.stream(
                    {'messages': [HumanMessage(content=user_input)]},
                    config = {'configurable':{'thread_id':'thread-1'}},
                    stream_mode = 'messages'
                )
            )
        
    st.session_state['message_history'].append({'role':'Ai', 'content': ai_message})


