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
    project_root = os.getcwd() # Assuming pytest is run from the project root
    for p in raw_paths:
        try:
            # Construct absolute path relative to project root
            abs_path = os.path.join(project_root, p)
            if not os.path.exists(abs_path):
                pytest.fail(f"Error: File not found at '{abs_path}'")
            absolute_paths.append(abs_path)
        except Exception as e:
            pytest.fail(f"Error processing path '{p}': {e}")

    return absolute_paths
