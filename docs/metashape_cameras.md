# Metashape Camera Backgrounds

**Script:** [`scripts/metashape_cameras.py`](../scripts/metashape_cameras.py)
**Type:** Blender add-on (single file)
**Target Blender:** 3.0 and later (written for 3.x / 4.x)
**UI location:** 3D Viewport > Sidebar (`N`) > **Metashape** tab

Assigns the undistorted photos from an Agisoft Metashape project as background
images on the matching cameras in your Blender scene. Look through any camera
and you see the original photo behind your geometry - handy for checking an
alignment, modelling against the photos, or projection work.

---

## Contents

- [What it does](#what-it-does)
- [Before you start](#before-you-start)
- [Install](#install)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Name matching rules](#name-matching-rules)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)

---

## What it does

With one click, for every camera in the scene, the add-on:

1. Looks for an image in a chosen folder whose file name (without extension)
   is the same as the camera's name.
2. Loads that image into Blender.
3. Replaces the camera's background images with it.
4. Sets the background to **Crop** framing and applies the scale you chose.

At the end it reports how many cameras were updated.

---

## Before you start

You need two things from Metashape:

| What | Why |
| --- | --- |
| **Cameras in Blender**, for example from an FBX or Alembic export of the aligned cameras | These are the cameras the images are attached to. |
| **A folder of undistorted photos** (Metashape: *Export > Undistort Photos*) | Blender cameras are perfect pinhole cameras with no lens distortion. Only undistorted images line up with them. The original, distorted photos will drift away from your geometry towards the edges of the frame. |

Keep the undistorted file names the same as the photo names. Metashape names
the cameras after the photos, so the names line up. See
[Name matching rules](#name-matching-rules).

---

## Install

### As an add-on (recommended)

1. *Edit > Preferences > Add-ons*.
2. Blender 4.2 and later: open the drop-down arrow at the top right and choose
   **Install from Disk...**. Blender 3.x to 4.1: click **Install...**.
3. Select `metashape_cameras.py`.
4. Tick **Metashape Camera Backgrounds** to enable it.

The panel stays available in every Blender session.

### One-off, from the Text Editor

1. Open `metashape_cameras.py` in Blender's **Text Editor**.
2. Click **Run Script**.

The panel appears for this session only. Running the script again is safe: it
unregisters the old version first.

---

## Usage

1. Import or open the scene that holds the Metashape cameras.
2. In the 3D Viewport press `N` and open the **Metashape** tab.
3. **1. Select Undistorted Images:** choose the folder with the undistorted
   photos.
4. **2. Master Scale:** leave this at `1.0` to start. See below.
5. Click **Apply to All Cameras**.
6. Look through a camera (select it, then `Ctrl` + `Numpad 0`) to check the
   result.

The status bar shows `Success! Assigned to N cameras at X scale.` Cameras that
had no matching image are listed in the system console
(*Window > Toggle System Console* on Windows, or the terminal Blender was
started from on macOS and Linux).

The operation supports **Undo** (`Ctrl` + `Z`).

### The Master Scale value

Scale is applied to every camera's background image. Use it when the photos do
not quite fill the camera frame. A common cause is that the undistorted images
are a slightly different size or aspect ratio from the camera's sensor setup.
Adjust the value and click **Apply to All Cameras** again: every camera is
rebuilt with the new scale. The field keeps five decimal places, for fine
adjustments.

---

## How it works

The file defines three things.

### 1. Two scene settings

Stored on the scene, so they are saved with your `.blend` file:

| Property | Type | Default | Purpose |
| --- | --- | --- | --- |
| `scene.ms_image_dir` | Folder path | empty | Folder with the undistorted images. Relative paths (`//images/`) work. |
| `scene.ms_image_scale` | Float, 5 decimals | `1.0` | Scale applied to each background image. |

### 2. The operator: `object.assign_camera_images`

This is what **Apply to All Cameras** runs. Step by step:

1. **Resolve the folder.** Converts a relative Blender path to an absolute one.
   If the folder does not exist, it stops with an error.
2. **Index the folder.** Lists every file (sub-folders are ignored) and builds
   a lookup of *file name without extension -> full path*. So `IMG_0042.jpg`
   becomes the key `IMG_0042`.
3. **Walk the cameras.** For every object in the current scene of type
   *Camera*, it reads the name of the camera **data** (not the object's name;
   see below) and looks it up.
4. **On a match:**
   - loads the image, reusing it if it is already loaded
     (`check_existing=True`), so running the tool again creates no duplicates;
   - turns on *Background Images* for the camera;
   - **removes every existing background image** on that camera;
   - adds the new image with **Frame Method = Crop** and the chosen scale.
5. **On no match:** prints a warning to the console and leaves the camera
   unchanged.
6. **Report.** Shows how many cameras were updated.

### 3. The panel: `VIEW3D_PT_metashape_cameras`

Draws the folder field, the scale field and the button in the **Metashape**
sidebar tab.

---

## Name matching rules

This is where most problems come from, so it is worth knowing exactly.

- The match uses the camera **data** name: the name with the green camera icon
  in the Outliner, under the object. It does **not** use the object name.
  Importers usually give both the same name, but if you rename a camera object
  in Blender, the data name stays the same and the data name is what counts.
- The match is **exact and case-sensitive**. `IMG_0042` does not match
  `img_0042`, `IMG_0042.001` or `IMG_0042_undist`.
- The file extension is ignored, and any file type is used. Keep only images
  in the folder.
- If two files share a name with different extensions (`IMG_0042.jpg` and
  `IMG_0042.tif`), only one of them is used, and which one is not guaranteed.

---

## Troubleshooting

| Symptom | Likely cause and fix |
| --- | --- |
| "Selected folder does not exist." | The path is empty or wrong. Choose the folder again with the folder button. |
| "Assigned to 0 cameras" | Names do not match. Compare a camera's **data** name in the Outliner with a file name in the folder. Look for a different case, an added suffix, or Blender's `.001`. |
| Some cameras updated, others not | Check the console for `Warning: No matching image found for '...'` and fix those names. |
| Image is updated but I can't see it | You are not looking through the camera. Press `Numpad 0`. Also check *Overlays > Camera Background* is not turned off (Blender 4.x and later), and the background image's opacity. |
| Image does not line up at the edges | You are using the original, distorted photos. Export undistorted photos from Metashape. |
| Image is slightly too big or small | Adjust **Master Scale** and apply again. |
| Existing background images vanished | This is expected. The tool clears all background images on every camera it matches. |

---

## Limitations

- Only cameras in the **current scene** are processed.
- All existing background images are **replaced**, not added to, on matched
  cameras.
- Each camera gets a single still image. Image sequences and movie clips are
  not set up.
- One scale value for all cameras. There is no per-camera setting in the panel,
  but you can change any single camera afterwards in
  *Camera Properties > Background Images*.
- Only tested by hand in Blender's UI. There is no automated test.
