"""Tests for generate_api_docs.py.  Run with:  python3 -m pytest doxygen/ -q

None of these tests need Doxygen, git or a network connection.
"""
from pathlib import Path
from xml.sax.saxutils import escape

import pytest

import generate_api_docs as g


# --------------------------------------------------------------- small helpers
def test_repo_root_is_script_parent():
    assert g.repo_root() == Path(g.__file__).resolve().parent.parent


def test_missing_doxygen_is_explained(monkeypatch):
    monkeypatch.setattr(g.shutil, "which", lambda name: None)
    with pytest.raises(SystemExit) as stop:
        g.find_doxygen()
    message = str(stop.value)
    assert "Doxygen was not found" in message
    assert "doxygen.nl" in message


def test_bad_source_is_refused(tmp_path):
    with pytest.raises(SystemExit) as stop:
        g.ensure_source(tmp_path, "main")
    assert "does not look like a checkout of uhd_radar" in str(stop.value)
    assert list(tmp_path.iterdir()) == []  # nothing created, nothing deleted


def test_good_source_is_accepted(tmp_path):
    (tmp_path / "run.py").write_text("")
    (tmp_path / "sdr").mkdir()
    assert g.ensure_source(tmp_path, "main") == tmp_path


def test_replace_dir_removes_stale_files(tmp_path):
    new = tmp_path / "new"
    new.mkdir()
    (new / "index.html").write_text("new")
    old = tmp_path / "site" / "api"
    old.mkdir(parents=True)
    (old / "index.html").write_text("old")
    (old / "page_for_a_deleted_file.html").write_text("stale")

    g.replace_dir(new, old)

    assert sorted(p.name for p in old.iterdir()) == ["index.html"]
    assert (old / "index.html").read_text() == "new"


def test_stage_input_copies_code_and_front_page_into_one_folder(tmp_path):
    source = tmp_path / "uhd_radar"
    (source / "sdr").mkdir(parents=True)
    (source / "sdr" / "chirp.cpp").write_text("// code")
    (source / "run.py").write_text("# code")
    (source / ".git" / "objects").mkdir(parents=True)
    (source / ".git" / "objects" / "pack.py").write_text("git data")
    (source / "data" / "my_run").mkdir(parents=True)
    (source / "data" / "my_run" / "notes.py").write_text("a recording's helper script")
    (source / "sdr" / "build" / "CMakeFiles").mkdir(parents=True)
    (source / "sdr" / "build" / "CMakeFiles" / "CMakeCXXCompilerId.cpp").write_text("compiler output")
    (source / "match_filter.png").write_text("not code")
    front_page = tmp_path / "mainpage.dox"
    front_page.write_text("/** @mainpage ORCA */")
    stage = tmp_path / "build" / "input"
    stage.mkdir(parents=True)
    (stage / "left_over_from_last_run.py").write_text("stale")

    g.stage_input(source, front_page, stage)

    staged = sorted(p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file())
    assert staged == ["mainpage.dox", "run.py", "sdr/chirp.cpp"]


def test_stage_input_takes_only_files_git_knows_about(tmp_path):
    if g.shutil.which("git") is None:
        pytest.skip("git is not installed")
    source = tmp_path / "uhd_radar"
    (source / "sdr").mkdir(parents=True)
    (source / "run.py").write_text("# tracked")
    (source / "sdr" / "chirp.cpp").write_text("// tracked")
    (source / "venv" / "lib").mkdir(parents=True)
    (source / "venv" / "lib" / "site.py").write_text("# somebody's local Python environment")
    git = ["git", "-C", str(source), "-c", "user.name=t", "-c", "user.email=t@example.org"]
    g.subprocess.run(["git", "init", "--quiet", str(source)], check=True)
    g.subprocess.run(git + ["add", "run.py", "sdr/chirp.cpp"], check=True)
    g.subprocess.run(git + ["commit", "--quiet", "-m", "code"], check=True)
    front_page = tmp_path / "mainpage.dox"
    front_page.write_text("/** @mainpage ORCA */")
    stage = tmp_path / "input"

    g.stage_input(source, front_page, stage)

    staged = sorted(p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file())
    assert staged == ["mainpage.dox", "run.py", "sdr/chirp.cpp"]


