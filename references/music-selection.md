# Music selection

Source: local royalty-free library at `~/x-brain/Resources/MusicLibrary/`.
Higgsfield does not produce a dedicated track; embedded clip audio is muted
or mixed low.

## Brief → track
Derive a brief from the product tone: mood (uplifting/energetic/calm/epic/
corporate/...), target BPM, keywords. Run:
`python3 scripts/pick_music.py --mood energetic --bpm 128 --keywords corporate`
It scans the library, parses mood/BPM from filenames
(e.g. `energetic_128bpm_corporate.mp3`), scores, prints the best path.

## BPM grid (beat sync)
Default: cut on a fixed grid derived from the chosen track's BPM
(beat seconds = 60 / bpm). Set each shot duration to a whole number of beats.
True onset detection is optional and only if `librosa` is installed.

## Naming convention for the library
`<mood>_<bpm>bpm_<genre>.<ext>` — e.g. `uplifting_120bpm_corporate.mp3`.
