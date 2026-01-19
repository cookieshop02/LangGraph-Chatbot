
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



    response = chatbot.invoke({'messages': [HumanMessage(content = user_input)]}, config = config)
    ai_message = response['messages'][-1].content
    #now let's make for ai message
    st.session_state['message_history'].append({'role':'Ai', 'content': ai_message})
    with st.chat_message('Ai'):
        st.text(ai_message)