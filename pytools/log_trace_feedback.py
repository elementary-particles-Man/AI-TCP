import argparse
from pathlib import Path
import yaml


def _find_reasoning_traces(obj):
    traces = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "reasoning_trace" and isinstance(v, list):
                traces.append(v)
            else:
                traces.extend(_find_reasoning_traces(v))
    elif isinstance(obj, list):
        for item in obj:
            traces.extend(_find_reasoning_traces(item))
    return traces


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract reasoning_trace logs")
    parser.add_argument("yaml_file", type=Path, help="AI-TCP YAML file")
    args = parser.parse_args()

    try:
        with open(args.yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as exc:
        print(f"❌ Failed to load {args.yaml_file}: {exc}")
        return

    traces = _find_reasoning_traces(data)
    if not traces:
        print(f"❌ No reasoning_trace found in {args.yaml_file}")
        return

    output_dir = Path("logs")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"trace_{args.yaml_file.stem}.md"

    lines = [f"# {args.yaml_file.name}"]
    for idx, trace in enumerate(traces, 1):
        if len(traces) > 1:
            lines.append(f"\n## reasoning_trace {idx}")
        for i, step in enumerate(trace, 1):
            if isinstance(step, dict):
                inp = str(step.get("input", "")).replace("\n", " ")
                out = str(step.get("output", "")).replace("\n", " ")
                lines.append(f"{i}. [{inp}] → [{out}]")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Wrote {output_path}")


if __name__ == "__main__":
    main()
