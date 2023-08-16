import streamlit as st
from typing import Callable

class Routing_Context:
    SESSION_KEY_PATH = "routing_path"
    def __init__(self) -> None:
        pass
    def route(self, *path:str):
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                print("the decorator did actually run")
                if st.session_state.get(Routing_Context.SESSION_KEY_PATH) in path:
                    print("an actual thing is being shown")
                    return func(*args, **kwargs)            
                return lambda:None
            return wrapper
        return decorator
 