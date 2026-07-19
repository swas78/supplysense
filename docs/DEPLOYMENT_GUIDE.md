# 🚀 Complete Deployment Guide for SupplySense

Because SupplySense uses a modern, decoupled architecture (FastAPI backend + Next.js frontend), the deployment process is split into three parts: Database, Backend, and Frontend. 

We highly recommend the following stack for the easiest and fastest free deployment for hackathons:
* **Database:** Supabase (Free PostgreSQL)
* **Backend:** Render.com (Free Python Hosting)
* **Frontend:** Vercel (Free Next.js Hosting)

Follow these exact steps in order.

---

## 🟢 Step 1: Deploy the Database (Supabase)

Your app currently uses a local `sqlite` database. For production, you need a database that lives in the cloud.

1. Go to [Supabase](https://supabase.com/) and create a free account.
2. Click **New Project** and create an organization.
3. Give your project a name (e.g., `supplysense-db`) and a secure password. **Save this password somewhere safe!**
4. Wait for the database to provision (takes about 1-2 minutes).
5. Go to **Settings (gear icon)** > **Database**.
6. Scroll down to **Connection string** and select **URI**.
7. Copy the connection string. It will look like this:
   `postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres`
8. In your project codebase, open `backend/database.py` and temporarily change the `SQLALCHEMY_DATABASE_URL` to your new connection string.
9. **Seed the Production Database:** Run your local start script one last time `bash run.sh`. This will connect to Supabase, create all the tables in the cloud, and push your mock hackathon data to it! 
10. Once seeded, change the `database.py` string back to using an environment variable for security: 
    ```python
    import os
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
    ```
11. Commit and push this change to GitHub.

---

## 🔵 Step 2: Deploy the AI Backend (Render)

Render makes it incredibly easy to host Python FastAPI servers directly from GitHub.

1. Go to [Render.com](https://render.com/) and sign up with GitHub.
2. Click **New +** and select **Web Service**.
3. Select **"Build and deploy from a Git repository"** and connect your `supplysense` GitHub repository.
4. Fill out the configuration exactly like this:
   * **Name:** `supplysense-api`
   * **Root Directory:** `backend` *(Crucial: This tells Render to look in the backend folder)*
   * **Environment:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Scroll down to **Advanced** and click **Add Environment Variable**. Add the following:
   * `GEMINI_API_KEY`: Paste your Google AI key here.
   * `DATABASE_URL`: Paste the Supabase connection string from Step 1.
6. Click **Create Web Service**.
7. Render will take about 2-3 minutes to build and deploy. Once it says "Live", copy the URL at the top left of the screen (e.g., `https://supplysense-api.onrender.com`).

---

## 🟣 Step 3: Deploy the Frontend (Vercel)

Vercel is the creator of Next.js and provides the absolute best hosting for it.

1. Open your project code and navigate to `frontend/src/lib/api.ts`.
2. Change the `API_BASE` variable from `http://localhost:8000/api` to the Render URL you just got in Step 2.
   * *Example:* `const API_BASE = 'https://supplysense-api.onrender.com/api';`
3. Commit this change and push it to GitHub (`git add .`, `git commit -m "update api url"`, `git push`).
4. Go to [Vercel.com](https://vercel.com/) and sign in with GitHub.
5. Click **Add New...** > **Project**.
6. Import your `supplysense` GitHub repository.
7. Vercel will automatically detect the folder structure. 
   * **Important:** Under **Framework Preset**, ensure it says `Next.js`. 
   * **Important:** Under **Root Directory**, click edit and select the `frontend` folder.
8. Click **Deploy**.
9. Vercel will build the frontend and give you a live `.vercel.app` URL.

---

## 🎯 Verification

1. Click on your live Vercel URL.
2. The dashboard should load data from your Supabase database via the Render backend.
3. Open the AI Chat Assistant and ask a question to verify that the Gemini API keys are working correctly on Render.

**You are now fully live and ready to submit to the hackathon!**
