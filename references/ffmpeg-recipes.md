# ffmpeg recipes

All commands are built by `scripts/lib/ffmpeg_cmd.py`; this is the human map.

## Per-shot normalization (before concat)
Every clip going into the concat list MUST share codec/fps/resolution.
Normalize each to 1920x1080@30, yuv420p:
`ffmpeg -y -i IN -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1" -r 30 -c:v libx264 -pix_fmt yuv420p OUT`

## Master (concat + captions + music + loudnorm)
`build_master_cmd()` → concat demuxer, burn `captions.ass`, mux music,
`loudnorm=I=-14:TP=-1.5:LRA=11` (social loudness), `-shortest`.

## Vertical reframe (16:9 → 9:16)
`build_reframe_cmd()` → blurred-background technique: blurred fill scaled to
cover 1080x1920, original scaled to width, centered overlay. For UI-heavy
shots prefer zoom-to-active-region; for generated b-roll prefer native 9:16
generation (re-run Higgsfield at 9:16 only for the hero shot if budget allows).

## End-card
Generate a 1080-wide logo-on-brand-color still and append as a 3s clip.
