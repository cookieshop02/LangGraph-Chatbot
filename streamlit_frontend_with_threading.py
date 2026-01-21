
#importing streamlit for frontend
import streamlit as st

from langgraph_backend import chatbot #for backend connection
from langchain_core.messages import HumanMessage
import uuid #to randomly generates thread id again and again

#-----------------------utility funcn----------------------

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_convo(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id': thread_id}}).values['messages']

#session_state(to keep history as it is)
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads'  not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])

#-------------------sidebar UI---------------------------
st.sidebar.title("LangGraph Chatbot")
if st.sidebar.button("New Chat"):
    reset_chat()
st.sidebar.header("My Conversations")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages = load_convo(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage): #current message
                role = 'user'
            else:
                role = 'Ai'

            temp_messages.append({'role': role,'content': msg.content})

        st.session_state['message_history'] = temp_messages

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


    config = {'configurable':{'thread_id': st.session_state['thread_id']}}

    #now let's make for ai message with streaming
    with st.chat_message('Ai'):

        ai_message = st.write_stream(
                message_chunk.content for message_chunk,metadata in chatbot.stream(
                    {'messages': [HumanMessage(content=user_input)]},
                    config = config,
                    stream_mode = 'messages'
                )
            )
        
    st.session_state['message_history'].append({'role':'Ai', 'content': ai_message})


