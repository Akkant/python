import operator
from typing import TypedDict, Annotated, Sequence

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import streamlit as st
from langchain_core.messages import AIMessage
from langchain_core.messages import SystemMessage
import uuid
from tool_funcs import addSubscription
from langchain_core.messages import HumanMessage, AIMessage
import logging
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", message=".*Pydantic will allow any object.*")
import os
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  
from dotenv import load_dotenv
load_dotenv()

@tool
def add_subscription(user_details:dict, ad_categories:list):
    """
    Tool to Add a subscription for the user.
    """
    try:
        return addSubscription(user_details, ad_categories)
    except Exception as e:
        logger.error(f"Error adding subscription: {e}")
        return "Failed to add subscription"

@tool
def addition(a: int, b: int) -> int:
    """
    Adds two numbers.
    """
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """
    Subtracts two numbers.
    """
    return a - b

tools = [
    add_subscription,
    addition,
    subtract
]

# ---------------------------------------------------
#               Define LLM and Bind All Tools  
# ---------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini"
)
bound_llm = llm.bind_tools(tools)


# ---------------------------------------------------
#                     Define State
# ---------------------------------------------------
class AgentState(TypedDict):
    """
        Represents the state of the agent during the conversation.
        This includes the messages which are exchanged
    """
    messages: Annotated[Sequence[BaseMessage], operator.add]





# -------------------------------
# Topic Classifier
# -------------------------------
def model_call(state: AgentState):
    
    logger.info("In LLM Model")
    
    system_prompt = SystemMessage(content=
        """
           You are a Media company AI agent and your task is to assist users with their queries.
              - When users wants to subscribe to advertisements, you must follow these steps.
                 - Ask for their name, email and phoneNumber
                    - Once you get the details, update those details in variable user_details and wait for user to select adCategories
                 - Ask user to select for categories from this list: ['Sports', 'Entertainment', 'Technology', 'Health', 'Finance']
                    - Once you get the categories, update those details in variable ad_categories
                 - Once you have both user_details and ad_categories, invoke the required tool to add user subscription with user_details and ad_categories
                 - response should be clean and concise, without any unnecessary information.
        """
    )
    response = bound_llm.invoke([system_prompt] + state["messages"])
    print(f"Response from LLM: {response}")
    return {"messages": [response]}


# -------------------------------------------------
#                  Define Tool Node
# -------------------------------------------------

tool_node = ToolNode(tools=tools)



# -------------------------------------------------
#                 Define Router
# -------------------------------------------------
def should_continue(state: AgentState): 
    messages = state["messages"]
    last_message = messages[-1]
    print(f"Last message: {last_message.tool_calls}")
    if not last_message.tool_calls: 
        return "end"
    else:
        return "continue"




# -------------------------------
# LangGraph Definition 
# -------------------------------
graph = StateGraph(AgentState)
graph.add_node("agent_node", model_call)
graph.add_node("tools_node", tool_node)
graph.set_entry_point("agent_node")
graph.add_conditional_edges(
    "agent_node",
    should_continue,
    {
        "continue": "tools_node",
        "end": END,
    },
)
graph.add_edge("tools_node", "agent_node")
app = graph.compile()



if __name__ == "__main__":
    try:
        # Initialize placeholder in session state if not present
        if "placeholderText" not in st.session_state:
            st.session_state.placeholderText = "Type your message here..."
        with open('graph.png','wb') as file:
            file.write(app.get_graph().draw_mermaid_png())
        # Set up page
        st.set_page_config(page_title="Peoples Media Support Agent", layout="wide")
        st.title("🔮Peoples Media Support Agent")
        # Initialize session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "conversation_state" not in st.session_state:
            st.session_state.conversation_state = {"messages": []}
        # Unique session ID for LangGraph
        if "thread_id" not in st.session_state:
            st.session_state.thread_id = "cmedia-support-thread-" + str(uuid.uuid4())
        config = {"configurable": {"thread_id": st.session_state.thread_id}} 
        # Display Chat History (with avatars & timestamps)
        for msg in st.session_state.chat_history:
            if isinstance(msg, HumanMessage):
                with st.chat_message("user", avatar="👨‍💻"):
                    st.markdown(msg.content)
                    st.caption(datetime.now().strftime("%I:%M %p")) 
            elif isinstance(msg, AIMessage):
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg.content)
                    st.caption(datetime.now().strftime("%I:%M %p"))

        # Input Box (at bottom, styled)
        if user_input := st.chat_input(st.session_state.placeholderText):
            # Add user message to history/state
            user_msg = HumanMessage(content=user_input)
            st.session_state.chat_history.append(user_msg)
            st.session_state.conversation_state["messages"].append(user_msg)

            # Show user input immediately
            with st.chat_message("user", avatar="👨‍💻"):
                st.markdown(user_input)
                st.caption(datetime.now().strftime("%I:%M %p"))

            # Call LangGraph app with spinner
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤔 Thinking..."):
                    response = app.invoke(st.session_state.conversation_state, config=config)
                messages = response.get("messages", [])
                ai_msg = messages[-1] if messages and isinstance(messages[-1], AIMessage) else None
                content = ''
                if ai_msg:
                    st.markdown(ai_msg.content)
                    st.caption(datetime.now().strftime("%I:%M %p"))
                    st.session_state.chat_history.append(ai_msg)
                else:
                    st.markdown("⚠️ Sorry, I couldn't understand that.")
                st.rerun()


    except Exception as e:
        logger.error(f"An error occurred: {e}")
        st.error("An unexpected error occurred. Please try again later.")
        st.stop()
      