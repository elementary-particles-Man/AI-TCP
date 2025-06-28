import pytest
import os

def pytest_addoption(parser):
    parser.addoption(
        "--files-to-check", action="store", default="", help="Semicolon-separated list of files to check."
    )

@pytest.fixture(scope="session")
def files_to_check(request):
    files_str = request.config.getoption("--files-to-check")
    if not files_str:
        return []

    raw_paths = [f.strip() for f in files_str.split(";") if f.strip()]
    if not raw_paths:
        return []

    absolute_paths = []
    for p in raw_paths:
        try:
            abs_path = os.path.abspath(p)
            absolute_paths.append(abs_path)
        except Exception as e:
            pytest.fail(f"Error processing path '{p}': {e}")

    return absolute_paths
