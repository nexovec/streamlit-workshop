import streamlit as st
from typing import Callable

class Routing_Context:
    SESSION_KEY_PATH = "routing_path"
    def __init__(self, default=None) -> None:
        routing_key = Routing_Context.SESSION_KEY_PATH
        if st.session_state.get(routing_key) is None:
            st.session_state[routing_key] = default

    def redirect(self, path: str):
        st.session_state[Routing_Context.SESSION_KEY_PATH] = path
        st.experimental_rerun()

    def route(self, *path:str):
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                # print("the decorator did actually run")
                if st.session_state.get(Routing_Context.SESSION_KEY_PATH) in path:
                    # print("an actual thing is being shown")
                    return func(*args, **kwargs)            
                return lambda:None
            return wrapper
        return decorator
 