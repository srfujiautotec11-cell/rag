# Guide: Setting Up Your SQL Database (from scratch)

Your application needs a PostgreSQL database to store information about your documents. The `docker-compose.yml` file in this project makes this incredibly easy, even if you've never used SQL or Docker before.

## The Goal

**What are we doing?**

We are using Docker to create and run a PostgreSQL database inside a "container" on your machine. This keeps the setup clean, isolated, and easy to manage.

**Why do this?**

*   **Simplicity:** You don't need to manually install and configure PostgreSQL. Docker handles it with two simple commands.
*   **Consistency:** It ensures the database runs the same way on any computer.
*   **Cleanliness:** All database files are kept in one place and can be easily removed without affecting your system.

**When should I do this?**

This is a one-time setup. You need to do this before you can upload your first document.

**Where will the changes be made?**

You will create one new file, `.env`, to hold your database credentials, and then you'll run commands in your terminal.

---

## How-To Guide: Setting up the Database

### Step 1: Install Docker Desktop

Docker is a tool that runs applications in isolated environments called containers.

*   **How:** Go to https://www.docker.com/products/docker-desktop/ and download the installer for your operating system. Run the installer.
*   **Verify:** After installation, open Docker Desktop. Once it shows a green light and says "Docker Desktop is running," you're ready.

### Step 2: Create a `.env` File for Credentials

Your `docker-compose.yml` is smartly configured to read database credentials from environment variables. Let's create a file to store them.

*   **How:** In the root directory of your project (the same folder as `app.py`), create a new file named `.env`. **Important:** The file must be named exactly `.env` with no other extension.
*   Add the following content to it. You can use these credentials or choose your own.

    ```
    # Database Credentials
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=rag_db
    
    # This is the full connection string the app will use
    DATABASE_URL=postgresql://user:password@localhost:5432/rag_db
    
    # Your Gemini API Key (if not using a local LLM)
    GEMINI_API_KEY=your_api_key_here
    ```

*   Your `.gitignore` file is already set up to ignore this file, so your secrets are safe!

### Step 3: Start the Database with Docker

Now for the magic. We'll use Docker Compose to read your `docker-compose.yml` file and start the database.

*   **How:** Open a terminal in your project's root directory and run:
    ```sh
    docker-compose up -d
    ```
    *   `up` tells Docker to start the services defined in the file.
    *   `-d` tells it to run in "detached" mode (in the background).

*   **Verify:** You should see output indicating that the `rag-postgres-db` container was created and started. You can also open Docker Desktop to see the container running.

Your database is now running and ready! Your application will automatically connect to it using the `DATABASE_URL` from your `.env` file.

### Troubleshooting Prompts for Your AI Assistant

> **For Docker Not Found Errors:**
> "I'm trying to run `docker-compose up -d` to start my PostgreSQL database, but I'm getting an error like 'command not found: docker-compose'. I have installed Docker Desktop. What could be wrong?"

> **For Database Connection Errors in the App:**
> "I have my Docker container for PostgreSQL running, but my Streamlit app gives an error saying it can't connect to the database. I've created a `.env` file with `DATABASE_URL=postgresql://user:password@localhost:5432/rag_db`. Can you help me figure out what to check?"

> **For "Authentication Failed" Errors:**
> "My app is trying to connect to the Docker PostgreSQL database, but I'm seeing an 'authentication failed' error. I've checked my `.env` file and the `POSTGRES_USER` and `POSTGRES_PASSWORD` seem to match the `DATABASE_URL`. What else could cause this?"