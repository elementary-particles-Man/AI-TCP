import os
import pytest

# フックで CLI オプションを追加
def pytest_addoption(parser):
    parser.addoption(
        "--files-to-check",
        action="store",
        default="",
        help="Semicolon-separated list of file paths to check."
    )

# フックで fixture に渡す
@pytest.fixture(scope="session")
def files_to_check(request):
    files = request.config.getoption("--files-to-check")
    return [f.strip() for f in files.split(";") if f.strip()]

# ファイル存在チェックテスト
def test_files_exist(files_to_check):
    output_path = r"X:\work\TaskValidation.txt"
    with open(output_path, "a", encoding="utf-8") as f:
        for path in files_to_check:
            if os.path.exists(path):
                f.write(f"[✅] {path} exists.\n")
            else:
                f.write(f"[❌] {path} NOT found.\n")

# セッション終了時に完了ログ
def pytest_sessionfinish(session, exitstatus):
    output_path = r"X:\work\TaskValidation.txt"
    with open(output_path, "a", encoding="utf-8") as f:
        f.write("=== Validation Complete ===\n")
