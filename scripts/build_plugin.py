"""Build the complete plugin ZIP and SHA-256 receipt using the standard library."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "plugin.json").read_text())
    overlay = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    for key in ("name", "version", "description", "author"):
        assert manifest[key] == overlay[key], key
    interface = manifest["extensions"]["com.openai"]["interface"]
    assert interface == overlay["interface"]
    for key in ("composerIcon", "logo"):
        asset = (ROOT / interface[key]).resolve()
        assert asset.is_relative_to(ROOT) and asset.is_file()
    skill = ROOT / "skills/won-myunghee/SKILL.md"
    assert "\nname: won-myunghee\n" in skill.read_text()
    apps = json.loads((ROOT / ".app.json").read_text())["apps"]
    assert len(apps) == 6 and all(x["id"] and isinstance(x["required"], bool) for x in apps.values())
    assert manifest["extensions"]["com.openai"]["apps"] == "./.app.json"
    assert len(interface["shortDescription"]) <= 30
    sources = json.loads((ROOT / "BUNDLED-SOURCES.json").read_text())
    assert sources["version"] == manifest["version"]
    for name in ("market-news-radar", "world-memory-autopilot"):
        entry = sources["upstream_skill_releases"][name]
        skill_root = ROOT / "skills" / name
        assert (skill_root / "VERSION").read_text().strip() == entry["version"]
        assert f"Version: {chr(96)}{entry['version']}{chr(96)}" in (skill_root / "SKILL.md").read_text()
        for relative, expected in entry["distribution_file_sha256"].items():
            if relative == "agents/openai.yaml":
                assert "  products:\n  - CHAT\n  - CODEX\n" in (skill_root / relative).read_text()
            else:
                assert hashlib.sha256((skill_root / relative).read_bytes()).hexdigest() == expected, relative
    paths = [ROOT / ".app.json", ROOT / "BUNDLED-SOURCES.json", ROOT / "plugin.json", ROOT / ".codex-plugin/plugin.json", ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "scripts/build_plugin.py"]
    for directory in ("assets", "skills"):
        for path in sorted((ROOT / directory).rglob("*")):
            assert not path.is_symlink(), path
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc" and path.name != ".DS_Store":
                paths.append(path)
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f"economic-research-club-plugin-{manifest['version']}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(paths):
            assert not path.is_symlink()
            info = zipfile.ZipInfo(path.relative_to(ROOT).as_posix(), (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, path.read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert len(bundle.namelist()) == len(paths)
        for path in paths:
            assert bundle.read(path.relative_to(ROOT).as_posix()) == path.read_bytes()
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".sha256").write_text(f"{digest}  {archive.name}\n")
    print(f"Verified {len(paths)} files: {archive.name}\nSHA-256: {digest}")


if __name__ == "__main__":
    main()
