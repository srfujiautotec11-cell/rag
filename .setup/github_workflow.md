# The Professional GitHub Workflow: A Step-by-Step Guide

Following a professional workflow not only makes your project history cleaner but also makes it much easier for others (and your future self!) to understand your changes.

The core principle is this: **Never commit directly to your `main` branch.** Instead, you do your work on a separate "feature" branch and then propose to merge it in. This process is managed through a **Pull Request (PR)**, which is the heart of collaboration on GitHub.

---

### Step 1: Create a New Branch for Your Changes

**Why?** Your `main` branch should always be stable and deployable. By creating a separate branch, you create an isolated environment for your work. If you make a mistake, it doesn't affect the main codebase.

**How:** Open your terminal in the project directory and run this command:

```sh
git checkout -b docs/update-readme
```

*   `git checkout -b` is a shortcut that creates a new branch and immediately switches to it.
*   `docs/update-readme` is a descriptive branch name. Using prefixes like `docs/`, `feat/`, or `fix/` is a great habit to organize your branches.

---

### Step 2: Make Your Edits

This is the easy part! Go ahead and make all the desired changes to your files. Save them when you're done.

---

### Step 3: Stage and Commit Your Changes

**Why?** A commit is a snapshot of your work at a specific point in time. It's crucial to write a clear commit message that explains *what* you did and *why*. This creates a readable history of your project.

**How:**
1.  **Stage the file(s):** This tells Git exactly which changes you want to include in the next commit.

    ```sh
    git add README.md .setup/new_guide.md
    ```

2.  **Commit the changes:** Now, save that snapshot with a descriptive message using the **Conventional Commits** format.

    ```sh
    git commit -m "docs: Update README and add new setup guides"
    ```

---

### Step 4: Push Your Branch to GitHub

**Why?** Right now, your new branch and commit only exist on your local machine. Pushing sends them up to your remote repository on GitHub.

**How:**
```sh
git push -u origin docs/update-readme
```
*   The `-u` flag sets the "upstream" branch, so next time you can just run `git push`.

---

### Step 5: Open a Pull Request (PR)

**Why?** A Pull Request is a formal proposal to merge your changes into the `main` branch. It's where discussion and review happen.

**How:**
1.  Go to your repository on GitHub.com.
2.  You will see a yellow banner with your new branch name and a green button that says **"Compare & pull request"**. Click it!
3.  Write a clear title and a helpful description of your changes, then click **"Create pull request"**.

---

### Step 6: Review and Merge Your Pull Request

**Why?** Even when working alone, reviewing your own PR is a powerful final check to catch typos or formatting errors.

**How:** On the Pull Request page, click the **"Files changed"** tab to review your work. If it all looks good, go back to the **"Conversation"** tab and click the green **"Merge pull request"** button.

---

### Step 7: Clean Up

**Why?** Once a feature branch is merged, it has served its purpose. Deleting it keeps your repository tidy.

**How:**
1.  **On GitHub:** After merging, click the **"Delete branch"** button.
2.  **On your local machine:** Switch back to your main branch, pull the latest changes, and then delete your local copy of the feature branch.
    ```sh
    git checkout main
    git pull origin main
    git branch -d docs/update-readme
    ```

You've just followed the exact workflow that professional software engineers use every day. It might seem like a lot of steps at first, but it quickly becomes second nature.