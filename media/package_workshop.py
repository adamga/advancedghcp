"""Package committed workshop files, excluding build caches and Git metadata."""

import argparse
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path, PurePosixPath


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("deliverables"))
    args = parser.parse_args()
    repo = args.repo.resolve()
    destination = args.out.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    tracked = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"],
                             check=True, capture_output=True).stdout.decode("utf-8").split("\0")
    files = []
    for item in filter(None, tracked):
        relative = PurePosixPath(item)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe archive member: {item}")
        if item.endswith(".zip") or "__pycache__" in relative.parts:
            continue
        if relative.parts[:2] in (("deliverables", "audio"), ("deliverables", "slides"),
                                  ("deliverables", "segments"), ("deliverables", "qa"),
                                  ("deliverables", "narration-chunks")):
            continue
        path = repo.joinpath(*relative.parts)
        if not path.is_file():
            raise FileNotFoundError(path)
        files.append((item, path))
    if not files:
        raise ValueError("Commit workshop files before packaging.")

    reports = {}
    for name, full in (("complete-workshop.zip", True), ("sample-app-and-labs.zip", False)):
        output = destination / name
        selected = [(item, path) for item, path in files if full or not item.startswith(("media/", "deliverables/"))]
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for item, path in selected:
                archive.write(path, f"advancedghcp/{item}")
            if not full:
                archive.writestr(
                    "START-HERE.txt",
                    "Open advancedghcp/README.md and workshop/README.md.\n"
                    "This lightweight archive contains the starter, labs, templates and instructor answers.\n"
                    "PowerPoint, video, transcript and source ledger are in the separately supplied complete-workshop.zip.\n"
                    "No Git metadata is included. Run git init and create a baseline commit before using worktree labs.\n"
                    "Run npm test and npm start from the advancedghcp directory.\n",
                )
        with zipfile.ZipFile(output) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"Archive CRC validation failed: {name}")
        reports[name] = {"files": len(selected), "bytes": output.stat().st_size,
                         "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}
    revision = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              check=True, capture_output=True, text=True).stdout.strip()
    report = {"result": "pass", "revision": revision, "archives": reports}
    (destination / "package-verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
