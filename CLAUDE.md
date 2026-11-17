# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

**BlenderDev sandbox** - a workspace for building Blender tools and
Python scripts. Active development happens here; reference docs live in
`reference/` (local only).

## Git

- Remote: `https://github.com/phantomvfx/BlenderDev.git`, branch `master`.
- GitHub account: **phantomvfx** (`gh auth switch --user phantomvfx` if another
  account is active).
- Code lives in `scripts/` (`*.py`); each tool has a matching page in `docs/<tool_name>.md`.
- `README.md` holds the tool index - add a row for every new tool.
- `reference/` is git-ignored - never commit doc imports.

## Commands

No build/lint/test toolchain - tools are plain Python scripts run inside Blender.

- `blender -b -P <script.py>` - run a script headless (background, no GUI).
- `blender --python-console` - interactive Python.

If Blender isn't on PATH or behaviour can't be verified, say so rather than
claiming it was tested.

## Blender version targeting

State the target Blender version when starting a tool; if none is stated, ask or
assume the latest installed. Record the target version in the script header.

## Layout

```
L:\BlenderDevSandbox\
|-- CLAUDE.md
|-- README.md
|-- docs/         <- one Markdown page per tool (usage + how it works)
|-- reference/    <- local-only reference docs (git-ignored)
`-- scripts/      <- Blender Python scripts (*.py)
```

## Conventions

- Keep tools self-contained and documented at the top of each file (purpose,
  target Blender version, how to install/run), with full docs in `docs/`.
- Reference docs are pointers only - never copy doc trees into the tracked repo.

