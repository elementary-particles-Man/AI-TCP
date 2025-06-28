import pytest
import os

def pytest_addoption(parser):
    parser.addoption(
        "--files-to-check", action="store", default="", help="Semicolon-separated list of files to check."
    )

@pytest.fixture(scope="session")
def files_to_check(request):
    files = request.config.getoption("--files-to-check")
    return [os.path.abspath(f.strip()) for f in files.split(";") if f.strip()]
