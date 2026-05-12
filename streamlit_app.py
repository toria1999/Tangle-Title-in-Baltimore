"""Standard Streamlit Cloud entry point.

Run this file, or Instruction.py, from the repository root. Keeping this thin
wrapper avoids deployments accidentally using a page file such as Quant Map as
the app entry point.
"""

from pathlib import Path
import runpy


runpy.run_path(str(Path(__file__).with_name("Instruction.py")), run_name="__main__")