def test_stage_input_copes_with_a_plain_copy_inside_another_git_repo(tmp_path):
    """A downloaded (not cloned) uhd_radar placed inside some other git repository is not 'known to git'."""
    if g.shutil.which("git") is None:
        pytest.skip("git is not installed")
    git = ["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@example.org"]
    g.subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    (tmp_path / "notes.txt").write_text("the other repository's own file")
    g.subprocess.run(git + ["add", "notes.txt"], check=True)
    g.subprocess.run(git + ["commit", "--quiet", "-m", "not the radar code"], check=True)
    source = tmp_path / "uhd_radar"
    (source / "sdr").mkdir(parents=True)
    (source / "run.py").write_text("# code")
    (source / "sdr" / "chirp.cpp").write_text("// code")
    front_page = tmp_path / "mainpage.dox"
    front_page.write_text("/** @mainpage ORCA */")
    stage = tmp_path / "input"

    g.stage_input(source, front_page, stage)

    staged = sorted(p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file())
    assert staged == ["mainpage.dox", "run.py", "sdr/chirp.cpp"]
    # The surrounding repository's last commit says nothing about the radar code.
    assert g.source_version(source) == "unknown version"


def test_relative_source_path_normalizes():
    root = Path("/work/uhd_radar")
    assert g.relative_source_path("/work/uhd_radar/sdr/chirp.cpp", root) == "sdr/chirp.cpp"
    assert g.relative_source_path("sdr\\chirp.cpp", root) == "sdr/chirp.cpp"
    assert g.relative_source_path("C:\\Work\\uhd_radar\\sdr\\chirp.cpp", "c:/work/uhd_radar") == "sdr/chirp.cpp"
    assert g.relative_source_path("/somewhere/else/x.py", root) == "/somewhere/else/x.py"


def test_is_test_path():
    assert g.is_test_path("tests/sdr/test_chirp.cpp")
    assert g.is_test_path("postprocessing/test_scripts/loopback_testing.py")
    assert g.is_test_path("postprocessing/test_code.py")
    assert not g.is_test_path("postprocessing/processing.py")
    assert not g.is_test_path("sdr/main.cpp")


# ------------------------------------------------------------------- coverage
def _member(member_id, name, bodyfile, brief="", detail="", qualified=None, args="()", declfile=None, has_body=True):
    qualified_tag = f"<qualifiedname>{qualified}</qualifiedname>" if qualified else ""
    body = f' bodyfile="{bodyfile}" bodystart="1"' if has_body else ""
    return f"""
      <memberdef kind="function" id="{member_id}">
        <name>{name}</name>{qualified_tag}
        <argsstring>{escape(args)}</argsstring>
        <briefdescription><para>{brief}</para></briefdescription>
        <detaileddescription><para>{detail}</para></detaileddescription>
        <location file="{declfile or bodyfile}" line="1"{body}/>
      </memberdef>"""


