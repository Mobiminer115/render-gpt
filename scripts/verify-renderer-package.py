#!/usr/bin/env python3
"""Verify Amethyst's bundled OpenGL backends and Java 8 runtime in the IPA payload."""
from pathlib import Path
import plistlib
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "artifacts/Payload/AngelAuraAmethyst.app")
frameworks = root / "Frameworks"
checks = {
    "MobileGlues backend": frameworks / "libmobileglues.dylib",
    "GL4ES backend": frameworks / "libgl4es_114.dylib",
    "EGL framework": frameworks / "libEGL.framework" / "libEGL",
    "OpenGL ES framework": frameworks / "libGLESv2.framework" / "libGLESv2",
    "Java 8 runtime": root / "java_runtimes" / "java-8-openjdk" / "release",
    "LWJGL OpenGL bridge": root / "Frameworks" / "liblwjgl_opengl.dylib",
}
failed = False
for label, path in checks.items():
    ok = path.is_file()
    print(f'{"PASS" if ok else "FAIL"} {label}: {path}')
    failed |= not ok

release = checks["Java 8 runtime"]
if release.is_file():
    text = release.read_text(errors="replace")
    if 'JAVA_VERSION="1.8' not in text and 'JAVA_VERSION="8' not in text:
        print(f"FAIL Java runtime is not identified as Java 8: {text[:240]!r}")
        failed = True
    else:
        print("PASS Java runtime version metadata identifies Java 8")

info = root / "Info.plist"
if info.is_file():
    with info.open("rb") as f:
        plist = plistlib.load(f)
    print(f"INFO bundle={plist.get('CFBundleIdentifier')} version={plist.get('CFBundleShortVersionString')}")
else:
    print(f"FAIL Info.plist missing: {info}")
    failed = True

if failed:
    sys.exit("Renderer package verification failed; refusing to publish an incomplete baseline.")
print("Renderer package verification passed.")
