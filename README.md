# Tangled Titles Synthesis Platform

This is a Streamlit MVP for synthesizing qualitative interviews, power mapping,
quantitative spatial patterns, and intervention entry points related to tangled
titles in Baltimore.

## Run Locally

```bash
cd "/Users/torialiu/Documents/New project/tangled-title-site"
.venv/bin/streamlit run Instruction.py
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
