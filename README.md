# BlenderDev

Blender Python tools for VFX and photogrammetry workflows.

## Tools

| Tool | What it does | Blender | Docs |
| --- | --- | --- | --- |
| [Metashape Camera Backgrounds](scripts/metashape_cameras.py) | Puts the undistorted photos from Agisoft Metashape on the matching cameras as background images, in one click. | 3.0+ | [docs/metashape_cameras.md](docs/metashape_cameras.md) |

## Quick start

Every script in `scripts/` is a single, self-contained file.

**Install as an add-on**

1. *Edit > Preferences > Add-ons*.
2. Blender 4.2+: drop-down at the top right > **Install from Disk...**.
   Blender 3.x to 4.1: **Install...**.
3. Pick the `.py` file and tick it to enable it.

**Or run it once** from Blender's **Text Editor** with **Run Script**.

**Or run it headless** (for scripts that do not need the UI):

```bash
blender -b your_file.blend -P scripts/<script>.py
```

Each tool's page in `docs/` has the full instructions.

## Repository layout

```
BlenderDev/
|-- README.md       <- you are here: tool index and quick start
|-- CLAUDE.md       <- conventions for contributors and AI assistants
|-- docs/           <- one Markdown page per tool
|   `-- metashape_cameras.md
|-- scripts/        <- the Blender Python scripts (*.py)
|   `-- metashape_cameras.py
`-- reference/      <- local-only reference docs (git-ignored, not in the repo)
```

## Adding a new tool

1. Put the script in `scripts/<tool_name>.py`.
2. Start the file with a docstring header: purpose, target Blender version,
   how to install and run.
3. Write `docs/<tool_name>.md`. Use
   [`docs/metashape_cameras.md`](docs/metashape_cameras.md) as a template.
4. Add a row to the **Tools** table above.

See [`CLAUDE.md`](CLAUDE.md) for the full conventions.
