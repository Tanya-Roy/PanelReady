# Panel Ready

Panel Ready is an interview-practice app. It uses a candidate's resume and a
job description to run a mock interview, give feedback, and keep a record of
topics to revisit.

## What it does

- Saves a profile, resume text, and interview history in SQLite.
- Lets a candidate search for a role or add one manually.
- Runs a voice-enabled or typed mock interview.
- Uses Groq to generate questions and feedback, and public web search for
  optional company and role context.

## Run it on your computer

You need Python 3.13 and a Groq API key. To publish the project, you also
need Git for Windows and GitHub and Render accounts. The key is used by the
app on the server and must not be committed to GitHub.

In PowerShell, from the project folder:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env`, replace `paste_your_key_here` with your Groq API key, and save.
Then start the app:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Visit <http://127.0.0.1:8000>. For local use, leave `COOKIE_SECURE=false`.

## Publish the source on GitHub

The repository is intended to be public. Before publishing, check that `.env`,
SQLite files, uploaded files, and your personal notes remain untracked. The
included `.gitignore` excludes these local files. Do not add API keys,
resumes, interview answers, or other personal information to the repository.
No license is included; public visibility alone does not grant permission to
reuse the code.

Create an empty public repository on GitHub (do not add a README, license, or
`.gitignore` there). In a terminal opened at this project folder, run:

```powershell
git init
git add .
git status --short
```

Review the staged file list. It should not contain `.env`, `.venv`, a database,
uploads, or personal notes. If it does, stop and fix the ignore rules before
continuing. Then replace `<your-github-repository-url>` with the URL GitHub
shows for your new repository:

```powershell
git commit -m "Prepare interview practice app"
git branch -M main
git remote add origin <your-github-repository-url>
git push -u origin main
```

GitHub stores the source code; Render runs the web app.

## Deploy on Render

The included `render.yaml` defines a Render web service, a persistent disk
for the SQLite database, HTTPS-only session cookies, and a health check.
Deploy it as a **Blueprint** connected to the GitHub repository:

1. Push the project to GitHub.
2. In Render, choose **New > Blueprint**, connect the repository, and apply
   the Blueprint.
3. When prompted, enter `GROQ_API_KEY` as a secret. Keep
   `GROQ_MODEL=groq/openai/gpt-oss-20b`, `DATABASE_PATH`, and
   `COOKIE_SECURE` as defined in `render.yaml`.
4. Wait for the service to finish building, then open its `onrender.com`
   URL. The `/healthz` endpoint should return `{"status":"ok"}`.

The Blueprint uses a paid Render web service because SQLite needs persistent
storage. Keep the service at one worker while it uses SQLite, and do not
remove or replace its persistent disk: that disk contains user accounts and
interview data.

## Before sharing the hosted app

This is a small project, not a hardened service for sensitive or regulated
information. Anyone who can reach the URL can create an account. There is no
email verification, password reset, or self-service account deletion, and
the app does not encrypt the SQLite data itself. Render encrypts its disks at
rest, but that does not replace application-level protections. Do not use
confidential resumes or other sensitive information.

The app sends resume/profile details, job information, and interview answers
to Groq to generate interview questions and feedback. Search queries are sent
to DuckDuckGo. Review those providers' terms and privacy policies before
using the service.

The Render disk persists between deploys. Render also creates daily disk
snapshots and retains them for seven days, but arrange separate backups before
relying on the service for important records. For a public service used by
people beyond a small, trusted test group, add account recovery and deletion,
abuse protection, data-retention controls, and a database and backup plan
appropriate to its users.

## Project files

- `app.py` — FastAPI application and SQLite-backed API.
- `interview_tracker.html` — browser interface.
- `render.yaml` — Render deployment configuration.
- `requirements.txt` — Python dependencies.
