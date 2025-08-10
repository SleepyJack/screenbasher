# Screenbasher

Screenbasher is a simple game I wrote for my toddler. It opens a full ‑‑screen window and lets children mash the keyboard or move/click the mouse to draw colourful circles and rectangles that fade over time. System keys like the Windows and Escape keys are blocked so your little one can't accidentally close the app or switch programs. To exit the game yourself, press **Ctrl+C** (or hold Left Ctrl and press `c`) in the console or inside the game window.

## How it works

- Uses [pygame](https://www.pygame.org) to create a full ‑‑screen window, hide the mouse cursor and draw random shapes in response to key presses and mouse events.
- Uses the [keyboard](https://pypi.org/project/keyboard/) module to block system keys and allow safe exit via `Ctrl+C`.
- Shapes fade gradually by decreasing their colour values until they disappear, keeping the screen lively.

## Releases

This repository includes a GitHub Actions workflow (`.github/workflows/build_and_release.yml`) that automatically builds a Windows executable using [PyInstaller](https://www.pyinstaller.org) and publishes it as a release.

The workflow runs on every push and on tags that start with `v*.*.*`. When you push a tag like `v1.2.0`, the workflow will:

1. Extract a version string from the tag or commit SHA and update `version_string` in `screenbasher.py`.
2. Install dependencies from `requirements.txt`.
3. Build a standalone `screenbasher.exe` using PyInstaller, rename it to include the version string and upload it as a build artifact.
4. If the push is a version tag, create a GitHub Release and attach the executable.

You can download prebuilt Windows binaries from the [Releases](../../releases) page. To run from source, install the dependencies and start the script:

```
pip install -r requirements.txt
python screenbasher.py
```

## Controls

- Mash any keys to spawn shapes in random colours.
- Move the mouse to leave a trail of red circles; left ‑‑click creates a large green circle; right ‑‑click creates a large blue circle.
- Exit the game using **Ctrl+C** or by holding **Left Ctrl** + `c`.
