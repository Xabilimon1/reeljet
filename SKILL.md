---
name: reeljet
description: Use when the user wants to create a short promo or demo video (Reels/TikTok/Shorts/landing hero) for an app, web, or SaaS from their own screen recordings and screenshots. Orchestrates creative direction, Higgsfield-generated motion/b-roll, local music, and deterministic ffmpeg assembly into master 16:9 + 9:16. Trigger: /reeljet.
---

# reeljet

Turn real product captures into short promo videos. You provide the substance
(recordings, screenshots, logo); Higgsfield adds motion/b-roll; a local library
adds music; ffmpeg assembles the final cut.

## Prerequisites
- ffmpeg installed (`brew install ffmpeg`).
- `~/x-brain/Resources/MusicLibrary/` populated (see references/music-selection.md).
- Higgsfield MCP connected with credits.

## Workflow (5 phases)

### Phase 0 — Intake + brand
1. Get the asset folder (recordings, screenshots, logo) + a short brief
   (what it does, audience, USP, tone, CTA).
2. Create the campaign dir:
   `~/x-brain/Projects/<App>/ads/<YYYY-MM-DD>-<campaign>/`.
3. `python3 scripts/extract_palette.py --assets <assets> --out <camp>/palette.json`
4. `python3 scripts/extract_frames.py --video <recording> --out <camp>/frames`

### Phase 1 — Creative plan  (APPROVAL GATE)
Read references/creative-direction.md. Write `<camp>/plan.json` (validated by
scripts/lib/plan_schema.py) and a human `<camp>/plan.md` storyboard.
Pick music: `python3 scripts/pick_music.py --mood ... --bpm ... --keywords ...`.
Set shot durations to whole beats (60/bpm). Compute and show the **estimated
Higgsfield credit cost** (sum per generated shot, see references/higgsfield-tools.md).
**STOP. Present plan.md + cost. Do not generate until the user approves.**

### Phase 2 — Generation (Higgsfield)
For each shot with source `higgsfield_broll` or `animated_screenshot`, call the
MCP tool per references/higgsfield-tools.md. Skip shots already `status: done`
(idempotent — never re-spend credits). Download into `<camp>/generated/`,
set `output_path`, `status`, `cost` in plan.json. Normalize every clip to
1920x1080@30 (references/ffmpeg-recipes.md) before assembly.

### Phase 3 — Assembly (ffmpeg)
`python3 scripts/assemble.py --campaign-dir <camp>`
Produces `master_16x9.mp4` and reframed `master_9x16.mp4`, captions burned from
palette, music mixed at -14 LUFS. Append the logo end-card/CTA.

### Phase 4 — QA / iterate
Check: hook readable in 2s; captions in mobile safe margins; audio -14 LUFS;
duration within platform limits; H.264/AAC. To redo one shot, clear its
plan.json entry (status->pending, drop output_path) and re-run Phase 2 + 3.

## References
- references/creative-direction.md — hooks, arc, caption style.
- references/higgsfield-tools.md — exact MCP tools, presets, models, cost.
- references/ffmpeg-recipes.md — normalization, master, reframe, end-card.
- references/music-selection.md — library, brief->track, BPM grid.
