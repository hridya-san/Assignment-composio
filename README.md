# AI Product Ops Take-Home Assignment

This workspace contains a small research agent that turns the 100-app assignment into a single self-explanatory HTML case study.

## What is included
- A reproducible Python script that builds the research dataset and renders the page.
- A generated HTML report at [site/index.html](site/index.html).
- A JSON export at [site/research_results.json](site/research_results.json).

## Run locally
```bash
python research_agent.py
```

Then open [site/index.html](site/index.html) in a browser or serve the folder with:

```bash
python -m http.server 8000
```

Then visit http://localhost:8000/site/index.html.

## Deployment on Render
1. Create a new Web Service in Render.
2. Connect your repository to Render.
3. Set the build command to:

```bash
python research_agent.py
```

4. Set the publish directory to:

```bash
site
```

5. Deploy the service.

## What to submit
- A live URL pointing to the deployed HTML page.
- A link to this source repository.
- This README documenting how to run the research agent locally.

## Deploying to Render (quick guide)

Option A — Manual (recommended if you control the repo):

1. Push this repository to GitHub (create a repo named e.g. `composio-case-study`).
2. In Render, create a new **Static Site** (or Web Service) and connect your GitHub repo.
3. Set the build command to:

```bash
python research_agent.py
```

4. Set the publish directory to:

```bash
site
```

5. Deploy — Render will run the build, generate `site/`, and publish the static files.

Option B — Ask me to push & deploy for you:

- If you want me to push the repo and create the Render service, I can do that if you provide a GitHub personal access token (repo scope) and permission to create a repo, and optionally a Render API key. Reply with which option you prefer and I will proceed.
