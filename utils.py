# --- utils.py ---

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

def load_json_safely(path: Path) -> dict:
    """
    JSONファイルを安全にロードする。
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_log(result: dict, output_path: Path) -> None:
    """
    処理結果を output.json に書き出す。
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"✅ Log written to {output_path}")

def archive_task(input_path: Path, archive_dir: Path) -> None:
    """
    処理済みタスクをアーカイブに移動する。
    アーカイブファイル名はタイムスタンプで一意化。
    """
    archive_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = f"{timestamp}_archived_task.json"
    shutil.move(str(input_path), str(archive_dir / archive_name))
    print(f"✅ Task archived to {archive_dir / archive_name}")
