"""Keep the Compose example exception exact; other .env files stay forbidden."""

from __future__ import annotations

import runpy
from collections.abc import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import cast

ROOT = Path(__file__).resolve().parents[2]
HYGIENE_TOOL = ROOT / "ai-agent-workspace-pack" / "_agent_ops" / "tools" / "check_repo_hygiene.py"
HELPER = runpy.run_path(str(HYGIENE_TOOL))
matches_forbidden = cast(Callable[[str], list[str]], HELPER["matches_forbidden"])
filesystem_artifacts = cast(Callable[[Path], list[tuple[str, str]]], HELPER["filesystem_artifacts"])


def test_only_required_compose_env_example_is_allowed() -> None:
    assert matches_forbidden("infra/compose/.env.example") == []
    assert matches_forbidden("infra/compose/.env.local") == [".env.*"]
    assert matches_forbidden("other/.env.example") == [".env.*"]


def test_filesystem_scan_allows_exact_placeholder_only() -> None:
    with TemporaryDirectory(prefix="meterproof-hygiene-") as temporary:
        root = Path(temporary)
        allowed = root / "infra" / "compose" / ".env.example"
        other = root / "other" / ".env.example"
        allowed.parent.mkdir(parents=True)
        other.parent.mkdir(parents=True)
        allowed.write_text("METERPROOF_PASSWORD=<local-only-password>\n", encoding="utf-8")
        other.write_text("SAMPLE=<placeholder>\n", encoding="utf-8")

        findings = filesystem_artifacts(root)

    assert findings == [("other/.env.example", "file pattern .env.*")]
