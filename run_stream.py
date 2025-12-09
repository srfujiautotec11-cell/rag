import sys
from streamlit.web import cli as stcli

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
    sys.exit(stcli.main())