from types import NoneType
import streamlit as st
from typing import Callable

class Routing_Context:
    SESSION_KEY_PATH = "routing_path"
    views = {}
    def __init__(self, default=None) -> None:
        routing_key = Routing_Context.SESSION_KEY_PATH
        if st.session_state.get(routing_key) is None:
            st.session_state[routing_key] = default
        # Routing_Context.views = Routing_Context.views or {}

    def redirect(self, path: str):
        st.session_state[Routing_Context.SESSION_KEY_PATH] = path
        st.experimental_rerun()

    def route(self, *paths:str):
        assert len(paths) != 0
        # print(f"route paths: {paths}", flush=True)
        def decorator(func: Callable):
            # print("runs 2", flush=True)
            def wrapper(*args, **kwargs):
                # print("the decorator did actually run", flush=True)
                if st.session_state.get(Routing_Context.SESSION_KEY_PATH) in paths:
                    # print("an actual thing is being shown")
                    return func(*args, **kwargs)            
                return lambda:None
            for path in paths:
                # print("I be running", flush=True)
                assert isinstance(path, str)
                Routing_Context.views[path] = wrapper
            return wrapper
        return decorator
    def render(self):
        for key, view in Routing_Context.views.items():
            # print(f"rendering {key}:\t{view}")
            view()
 