# Guide: Configuring Your Language Model (LLM)

This guide will walk you through switching from the default cloud-based Google Gemini to a private, local LLM running on your own machine using Ollama.

## The Goal

**What are we doing?**

We are re-routing the "brain" of the application from Google's servers to a model running directly on your computer.

**Why do this?**

*   **Privacy:** Your data and queries never leave your local machine.
*   **Cost:** No API fees.
*   **Offline Access:** Works without an internet connection once set up.
*   **Flexibility:** Easily swap between dozens of powerful open-source models.

**When should I do this?**

Do this after you have the application running with the default settings and you're ready to take the next step towards a fully local, private setup.

**Where will the changes be made?**

We will make small, targeted changes in three files:
1.  `pyproject.toml` (to add the Ollama library)
2.  `config.py` (to add settings for the local LLM)
3.  `services/generator.py` (to tell the app *how* to talk to the local LLM)

---

## How-To Guide: Switching to a Local LLM

### Step 1: Install Ollama

Ollama is a fantastic tool that manages downloading, running, and serving local LLMs.

*   **How:** Go to https://ollama.com and download the installer for your operating system (macOS, Windows, or Linux). Run the installer.
*   **Verify:** Open your terminal or command prompt and run `ollama --version`. If it prints a version number, you're all set!

### Step 2: Download a Local Model

Now, let's download a model for Ollama to serve. `llama3` is a great starting point.

*   **How:** In your terminal, run the following command. This will download the model, which may take a few minutes.
    ```sh
    ollama pull llama3
    ```
*   Ollama will now be running in the background, ready to serve this model.

### Step 3: Update Project Dependencies

We need to add the `langchain-community` library, which knows how to communicate with Ollama.

*   **How:** Open `pyproject.toml` and add `"langchain-community>=0.2.10"` to the `dependencies` list.

    ```diff
    --- a/pyproject.toml
    +++ b/pyproject.toml
    @@ -5,6 +5,7 @@
     requires-python = ">=3.11"
     dependencies = [
         "google-generativeai>=0.8.5",
    +    "langchain-community>=0.2.10",
         "langchain-text-splitters>=1.0.0",
         "pgvector>=0.4.1",
         "psycopg[binary]>=3.2.12",
    ```

*   **Install:** Open the terminal in PyCharm (or your code editor) and run `uv pip sync` to install the new package.

### Step 4: Update the Configuration

Let's add settings to `config.py` so you can easily switch between the cloud and local models.

*   **How:** Open `C:/rag/config.py` and add the new settings. We'll add a `USE_LOCAL_LLM` flag to control which model is active.

    ```diff
    --- a/config.py
    +++ b/config.py
    @@ -8,11 +8,18 @@
         GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
         DATABASE_URL: str = os.getenv("DATABASE_URL", "")
         
    +    # --- LLM Configuration ---
    +    # Set to True to use a local LLM with Ollama, False to use Gemini API
    +    USE_LOCAL_LLM: bool = False 
    +
         EMBEDDING_MODEL: str = "models/text-embedding-004"
         GENERATION_MODEL: str = "gemini-2.5-flash"
    +
    +    # Local LLM settings (only used if USE_LOCAL_LLM is True)
    +    OLLAMA_BASE_URL: str = "http://localhost:11434"
    +    LOCAL_GENERATION_MODEL: str = "llama3" # The model you pulled with Ollama
         
         ALLOWED_FILE_TYPES = ['pdf', 'txt', 'md', 'docx', 'doc']
         CHUNK_SIZE: int = 800
    ```

    *To activate your local model, you would simply change `USE_LOCAL_LLM: bool = False` to `True`.*

### Step 5: Update the Generator Service

Finally, let's teach `services/generator.py` how to use these new settings.

*   **How:** Open `C:/rag/services/generator.py` and modify it to choose the LLM based on the `USE_LOCAL_LLM` flag.

    ```diff
    --- a/services/generator.py
    +++ b/services/generator.py
    @@ -1,11 +1,18 @@
    -from langchain_google_genai import ChatGoogleGenerativeAI
    +import google.generativeai as genai
    +from langchain_community.chat_models import ChatOllama
     from langchain.prompts import PromptTemplate
     from langchain.schema.runnable import RunnablePassthrough
     from langchain.schema.output_parser import StrOutputParser
     from config import config
     
     class GeneratorService:
         def __init__(self):
    -        self.model = ChatGoogleGenerativeAI(model=config.GENERATION_MODEL, temperature=0.3)
    +        if config.USE_LOCAL_LLM:
    +            self.model = ChatOllama(
    +                base_url=config.OLLAMA_BASE_URL,
    +                model=config.LOCAL_GENERATION_MODEL,
    +                temperature=0.3
    +            )
    +        else:
    +            if config.GEMINI_API_KEY:
    +                genai.configure(api_key=config.GEMINI_API_KEY)
    +            self.model = genai.GenerativeModel(config.GENERATION_MODEL)
    ```

You're done! Now, by simply changing the `USE_LOCAL_LLM` flag in `config.py`, you can switch between Google's API and your own private, local LLM.

### Troubleshooting Prompts for Your AI Assistant

If you run into trouble, copy and paste the following into our chat.

> **For Connection Issues:**
> "I've set up my RAG application to use a local LLM with Ollama, but I'm getting a connection error. I've confirmed Ollama is running. My `config.py` has `OLLAMA_BASE_URL: str = "http://localhost:11434"`. Can you help me diagnose why my Streamlit app can't connect to the Ollama server?"

> **For Model Not Found Errors:**
> "My RAG app is giving me an error saying it can't find the local model. I'm trying to use `llama3`. I've set `LOCAL_GENERATION_MODEL: str = "llama3"` in my `config.py`. How can I verify that Ollama has downloaded this model and is serving it correctly?"