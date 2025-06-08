import importlib.util
from pathlib import Path

# Load the module with spaces in the filename
module_path = Path(__file__).resolve().parents[1] / 'Short Distance Travel.py'
spec = importlib.util.spec_from_file_location('sdt', module_path)
sdt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sdt)

def test_generate_map(tmp_path):
    output = tmp_path / 'Travel Map.html'
    sdt.generate_map(str(output))
    assert output.exists()
    assert output.stat().st_size > 0