def _compound(kind, name, members):
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<doxygen><compounddef id="x" kind="{kind}"><compoundname>{name}</compoundname>
<sectiondef kind="func">{''.join(members)}</sectiondef></compounddef></doxygen>"""


@pytest.fixture
def xml_dir(tmp_path):
    root = "/work/uhd_radar"
    # A free function declared in the header and defined in the .cpp: Doxygen writes it twice, with two ids.
    shared = dict(name="generate_out_filename", bodyfile=f"{root}/sdr/utils.cpp",
                  detail="Change filename if several files are written.", args="(const std::string &base_fn)")
    (tmp_path / "utils_8hpp.xml").write_text(_compound("file", "utils.hpp", [
        _member("utils_8hpp_1a50", declfile=f"{root}/sdr/utils.hpp", **shared)]))
    (tmp_path / "utils_8cpp.xml").write_text(_compound("file", "utils.cpp", [
        _member("utils_8cpp_1adc", **shared)]))
    # Class methods: declared in the header, body (and comment) in the .cpp.
    chirp = dict(bodyfile=f"{root}/sdr/chirp.cpp", declfile=f"{root}/sdr/chirp.hpp")
    (tmp_path / "classChirp.xml").write_text(_compound("class", "Chirp", [
        _member("c1", "Chirp", brief="constructs a new Chirp object", qualified="Chirp::Chirp", **chirp),
        _member("c2", "getTimeOffset", qualified="Chirp::getTimeOffset", args="() const", **chirp),
        _member("c3", "setTimeOffset", brief="sets the offset", qualified="Chirp::setTimeOffset", **chirp),
        _member("c4", "assignVarFromYaml", detail="reads the YAML file", qualified="Chirp::assignVarFromYaml", **chirp),
    ]))
    # A Python module is a "namespace" compound.
    (tmp_path / "namespacegenerate__chirp.xml").write_text(_compound("namespace", "generate_chirp", [
        _member("p1", "generate_chirp", f"{root}/preprocessing/generate_chirp.py",
                detail="Generate a chirp.", qualified="generate_chirp.generate_chirp", args="(config)"),
        _member("p2", "plot_chirp", f"{root}/preprocessing/generate_chirp.py",
                qualified="generate_chirp.plot_chirp", args="(ts, chirp)")]))
    # "inline mt19937 random_generator_tx(0);" is a variable, but Doxygen files it under functions.
    # It has no body, which is how the script tells it apart.
    (tmp_path / "pseudorandom__phase_8hpp.xml").write_text(_compound("file", "pseudorandom_phase.hpp", [
        _member("v1", "random_generator_tx", f"{root}/sdr/pseudorandom_phase.hpp", args="(0)", has_body=False)]))
    # Files Doxygen also writes into the folder; they hold no functions and must not break anything.
    (tmp_path / "index.xml").write_text("<doxygenindex></doxygenindex>")
    (tmp_path / "Doxyfile.xml").write_text("<doxyfile></doxyfile>")
    return tmp_path


def test_coverage_counts_each_function_once(xml_dir):
    rows = g.collect_coverage(xml_dir, Path("/work/uhd_radar"))
    by_path = {row.path: row for row in rows}

    assert [row.path for row in rows] == sorted(by_path)
    assert (by_path["sdr/utils.cpp"].documented, by_path["sdr/utils.cpp"].total) == (1, 1)
    assert (by_path["sdr/chirp.cpp"].documented, by_path["sdr/chirp.cpp"].total) == (3, 4)
    assert by_path["sdr/chirp.cpp"].missing == ["Chirp::getTimeOffset"]
    # Python names lose the module prefix Doxygen adds ("generate_chirp.plot_chirp").
    assert by_path["preprocessing/generate_chirp.py"].missing == ["plot_chirp"]
    assert "sdr/utils.hpp" not in by_path  # counted where the function body is
    assert "sdr/pseudorandom_phase.hpp" not in by_path  # a declaration without a body is not counted


def test_render_coverage_page_has_totals():
    rows = [
        g.FileCoverage("sdr/chirp.cpp", 3, 4, ["Chirp::getTimeOffset"]),
        g.FileCoverage("sdr/utils.cpp", 1, 1, []),
        g.FileCoverage("tests/sdr/test_chirp.cpp", 0, 2, ["TEST", "main"]),
    ]
    page = g.render_coverage_page(rows, "6d75349 (2026-10-30)")

    assert page.startswith("---\n")
    assert "title: Documentation coverage" in page
    assert "6d75349 (2026-10-30)" in page
    assert "| sdr/chirp.cpp | 3 | 4 | 75% |" in page
    assert "| **All files** | 4 | 7 | 57% |" in page
    assert "4 of 5 functions (80%)" in page  # the summary leaves test files out
    assert "- `Chirp::getTimeOffset`" in page
    assert "Doxygen warnings" not in page  # no warnings were passed in
    assert "with Doxygen" not in page  # no Doxygen version was passed in


def test_render_coverage_page_names_the_doxygen_version():
    page = g.render_coverage_page([g.FileCoverage("run.py", 0, 1, ["main"])], "6d75349 (2026-10-30)",
                                  doxygen_version="1.9.8")
    assert "Generated from `uhd_radar` commit 6d75349 (2026-10-30) with Doxygen 1.9.8." in page


def test_render_coverage_page_lists_warnings():
    page = g.render_coverage_page(
        [g.FileCoverage("sdr/main.cpp", 1, 1, [])], "abc1234 (2026-01-01)",
        warnings=["sdr/main.cpp:92: argument 'error_count' of command @param is not found"])
    assert "## Doxygen warnings" in page
    assert "- `sdr/main.cpp:92`: argument 'error_count' of command @param is not found" in page


def test_read_warnings_strips_root_and_duplicates(tmp_path):
    log = tmp_path / "doxygen_warnings.log"
    line = "/work/uhd_radar/sdr/main.cpp:92: warning: argument 'error_count' of command @param is not found\n"
    log.write_text(line + line + "  continuation text that is not a warning line\n")
    assert g.read_warnings(log, Path("/work/uhd_radar")) == [
        "sdr/main.cpp:92: argument 'error_count' of command @param is not found"]


def test_read_warnings_without_a_log_is_empty(tmp_path):
    assert g.read_warnings(tmp_path / "missing.log", tmp_path) == []


# ------------------------------------------------------- links on the landing page
def test_missing_api_links_reports_links_without_a_page(tmp_path):
    api = tmp_path / "api"
    api.mkdir()
    (api / "classSdr.html").write_text("")
    (api / "index.html").write_text("")
    text = ("See [`Sdr`](/api/classSdr.html), [`Old`](/api/classOld.html#details), "
            "[the reference](/api/index.html) and [the guide](/docs/radar/).")
    assert g.missing_api_links(text, api) == ["/api/classOld.html"]
