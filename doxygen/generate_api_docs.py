#!/usr/bin/env python3
"""Build the ORCA code reference with Doxygen and put it into the documentation site.

Run it from anywhere:

    python3 doxygen/generate_api_docs.py                       # downloads uhd_radar (branch main)
    python3 doxygen/generate_api_docs.py --source ../uhd_radar  # uses a copy of uhd_radar you already have

What it does:

  1. Finds Doxygen.
  2. Gets the ORCA code: your own checkout (--source) or a fresh download into doxygen/_build/uhd_radar.
  3. Copies the code files and the front page (doxygen/mainpage.dox) into one working folder and
     runs Doxygen on it with doxygen/Doxyfile.
  4. Replaces static/api/ with the new HTML. The site serves that folder at /api/.
  5. Rewrites content/en/docs/radar/code-reference/coverage.md, the page that lists which functions
     still need a comment.

Only the Python standard library is used. Tests: python3 -m pytest doxygen/ -q
"""
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import NamedTuple

UHD_RADAR_URL = "https://github.com/HI-SNR-Lab/uhd_radar.git"
SITE_OUTPUT = Path("static") / "api"
LANDING_PAGE = Path("content") / "en" / "docs" / "radar" / "code-reference" / "_index.md"
COVERAGE_PAGE = Path("content") / "en" / "docs" / "radar" / "code-reference" / "coverage.md"
SOURCE_PATTERNS = ("*.py", "*.cpp", "*.hpp")  # the files that get documented
SKIPPED_FOLDERS = (".git", "data", "sdr/build")  # git's own files, recordings, compiler output


class FileCoverage(NamedTuple):
    """How many functions of one source file have a description Doxygen can show."""

    path: str  # path inside uhd_radar, with forward slashes
    documented: int
    total: int
    missing: list  # names of the functions without a description


# ---------------------------------------------------------------- locations
def repo_root() -> Path:
    """The orca-documentation folder (the parent of the folder this script is in)."""
    return Path(__file__).resolve().parent.parent


def relative_source_path(path, root) -> str:
    """Path of a source file inside uhd_radar, with forward slashes. Doxygen reports full paths."""
    path = str(path).replace("\\", "/")
    root = str(root).replace("\\", "/").rstrip("/")
    if path.lower().startswith(root.lower() + "/"):  # Windows paths can differ in upper/lower case
        return path[len(root) + 1:]
    return path


def is_test_path(path: str) -> bool:
    """True for unit tests and test scripts, which the coverage summary leaves out."""
    parts = path.split("/")
    return parts[0] == "tests" or "test_scripts" in parts or parts[-1].startswith("test_")


# -------------------------------------------------------------------- tools
def find_doxygen() -> str:
    """Return the path of the doxygen program, or stop with instructions for installing it."""
    path = shutil.which("doxygen")
    if path is None:
        raise SystemExit(
            "Doxygen was not found. Install it, then run this script again:\n"
            "  Windows: installer from https://www.doxygen.nl/download.html (tick 'add to PATH')\n"
            "  macOS:   brew install doxygen\n"
            "  Linux:   sudo apt install doxygen")
    return path


