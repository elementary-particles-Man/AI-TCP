from types import SimpleNamespace

from pytools import format_task_validation as ft


def test_format_task_validation(tmp_path, monkeypatch):
    log_file = tmp_path / "TaskValidation.txt"
    log_file.write_text("sample log", encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    dummy_now = SimpleNamespace()
    dummy_now.strftime = lambda fmt: "20240102_030405"
    monkeypatch.setattr(ft, "datetime", SimpleNamespace(now=lambda: dummy_now))

    ft.main([str(log_file)])

    out_path = tmp_path / "cli_archives" / "TaskValidation_20240102_030405.md"
    assert out_path.exists()
    expected = (
        "# Task Validation Log\n\n```\nsample log\n```\n\n[Task Completed]\n"
    )
    assert out_path.read_text(encoding="utf-8") == expected
