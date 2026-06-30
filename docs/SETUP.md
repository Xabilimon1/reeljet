# reeljet setup

1. `brew install ffmpeg`  (required: assembly + frame extraction)
2. Python deps (anaconda usually has them): `python3 -m pip install pillow pytest`
3. Create the music library and add royalty-free tracks:
   `mkdir -p ~/x-brain/Resources/MusicLibrary`
   Name files with hints, e.g. `uplifting_120bpm_corporate.mp3` (mood / bpm / genre).
4. Install the skill (Task 12): symlink this repo into `~/.claude/skills/reeljet`.

Outputs per campaign go to:
`~/x-brain/Projects/<App>/ads/<YYYY-MM-DD>-<campaign>/`
