import json
import urllib.request
from urllib.parse import ParseResult

from ..errors import VersionError
from ..utils import info
from .version import Version


def fetch_rubygem_versions(url: ParseResult) -> list[Version]:
    if url.netloc != "rubygems.org":
        return []
    parts = url.path.split("/")
    gem = parts[-1]
    gem_name, _ = gem.rsplit("-")
    versions_url = f"https://rubygems.org/api/v1/versions/{gem_name}.json"
    info(f"fetch {versions_url}")
    resp = urllib.request.urlopen(versions_url)
    json_versions = json.load(resp)
    if len(json_versions) == 0:
        raise VersionError("No versions found")

    versions: list[Version] = []
    for version in json_versions:
        number = version["number"]
        assert isinstance(number, str)
        prerelease = version["prerelease"]
        assert isinstance(prerelease, bool)
        version.append(Version(number, prerelease=prerelease))
    return versions
