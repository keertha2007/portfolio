# Keerthana JM — Portfolio Website

A personal portfolio website with a **Python Flask** backend that stores contact form messages in a **Neon (PostgreSQL)** database, deployed on **Render**.

---

## 📁 Project Structure

```
portfolio/
├── index.html          ← Your frontend (already done!)
├── app.py              ← Flask backend
├── requirements.txt    ← Python dependencies
├── .env                ← Your secret DB URL (never push this!)
├── .env.example        ← Template for .env
├── .gitignore          ← Files git should ignore
└── README.md           ← This file
```

---

## 🛠️ Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | HTML, Tailwind CSS, JavaScript      |
| Backend   | Python + Flask                      |
| Database  | Neon (PostgreSQL)                   |
| Hosting   | Render                              |

---

## ⚙️ Local Setup (Run on Your Computer)

### Step 1 — Clone your repo
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up your `.env` file
```bash
cp .env.example .env
```
Open `.env` and paste your **Neon connection string** (see below).

### Step 5 — Run the app
```bash
python app.py
```
Open your browser and go to **http://localhost:5000**

---

## 🐘 Setting Up Neon (Free Database)

1. Go to [https://neon.tech](https://neon.tech) and sign up for free
2. Click **"New Project"** → give it a name like `portfolio`
3. Once created, go to **"Connection Details"**
4. Copy the **Connection string** — it looks like:
   ```
   postgresql://user:password@ep-something.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
5. Paste it as `DATABASE_URL` in your `.env` file

> The table (`messages`) is created automatically when the app starts for the first time.

---

## 🚀 Deploy on Render (Free Hosting)

### Step 1 — Push your code to GitHub
```bash
git add .
git commit -m "Add Flask backend"
git push origin main
```

### Step 2 — Create a new Web Service on Render
1. Go to [https://render.com](https://render.com) and sign up / log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select your repo
4. Fill in the settings:

| Setting         | Value                          |
|-----------------|--------------------------------|
| Environment     | Python 3                       |
| Build Command   | `pip install -r requirements.txt` |
| Start Command   | `gunicorn app:app`             |

### Step 3 — Add Environment Variable on Render
1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Key: `DATABASE_URL`
4. Value: your Neon connection string (same one from your `.env` file)
5. Click **"Create Web Service"**

Render will build and deploy your site. In a few minutes you'll get a live URL like:
`https://your-portfolio.onrender.com` 🎉

---

## 📬 How the Contact Form Works

1. Visitor fills out the form and clicks **Send Message**
2. JavaScript sends the data to `POST /contact` on your Flask server
3. Flask validates the data and saves it to the `messages` table in Neon
4. A success or error message is shown to the visitor

To view submitted messages, you can use the **Neon Console** → Tables → `messages`.

---

## 🔒 Important Security Notes

- **Never commit your `.env` file** — it's in `.gitignore` for this reason
- Always add `DATABASE_URL` as an environment variable on Render, not in your code
- The `.env.example` file is safe to commit — it has no real credentials

---

## 👩‍💻 Author

**Keerthana JM**  
BCA Undergraduate Student  
[GitHub](https://github.com/keertha2007) · [LinkedIn](https://www.linkedin.com/in/keerthana-jm-271616384)
