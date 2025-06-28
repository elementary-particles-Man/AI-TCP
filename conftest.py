def pytest_addoption(parser):
    parser.addoption(
        "--files-to-check", action="store", default="", help="Comma-separated list of files to check"
    )