if not __name__ == "__main__":
    raise Exception("This file is not meant to be imported.")

import subprocess

subprocess.run(["streamlit", "run", "webui.py", "--browser.gatherUsageStats", "false", "--server.enableCORS", "false", "--server.port", "5000"])
