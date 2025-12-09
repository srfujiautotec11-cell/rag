import subprocess
import os

def main():
    """The main entrypoint for the application."""
    # The command to run the Streamlit app
    command = ["streamlit", "run", "app.py", "--server.port", "5000", "--server.address", "0.0.0.0"]
    subprocess.run(command)

if __name__ == "__main__":
    main()