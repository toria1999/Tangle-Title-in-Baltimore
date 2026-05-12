# Tangled Titles Synthesis Platform

This is a Streamlit MVP for synthesizing qualitative interviews, power mapping,
quantitative spatial patterns, and intervention entry points related to tangled
titles in Baltimore.

## Run Locally

```bash
cd "/Users/torialiu/Downloads/Tangle-Title-in-Baltimore"
streamlit run streamlit_app.py
```

`Instruction.py` is the app's main page. `streamlit_app.py` is a thin wrapper
for Streamlit Cloud and other hosts so the deployment does not accidentally use
one of the files inside `pages/` as the entry point.

### On Windows

From the repository root, run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Replace Placeholder Data

The site is driven by CSV files in `data/`:

- `nodes.csv`: power map nodes
- `edges.csv`: power map relationships
- `themes.csv`: interview themes linked to node IDs
- `tract_data.csv`: quantitative tract-level placeholder data
- `synthesis_matrix.csv`: integrated evidence matrix

Keep the column names the same when replacing placeholder rows with real project
outputs.