def doxygen_version(doxygen: str) -> str:
    """Version number of the installed Doxygen, for example '1.9.8' ('' if it cannot be read)."""
    try:
        result = subprocess.run([doxygen, "--version"], capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return ""
    return result.stdout.strip().split(" ")[0]


def run(command: list) -> None:
    """Run a command and stop with a readable message if it fails."""
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        raise SystemExit(f"'{command[0]}' was not found. Install it, or pass --source with your own copy of uhd_radar.")
    except subprocess.CalledProcessError:
        raise SystemExit("This command failed: " + " ".join(command))


def ensure_source(source, ref: str) -> Path:
    """Return the folder holding the ORCA code.

    With `source`, check that it really is a copy of uhd_radar and use it as it is.
    Without it, download (or update) branch or tag `ref` into doxygen/_build/uhd_radar.
    """
    if source is not None:
        source = Path(source).expanduser().absolute()
        if not ((source / "run.py").is_file() and (source / "sdr").is_dir()):
            raise SystemExit(f"{source} does not look like a checkout of uhd_radar (expected run.py and sdr/ inside it).")
        return source

    target = repo_root() / "doxygen" / "_build" / "uhd_radar"
    if (target / ".git").is_dir():
        run(["git", "-C", str(target), "fetch", "--depth", "1", "origin", ref])
        run(["git", "-C", str(target), "checkout", "--quiet", "--detach", "FETCH_HEAD"])
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--depth", "1", "--branch", ref, UHD_RADAR_URL, str(target)])
    return target


def _is_git_checkout(folder: Path) -> bool:
    """True if `folder` is the top folder of a git checkout, not just a folder somewhere inside one."""
    return (folder / ".git").exists()


def source_version(source: Path) -> str:
    """Short commit hash and date of the code being documented, for example '6d75349 (2026-10-30)'."""
    if not _is_git_checkout(source):
        return "unknown version"
    try:
        result = subprocess.run(["git", "-C", str(source), "log", "-1", "--format=%h (%cs)"],
                                capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return "unknown version"
    return result.stdout.strip() or "unknown version"


def _source_files(source: Path) -> list:
    """Paths (relative, forward slashes) of the code files to document.

    In a git checkout these are the files git knows about, so a local Python environment or
    other files lying around in the folder are left out. Elsewhere, every matching file is
    taken except those in SKIPPED_FOLDERS.
    """
    if _is_git_checkout(source):
        try:
            listing = subprocess.run(["git", "-C", str(source), "ls-files", "-z", "--"] + list(SOURCE_PATTERNS),
                                     capture_output=True, text=True, check=True).stdout
            tracked = sorted(name for name in listing.split("\0") if name and (source / name).is_file())
            if tracked:
                return tracked
        except (OSError, subprocess.CalledProcessError):
            pass
    files = set()
    for pattern in SOURCE_PATTERNS:
        for item in source.rglob(pattern):
            relative = item.relative_to(source).as_posix()
            if item.is_file() and not any(relative.startswith(skip + "/") for skip in SKIPPED_FOLDERS):
                files.add(relative)
    return sorted(files)


def stage_input(source: Path, front_page: Path, stage: Path) -> None:
    """Copy the code files and the front page into one fresh folder for Doxygen to read.

    Doxygen then sees a single top folder, so every path in the pages is relative to the top
    of uhd_radar and no folder name of this computer ends up in the site.
    """
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for relative in _source_files(source):
        target = stage / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, target)
    shutil.copy2(front_page, stage / front_page.name)


def replace_dir(src: Path, dst: Path) -> None:
    """Make `dst` an exact copy of `src`, so pages of deleted source files do not stay behind."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def run_doxygen(doxygen: str, input_dir: Path, build: Path, version: str) -> None:
    """Run Doxygen. The Doxyfile reads the three ORCA_* environment variables set here."""
    if build.exists():
        shutil.rmtree(build)
    build.mkdir(parents=True)
    env = dict(
        os.environ,
        ORCA_INPUT_DIR=input_dir.as_posix(),
        ORCA_BUILD_DIR=build.as_posix(),
        ORCA_VERSION=version,
    )
    result = subprocess.run([doxygen, "Doxyfile"], cwd=repo_root() / "doxygen", env=env)
    if result.returncode != 0:
        raise SystemExit("Doxygen stopped with an error (see the messages above).")


# ----------------------------------------------------------------- coverage
def _has_description(member) -> bool:
    """True if Doxygen found a brief or a detailed description for this function."""
    for tag in ("briefdescription", "detaileddescription"):
        element = member.find(tag)
        if element is not None and "".join(element.itertext()).strip():
            return True
    return False


def _display_name(name: str, path: str) -> str:
    """Drop the module prefix Doxygen puts on Python names ('generate_chirp.plot_chirp' -> 'plot_chirp')."""
    module = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    if path.endswith(".py") and name.startswith(module + "."):
        return name[len(module) + 1:]
    return name


def collect_coverage(xml_dir, root) -> list:
    """Read Doxygen's XML output and count, per source file, the functions that have a description.

    A function declared in a header and defined in a .cpp file appears twice in the XML.
    It is counted once, under the file that holds its body. Declarations without a body are
    skipped: they are prototypes, or variables such as "inline mt19937 generator(0);" that
    Doxygen mistakes for functions.
    """
    functions = {}  # (file, name, arguments) -> has a description
    for xml_file in sorted(Path(xml_dir).glob("*.xml")):
        compound = ET.parse(xml_file).getroot().find("compounddef")
        if compound is None:  # index.xml and Doxyfile.xml hold no code
            continue
        for member in compound.iter("memberdef"):
            location = member.find("location")
            if member.get("kind") != "function" or location is None:
                continue
            where = location.get("bodyfile")
            if not where:
                continue
            path = relative_source_path(where, root)
            name = member.findtext("qualifiedname") or member.findtext("name") or "?"
            key = (path, _display_name(name, path), member.findtext("argsstring") or "")
            functions[key] = functions.get(key, False) or _has_description(member)

    rows = []
    for path in sorted({key[0] for key in functions}):
        in_file = {key: done for key, done in functions.items() if key[0] == path}
        missing = sorted((key[1] for key, done in in_file.items() if not done), key=str.lower)
        rows.append(FileCoverage(path, sum(in_file.values()), len(in_file), missing))
    return rows


def read_warnings(log_path, root) -> list:
    """Doxygen's warnings as 'file:line: message', without duplicates and without the folder prefix."""
    log_path = Path(log_path)
    if not log_path.is_file():
        return []
    warnings = []
    for line in log_path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"^(.*?):(\d+): warning: (.*)$", line)
        if match:
            entry = f"{relative_source_path(match.group(1), root)}:{match.group(2)}: {match.group(3).strip()}"
            if entry not in warnings:
                warnings.append(entry)
    return warnings


