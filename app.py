"""Compatibility entry point for local Streamlit runs.

The deployed app uses streamlit_app.py. This file keeps `streamlit run app.py`
working without changing the existing app structure.
"""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).with_name("streamlit_app.py")), run_name="__main__")
