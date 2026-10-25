# Panel Ready

Panel Ready is a small interview practice project. It has a web app for
practicing a full interview and a separate command-line exercise where three
AI interviewers review one answer.

## The three-person panel

The panel is in `panel.py`. It reviews the same interview question and answer
from three points of view:

1. **Technical lead** — looks at technical understanding, gaps, and a useful
   follow-up question.
2. **HR interviewer** — looks at communication, structure, ownership, and
   self-awareness.
3. **Hiring manager** — considers both reviews, gives a hiring verdict, and
   picks a practice priority.

The reviewers run in sequence. Their feedback is saved to
`panel_feedback.md`; the hiring manager's practice priority is kept in a local
SQLite database and can inform later runs.

## The web app

The web app is a separate part of the project. A candidate can save a resume,
add a job description, and practice a mock interview with typed or spoken
answers. It prepares questions across different interview topics, gives
feedback on answers, and saves topics to review. Groq generates the questions
and coaching; public search provides optional company and role context.

The three-person panel described above is **not part of the web interview
flow**. It is the separate `panel.py` command-line exercise.

## Run locally

Use Python 3.13 and a Groq API key. Install the packages and create a local
`.env` file:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your key to `.env` as `GROQ_API_KEY=your_key`. Do not share or commit
`.env`.

To start the web app:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>.

To run the three-person panel, create `question.txt` and `answer.txt` in the
project folder with the interview question and your answer, then run:

```powershell
.\.venv\Scripts\python.exe panel.py
```

The question, answer, generated feedback, and panel memory are local files and
are excluded from Git.

## Deployment

`render.yaml` configures the web app for Render. The web app needs a Groq API
key set as the `GROQ_API_KEY` environment secret and persistent storage for
its SQLite database. The command-line panel is not started by the Render
service.

## Notes

The web app stores profiles and interview history in SQLite. Resume/profile
details, job information, and answers are sent to Groq for coaching; search
queries are sent to DuckDuckGo. Avoid using confidential personal information.
The hosted app is a project demo, not a service for sensitive data.
