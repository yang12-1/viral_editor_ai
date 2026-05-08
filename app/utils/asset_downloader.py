import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests


ASSET_ROOT = Path("app/assets")
MANIFEST_PATH = ASSET_ROOT / "asset_manifest.json"
ASSET_GROUPS = ("fonts", "sfx", "bgm", "memes")


def _resolve_url(item):
    direct_url = item.get("url")
    if direct_url:
        return direct_url

    env_name = item.get("url_env")
    if env_name:
        return os.getenv(env_name)

    return None


def _is_http_url(url):
    parsed = urlparse(url or "")
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def ensure_asset_dirs():
    for group in ASSET_GROUPS:
        (ASSET_ROOT / group).mkdir(parents=True, exist_ok=True)


def download_asset(url, output_path, timeout=60):
    if not _is_http_url(url):
        raise ValueError(f"Invalid asset URL: {url}")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with output_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 256):
                if chunk:
                    file.write(chunk)

    return output_path


def ensure_assets(manifest_path=MANIFEST_PATH):
    """Download manifest-defined assets.

    For copyrighted meme sounds, put direct URLs you are allowed to use in
    environment variables such as VINE_BOOM_URL and METAL_PIPE_URL.
    """
    ensure_asset_dirs()
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        return {}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    downloaded = {}

    for group in ASSET_GROUPS:
        downloaded[group] = []
        for item in manifest.get(group, []):
            name = item.get("name")
            if not name:
                continue

            output_path = ASSET_ROOT / group / name
            if output_path.exists() and output_path.stat().st_size > 0:
                downloaded[group].append(str(output_path))
                continue

            url = _resolve_url(item)
            if not url:
                print(f"[asset] skipped {group}/{name}: no url or env var configured")
                continue

            try:
                download_asset(url, output_path)
                downloaded[group].append(str(output_path))
                print(f"[asset] downloaded {group}/{name}")
            except Exception as exc:
                print(f"[asset] failed {group}/{name}: {exc}")

    return downloaded