def _percent(documented: int, total: int) -> str:
    return f"{round(100 * documented / total)}%" if total else "n/a"


def render_coverage_page(rows: list, version: str, warnings=(), doxygen_version: str = "") -> str:
    """The Markdown text of the 'Documentation coverage' page of the site."""
    code = [row for row in rows if not is_test_path(row.path)]
    code_done, code_total = sum(r.documented for r in code), sum(r.total for r in code)
    all_done, all_total = sum(r.documented for r in rows), sum(r.total for r in rows)

    lines = [
        "---",
        "title: Documentation coverage",
        "linkTitle: Documentation coverage",
        "description: Which functions in the ORCA code have a comment that Doxygen can show",
        "weight: 10",
        "---",
        "",
        "<!-- Written by doxygen/generate_api_docs.py. Do not edit by hand: the next run overwrites it. -->",
        "",
        f"Generated from `uhd_radar` commit {version}" + (f" with Doxygen {doxygen_version}." if doxygen_version else "."),
        "",
        "A function counts as documented when Doxygen found a description for it. Doxygen only reads comments "
        "written in its own format, so an ordinary `//` or `#` comment does not count. The format is described "
        "under \"Doxygen Requirements\" in the "
        "[uhd_radar style guide](https://github.com/HI-SNR-Lab/uhd_radar/blob/main/STYLEGUIDE.md).",
        "",
        f"**Summary:** {code_done} of {code_total} functions ({_percent(code_done, code_total)}) "
        "have a description. Test files are in the table but not in this count.",
        "",
        "| File | Documented | Functions | Coverage |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row.path} | {row.documented} | {row.total} | {_percent(row.documented, row.total)} |")
    lines.append(f"| **All files** | {all_done} | {all_total} | {_percent(all_done, all_total)} |")

    if any(row.missing for row in code):
        lines += ["", "## Functions without a description", "",
                  "Test files are left out of this list."]
        for row in code:
            if row.missing:
                lines += ["", f"### {row.path}", ""]
                lines += [f"- `{name}`" for name in row.missing]

    if warnings:
        lines += ["", "## Doxygen warnings", "",
                  "Comments that Doxygen could read but that do not match the code, "
                  "for example a `@param` naming an argument the function does not have.", ""]
        for warning in warnings:
            place, _, message = warning.partition(": ")
            lines.append(f"- `{place}`: " + html.escape(message, quote=False).replace("*", "\\*"))

    return "\n".join(lines) + "\n"


def missing_api_links(markdown: str, api_dir) -> list:
    """Links of the form (/api/page.html) in `markdown` whose page does not exist in `api_dir`.

    The landing page links straight to a few reference pages. If a class or file is renamed
    in uhd_radar, its page gets a new name and such a link would quietly stop working.
    """
    links = set(re.findall(r"\]\((/api/[^)#\s]+)", markdown))
    return sorted(link for link in links if not (Path(api_dir) / link[len("/api/"):]).is_file())


# --------------------------------------------------------------------- main
def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Build the ORCA code reference with Doxygen.")
    parser.add_argument("--source", metavar="FOLDER",
                        help="a copy of uhd_radar on this computer (default: download it)")
    parser.add_argument("--ref", default="main", metavar="BRANCH",
                        help="branch or tag to download when --source is not given (default: main)")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    doxygen = find_doxygen()
    source = ensure_source(args.source, args.ref)
    version = source_version(source)
    root = repo_root()
    stage = root / "doxygen" / "_build" / "input"
    build = root / "doxygen" / "_build" / "out"

    print(f"Documenting uhd_radar {version} from {source} with Doxygen {doxygen_version(doxygen)}")
    stage_input(source, root / "doxygen" / "mainpage.dox", stage)
    run_doxygen(doxygen, stage, build, version)
    replace_dir(build / "html", root / SITE_OUTPUT)

    rows = collect_coverage(build / "xml", stage)
    warnings = read_warnings(build / "doxygen_warnings.log", stage)
    page = root / COVERAGE_PAGE
    page.parent.mkdir(parents=True, exist_ok=True)
    with open(page, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(render_coverage_page(rows, version, warnings, doxygen_version(doxygen)))

    landing = root / LANDING_PAGE
    if landing.is_file():
        broken = missing_api_links(landing.read_text(encoding="utf-8"), root / SITE_OUTPUT)
        if broken:
            print(f"WARNING: {LANDING_PAGE.as_posix()} links to pages that no longer exist: " + ", ".join(broken))

    html_files = sum(1 for item in (root / SITE_OUTPUT).rglob("*") if item.is_file())
    print(f"Wrote {html_files} files to {SITE_OUTPUT.as_posix()}/ and updated {COVERAGE_PAGE.as_posix()}")
    print("Start the site (docker compose up) and open http://localhost:1313/api/ to look at it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
