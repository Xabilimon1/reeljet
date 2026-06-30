# ffmpeg recipes

All commands are built by `scripts/lib/ffmpeg_cmd.py`; this is the human map.

## No libass required
Captions are NOT burned with the `subtitles`/`drawtext` filter — many ffmpeg
builds (incl. recent Homebrew bottles) ship without libass/freetype. Instead
`scripts/lib/caption_render.py` draws each caption as a transparent full-frame
PNG with Pillow, and the master step composites them with the always-present
`overlay` filter, timed via `enable='between(t,start,end)'`. Only `overlay`,
`scale`, `pad`, `boxblur`, `libx264`, `aac`, `loudnorm` are needed.

## Master (concat + scale + caption overlays + music + loudnorm)
`build_master_cmd(concat_list, music, overlays, out, w, h, fps)`:
- concat demuxer reads the per-shot clip list;
- `scale=w:h:force_original_aspect_ratio=decrease,pad=w:h:...,setsar=1` brings
  every clip to the master frame (handles varied clip sizes / letterboxing);
- each caption PNG is overlaid for its `between(t,start,end)` window;
- music muxed and normalized `loudnorm=I=-14:TP=-1.5:LRA=11` (social loudness),
  `-shortest`.

## Vertical reframe (16:9 → 9:16)
`build_reframe_cmd()` → blurred-background technique: blurred fill scaled to
cover 1080x1920, original scaled to width, centered overlay. Captions are baked
into the 16:9 master and ride along into the central band of the 9:16 — for
UI-heavy shots prefer zoom-to-active-region; for hero b-roll, generating a
native 9:16 clip in Higgsfield gives the best vertical framing.

## End-card
Generate a 1080-wide logo-on-brand-color still and append as a 3s clip.

## Per-shot inputs
Clips going into the concat list should ideally share fps; the master's
`scale`/`pad` normalizes resolution. If real recordings differ wildly in fps,
normalize first: `-r 30 -c:v libx264 -pix_fmt yuv420p`.
