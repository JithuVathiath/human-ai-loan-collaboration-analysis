# Human–AI Loan Collaboration Analysis

This repository contains a public, code-only version of the research notebook. Raw research files, participant-level outputs, local paths, execution metadata and personal coder names are not included.

## Notebook

Open human_ai_loan_collaboration_analysis_public.ipynb in JupyterLab or another Jupyter-compatible environment.
The notebook searches recursively from its working directory for the authorised pseudonymised source files. Those files must be obtained through the applicable research-data access process and placed in a local data/ directory. They must not be committed to the repository.

## Independent double-coding

The primary researcher coded all 210 survey/free-text responses using a 23-code framework. A second human coder independently coded a 52-response sample (24.8%) using the same codebook.

Agreement was calculated from the two independent coding sets before consensus:

- 1,196 binary coding decisions;
- six differences;
- 99.50% overall raw agreement;
- Cohen’s kappa from 0.857 to 1.000 for the 11 codes with category variation;
- undefined kappa for 12 codes unused by both coders.

The six differences were subsequently resolved through consensus. These reliability results underpin the six original qualitative themes. They do not apply to the separate deterministic rule-based twelve-theme transcript classification in Part 11.

## Environment

Python 3.11 or later is recommended.

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    jupyter lab

## Public-release safeguards

- Keep source data and generated outputs outside version control.
- The public notebook is provided without saved outputs.
- Do not publish transcript filenames, timestamps, participant-level tables or unapproved quotations.
- Preserve the distinction between the independently double-coded 23-code analysis and the separate Part 11 rule-based classification.

