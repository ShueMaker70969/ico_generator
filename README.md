# PNG to ICO Generator

A small Python desktop app that converts a single PNG image into a multi-size ICO file.

## Setup

Honestly, not much to be said. Run this in any environment that has pillow. Run the main.py, and the app should launch. 

## Run

```powershell
python main.py
```
...really, that's it.

## Usage

1. Click **Browse...** and choose a `.png` image.
2. Choose the output `.ico` path, or keep the default next to the PNG.
3. Select the icon sizes to include.
4. Click **Convert**.

The app preserves PNG transparency and writes one `.ico` file containing the selected sizes.
Easiest way to use, is to prepare one png file with transparent background, 256*256 size, then browse and select that image. For the icon sizes to include, simply include every possible size.