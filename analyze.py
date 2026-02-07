import xml.etree.ElementTree as ET
import sys
import json
import os
import subprocess
import tempfile

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def extract_permissions(manifest_path):
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    perms = set()

    for p in root.findall("uses-permission"):
        name = p.attrib.get(ANDROID_NS + "name")
        if name:
            perms.add(name)

    return sorted(perms)

def main(apk_path):
    if not os.path.exists(apk_path):
        print(f"APK not found: {apk_path}")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:
        result = subprocess.run(
            ["apktool", "d", "-f", apk_path, "-o", temp_dir],
            capture_output=True,
            text=True
        )

        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

        if result.returncode != 0:
            print("apktool failed")
            sys.exit(1)

        manifest_path = None
        for root, _, files in os.walk(temp_dir):
            if "AndroidManifest.xml" in files:
                manifest_path = os.path.join(root, "AndroidManifest.xml")
                break

        if not manifest_path:
            print("AndroidManifest.xml not found after decompilation")
            sys.exit(1)

        permissions = extract_permissions(manifest_path)

        print(json.dumps({
            "apk": apk_path,
            "permissions": permissions
        }, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: docker run apk-analyzer <apk_path>")
        sys.exit(1)

    main(sys.argv[1])
