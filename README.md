# AI Product Ops Take-Home Assignment

This repository contains the completed take-home assignment for the AI Product Ops role.

## What is included
- `research_agent.py` — builds the research dataset for the 100 apps and renders the case study page.
- `site/index.html` — the final self-explanatory HTML case study.
- `site/research_results.json` — the structured dataset behind the report.
- `render.yaml.template` — optional Render manifest template for deployment.

## What this project shows
- A compact 100-app research matrix for auth, self-serve gating, API surface, and buildability.
- A verified sample checklist that documents accuracy checks.
- A reusable research agent script that generates the page from the dataset.

## How it works
1. `research_agent.py` contains the app dataset and report generation logic.
2. Running the script builds the output into the `site` folder.
3. `site/index.html` is the reviewer-facing case study with findings, patterns, and evidence links.

## Run locally
```bash
python research_agent.py
```

Then open `site/index.html` in a browser.

## Notes
- The generated site is self-contained and meant to be submitted as the review deliverable.
- The code is designed to be easy to run and inspect without additional setup.
