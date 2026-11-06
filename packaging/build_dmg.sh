#!/bin/sh
# Builds dist/EMA-GUI-<version>-arm64.dmg from the repo's .venv. Run from anywhere: sh packaging/build_dmg.sh
set -eu
cd "$(dirname "$0")/.."
VERSION="${EMA_VERSION:-1.0.0}"
DMG="dist/EMA-GUI-$VERSION-arm64.dmg"

[ -f ema.pt ] && [ -f decoder.pt ] || .venv/bin/hf download canberkkkkkk/ema-lightning ema.pt decoder.pt --local-dir .
.venv/bin/pip install -q pyinstaller
EMA_VERSION="$VERSION" .venv/bin/pyinstaller --noconfirm --clean --distpath dist --workpath build packaging/ema-gui.spec

STAGE="$(mktemp -d)"
cp -R "dist/EMA GUI.app" "$STAGE/"
ln -s /Applications "$STAGE/Applications"
rm -f "$DMG"
hdiutil create -volname "EMA GUI" -srcfolder "$STAGE" -format UDZO -ov "$DMG" > /dev/null
rm -rf "$STAGE"
echo "$DMG ($(du -h "$DMG" | cut -f1))"
