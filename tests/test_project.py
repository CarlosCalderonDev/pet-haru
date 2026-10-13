from __future__ import annotations

import functools
import http.server
import json
import re
import socketserver
import threading
import unittest
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

import sys

sys.path.insert(0, str(SCRIPTS))

from pet_config import STATES, load_metadata, sprite_settings  # noqa: E402
from validate_pet import validate  # noqa: E402


class ProjectIntegrityTests(unittest.TestCase):
    def test_canonical_atlas_and_derived_frames_are_valid(self) -> None:
        report = validate()
        self.assertTrue(report["valid"], report["errors"])
        self.assertEqual(report["errors"], [])

    def test_metadata_matches_image_geometry(self) -> None:
        atlas_path, width, height, cell_w, cell_h, counts = sprite_settings()
        with Image.open(atlas_path) as atlas:
            self.assertEqual(atlas.size, (width, height))
        self.assertEqual(width % cell_w, 0)
        self.assertEqual(height % cell_h, 0)
        self.assertEqual(len(counts), len(STATES))

    def test_viewer_state_manifest_matches_metadata(self) -> None:
        source = (ROOT / "viewer" / "app.js").read_text(encoding="utf-8")
        entries = re.findall(r'id: "([^"]+)"[^\n]+frames: (\d+)', source)
        self.assertEqual([state for state, _ in entries], STATES)
        self.assertEqual([int(count) for _, count in entries], load_metadata()["spritesheet"]["frames_per_row"])

    def test_readme_local_links_exist(self) -> None:
        source = (ROOT / "README.md").read_text(encoding="utf-8")
        links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", source)
        local_links = [link for link in links if not re.match(r"^(?:[a-z]+://|#)", link)]
        missing = [link for link in local_links if not (ROOT / link).exists()]
        self.assertEqual(missing, [])

        headings = re.findall(r"^#{2,6}\s+(.+)$", source, flags=re.MULTILINE)
        anchors = {
            "#" + re.sub(r"[^\w -]", "", heading.lower()).replace(" ", "-")
            for heading in headings
        }
        internal_links = [link for link in links if link.startswith("#")]
        self.assertEqual([link for link in internal_links if link not in anchors], [])

    def test_no_personal_absolute_paths_in_sources(self) -> None:
        roots = [ROOT / "scripts", ROOT / "viewer", ROOT / "docs", ROOT / ".github"]
        suffixes = {".py", ".ps1", ".js", ".html", ".css", ".md", ".json", ".yml", ".yaml"}
        offenders = []
        forbidden = ("C:" + "\\Users\\", "." + "codex", "codex-" + "runtimes")
        for source_root in roots:
            for path in source_root.rglob("*"):
                if path.is_file() and path.suffix.lower() in suffixes:
                    text = path.read_text(encoding="utf-8")
                    if any(marker in text for marker in forbidden):
                        offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])


class ViewerHttpSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
        cls.server = socketserver.TCPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_viewer_assets_are_served(self) -> None:
        for path, content_type in [
            ("/viewer/", "text/html"),
            ("/viewer/styles.css", "text/css"),
            ("/viewer/app.js", "text/javascript"),
            ("/assets/frames/idle/00.png", "image/png"),
        ]:
            with self.subTest(path=path):
                with urllib.request.urlopen(self.base_url + path, timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    self.assertIn(content_type, response.headers.get_content_type())
                    self.assertGreater(len(response.read()), 0)


if __name__ == "__main__":
    unittest.main()
