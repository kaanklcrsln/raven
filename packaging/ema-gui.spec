# PyInstaller spec for EMA GUI.app (Apple Silicon). Built by packaging/build_dmg.sh.
import os

from PyInstaller.utils.hooks import collect_data_files

VERSION = os.environ.get("EMA_VERSION", "1.0.0")
REPO = os.path.abspath(os.path.join(SPECPATH, ".."))

datas = [
    # the model ships inside the app, so the first launch needs no internet
    (os.path.join(REPO, "ema.pt"), "."),
    (os.path.join(REPO, "decoder.pt"), "."),
    (os.path.join(REPO, "Bagel_Fat_One", "BagelFatOne-Regular.ttf"), "Bagel_Fat_One"),
    (os.path.join(REPO, "Bagel_Fat_One", "OFL.txt"), "Bagel_Fat_One"),
    (os.path.join(REPO, "LICENSE"), "."),
] + collect_data_files("normalizer_tr") + collect_data_files("ema_lightning")

a = Analysis(
    [os.path.join(REPO, "ema-gui", "app.py")],
    datas=datas,
    # installed in the same venv for EMA Island and Raven Web, never imported by EMA GUI
    excludes=["gradio", "transformers", "mlx", "mlx_whisper", "faster_whisper", "silero_vad", "google",
              "anthropic", "spaces", "IPython", "matplotlib", "pytest"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="EMA GUI", console=False, target_arch="arm64")
coll = COLLECT(exe, a.binaries, a.datas, name="EMA GUI")
app = BUNDLE(
    coll,
    name="EMA GUI.app",
    bundle_identifier="com.kaanklcrsln.emagui",
    info_plist={
        "CFBundleDisplayName": "EMA GUI",
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "12.0",
    },
)
