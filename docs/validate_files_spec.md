
# CLI Specification: `validate_files` Task

This document outlines the command-line interface (CLI) specification for the `validate_files` task, which is executed by the AI-TCP agent via the `task_bridge_runner.py`.

## Overview

The `validate_files` task is designed to perform two primary functions:
1.  **File Existence and Integrity Check**: Verify the presence of specified files and, in the future, their integrity using checksums.
2.  **Pytest Execution**: Run a designated pytest suite against the specified files to ensure code quality and functionality.

This task is triggered by the `task_bridge_runner.py` when a `validate_files` entry is found in `new_task.json`.

## `validate_task.py` Usage

The `validate_task.py` script is the core component that executes the `validate_files` task. It is **not intended for direct manual execution**.

**Location:** `scripts/auto_ops/validate_task.py`

**Execution Flow (Internal to Agent):**

1.  The `task_bridge_runner.py` detects a `validate_files` task in `new_task.json`.
2.  It sets the environment variable `AI_TCP_AGENT_CALL` to `true`.
3.  It invokes `validate_task.py` using `python scripts/auto_ops/validate_task.py`.
4.  `validate_task.py` reads its configuration (e.g., `files_to_check`, `log_path`, `pytest_target`) directly from the `new_task.json` file.
5.  It performs file existence checks and logs the results to `TaskValidation.txt`.
6.  It executes `pytest` with the `--files-to-check` argument, passing the list of files.
7.  Pytest output and exit code are logged to `TaskValidation.txt`.
8.  The script exits with `0` on success, `1` for general errors (e.g., `new_task.json` not found, task not found), and `2` if any specified files are not found or potential tampering is detected.

**Key Features:**

*   **Agent-Only Execution**: Prevents accidental manual execution.
*   **Timestamped Logging**: All log entries in `TaskValidation.txt` include a timestamp for better traceability.
*   **Standardized Pytest Exit Code Logging**: The pytest exit code is explicitly logged for consistent parsing.
*   **Checksum Verification (Future)**: Designed to incorporate file size and hash verification to detect tampering.

## `conftest.py` Fixture Structure

The `conftest.py` file in the project root defines pytest fixtures and hooks that are automatically discovered by pytest.

**Location:** `conftest.py`

**Key Components for `validate_files`:**

### `pytest_addoption(parser)` Hook

This hook adds a custom command-line option `--files-to-check` to pytest. This option is used by `validate_task.py` to pass the list of files to the pytest test suite.

```python
def pytest_addoption(parser):
    parser.addoption(
        "--files-to-check",
        action="store",
        default="",
        help="Semicolon-separated list of file paths to check."
    )
```

### `files_to_check` Fixture

This session-scoped fixture retrieves the value of the `--files-to-check` option and processes it into a list of absolute file paths. It handles argument normalization, semicolon splitting, and includes basic error handling for path processing.

```python
import pytest
import os

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
```

This fixture ensures that tests requiring knowledge of the files being validated can easily access a normalized and absolute list of paths.

## Task Execution Flow

1.  **Task Definition**: A `validate_files` task is defined in `new_task.json` with the `files_to_check` parameter.
2.  **Monitoring**: `task_bridge_runner.py` continuously monitors `new_task.json` for changes.
3.  **Task Trigger**: Upon detecting a `validate_files` task, `task_bridge_runner.py` executes `validate_task.py`.
4.  **File Validation**: `validate_task.py` performs file existence and integrity checks.
5.  **Pytest Execution**: `validate_task.py` invokes `pytest`, passing the `files_to_check` via the `--files-to-check` CLI option.
6.  **Fixture Activation**: The `files_to_check` fixture in `conftest.py` processes this option, making the list of files available to tests.
7.  **Logging**: All validation and pytest results are logged to `TaskValidation.txt`.
8.  **Report Generation**: `task_log_parser.py` parses `TaskValidation.txt` and generates a Markdown report.
9.  **Archiving**: `task_bridge_runner.py` archives the `TaskValidation.txt` and `output.json` for historical tracking.

This structured approach ensures consistent and automated validation of files within the AI-TCP project.
