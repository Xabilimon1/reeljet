# reeljet — Design Spec

- **Date:** 2026-06-30
- **Status:** Approved design → ready for implementation plan
- **Trigger:** `/reeljet`
- **Type:** Claude Code orchestrator skill
- **Repo:** `~/x-brain/Projects/reeljet/` (standalone git repo, ignored by the x-brain vault). Installed by symlink into `~/.claude/skills/reeljet`.

---

## 1. Purpose

Turn **real captures of an app / web / SaaS** (screen recordings + screenshots + logo) into **short promo/demo videos** for social and landing pages. The skill orchestrates creative direction, AI-generated motion, and deterministic assembly into a finished `.mp4`.

The differentiating value is **Phase 1 creative direction** (hook, arc, storyboard, palette, music match), not mechanical clip-stitching.

### Division of labor (hybrid)
- **User provides** (the substance): screen recordings, screenshots, logo of the real product.
- **Higgsfield generates** (the polish): animations, b-roll, transitions/interactions, animated stills (image-to-video), optional generated scenes.
- **Local library provides**: background music (royalty-free), matched to the product/vibe.
- **ffmpeg assembles**: the final deterministic timeline (real clips + generated pieces + music + kinetic captions).

---

## 2. Confirmed decisions

| Topic | Decision |
|---|---|
| UI handling | User supplies real captures/recordings; Higgsfield = music-adjacent motion/animation/interactions, **not** literal UI rendering |
| Final montage | **Auto with ffmpeg** — deterministic timeline, reproducible, no external editor |
| Formats | **Master 16:9 + smart reframe to 9:16** (~1× credits). 16:9 = YouTube/landing hero; 9:16 = Reels/TikTok/Shorts |
| Narrative layer | **On-screen kinetic captions** (no voiceover). Plus: extract **color palette** from assets → caption/accent colors; pick **most fitting music** |
| I/O | **Centralized in x-brain**: `~/x-brain/Projects/<App>/ads/<YYYY-MM-DD>-<campaign>/` |
| Architecture | **Orchestrator + bundled deterministic scripts** + Higgsfield MCP for generation |
| Music source | **Local royalty-free library** at `~/x-brain/Resources/MusicLibrary/`; skill picks best match by mood/BPM/genre |
| Aspect strategy | Generate b-roll once at 16:9; derive 9:16 by smart reframe (UI floating over generated bg, zoom-to-active-region, occasional Higgsfield outpainting) |

---

## 3. Higgsfield MCP — capabilities (grounding)

Confirmed at capability level (exact tool names/params pinned at implementation; see §8 residual):
- Image generation (Soul), image-to-video with motion/camera presets (~5–15s clips), character references, style presets.
- Models available through the MCP: Veo 3.1, Sora 2, Kling 3.0, Seedance 2.0, Wan, MiniMax Hailuo, Soul Cinema, Cinema Studio.
- Aspect ratios **16:9 and 9:16** supported; clips up to ~15s.
- Possible extras (version-dependent): vertical-clip+subtitle cutting, virality score, background removal, image expansion (outpainting), upscaling, "marketing video from URL".
- **Not provided**: dedicated background-music track generation → music comes from the local library. Veo3/Sora2 embedded audio is muted or mixed low per shot.

---

## 4. Pipeline (5 phases)

### Phase 0 — Intake + brand
- Point skill at an asset folder (recordings, screenshots, logo) and capture a short product brief (what it does, audience, USP, tone, CTA).
- `extract_palette.py` → `palette.json` (dominant colors, accent, text-contrast picks) from screenshots + logo.
- `extract_frames.py` (ffmpeg scene-detect) → key frames from recordings (reference + image-to-video seeds).

### Phase 1 — Creative plan  ← **APPROVAL GATE**
- Produce ad concept: hook (first ~2s), narrative arc, CTA, target emotion.
- **Storyboard** in `plan.json` — per shot: `source` (`real_clip` | `higgsfield_broll` | `animated_screenshot`), `duration`, `caption`, `transition`, `motion_preset`, `music_beat`, `aspect_notes`.
- Music brief + chosen track from the local library (`pick_music.py`).
- Palette → caption/accent/lower-third colors.
- **Show estimated Higgsfield credit cost** (N generated shots × model) before any generation.
- **Nothing is generated and no credits are spent until the user approves the plan.**

### Phase 2 — Generation (Higgsfield)
- For each `higgsfield_*` shot: call the appropriate MCP tool (Soul / image-to-video / text-to-video) per storyboard; animate provided screenshots where specified.
- Async: poll for completion, handle failures, download to `generated/`.
- **State tracking + idempotency:** each `plan.json` shot records `status`, `output_path`, `cost`. Re-runs **never regenerate** completed shots. Regenerating one shot = clear that shot's entry.

### Phase 3 — Assembly (ffmpeg)
- `assemble.py` reads `plan.json` and builds the ffmpeg graph:
  - Concatenate real + generated clips with transitions.
  - **Smart reframe** for 9:16: real landscape UI floats over generated background, dynamic zoom to active region, optional outpainting; native generated b-roll where available.
  - Kinetic captions via generated `captions.ass`, styled from `palette.json`.
  - Mix chosen music track; duck/mute embedded clip audio.
  - **Logo end-card / CTA** (logo + optional brand-font caption).
- Render **master 16:9** then derive **9:16**. Output specs: **H.264 / AAC, audio normalized to −14 LUFS**, platform-appropriate fps/duration.

### Phase 4 — QA / iterate
- QA checklist (definition of done): hook legible within 2s; captions inside mobile safe-margins; audio at −14 LUFS; duration within platform limits; codecs correct.
- Optional virality score if the MCP exposes it.
- Present for review; allow regenerating individual shots without rebuilding everything.

---

## 5. Skill structure

```
reeljet/                          # repo root (~/x-brain/Projects/reeljet)
  SKILL.md                        # orchestrates the 5 phases + approval gate
  references/
    creative-direction.md         # hook frameworks, pacing, arc, caption style
    higgsfield-tools.md           # tool map + models + motion/camera presets (filled at impl)
    ffmpeg-recipes.md             # transitions, kinetic captions, smart reframe, audio mix, multi-format
    music-selection.md            # match heuristic mood/BPM/genre
  scripts/
    extract_palette.py            # Pillow → palette.json
    extract_frames.py             # ffmpeg scene-detect → key frames
    pick_music.py                 # choose track from MusicLibrary by brief
    assemble.py                   # plan.json → ffmpeg → master_*.mp4 + captions.ass
  docs/specs/                     # this spec
```

### Output layout (per campaign, in x-brain)
```
~/x-brain/Projects/<App>/ads/<YYYY-MM-DD>-<campaign>/
  brief.md  plan.md  plan.json  palette.json
  frames/  generated/  captions.ass
  master_16x9.mp4  master_9x16.mp4  build.log
```

---

## 6. Prerequisites (one-time setup)

- `brew install ffmpeg` (**required** — assembly + frame extraction). ffmpeg is **not** currently installed.
- Python: anaconda `python3` + **Pillow** (palette). Keep scripts dependency-light (stdlib + Pillow). `librosa` BPM detection is **optional**; default to tag/filename-based BPM.
- Create `~/x-brain/Resources/MusicLibrary/` and populate with royalty-free tracks. Optional sidecar tags (mood/BPM/genre); otherwise `pick_music.py` infers from name/folder. (User is responsible for per-platform music licensing.)
- Higgsfield account with credits (generation costs).
- Symlink `~/x-brain/Projects/reeljet` → `~/.claude/skills/reeljet`; add a pointer line in `~/.claude/CLAUDE.md` (mirrors the graphify pattern).
- The x-brain vault `.gitignore` ignores `Projects/reeljet/` so the nested repo does not pollute the vault.

---

## 7. Design principles

- **Cost control:** hard approval gate + credit estimate before any generation; idempotent regeneration.
- **Reproducibility:** `plan.json` is the single source of truth; assembly is deterministic from it.
- **Progressive disclosure:** lean `SKILL.md`, depth in `references/`.
- **Honesty over hype:** the skill never claims to render the real UI; real footage stays real, generated stays clearly b-roll.

---

## 8. Open / residual items

- **Exact MCP tool names & params** are not loadable this session (claude.ai MCPs load lazily). Pin them at implementation by forcing the MCP to load, then fill `references/higgsfield-tools.md`. The design depends only on confirmed capabilities, not specific names.
- **Beat sync honesty:** captions/cuts align to a **fixed BPM grid** (from tag or estimate) by default; true beat detection is optional and only if `librosa` is present.
- **Vault hygiene:** `master_*.mp4` and `generated/` are git-ignored in output campaigns to avoid bloating the vault; `plan.md` / `brief.md` are versioned.

---

## 9. Out of scope (YAGNI)

- Voiceover / TTS / talking avatars (captions-only for v1).
- AI music generation (local library only).
- Square 1:1 and "one master → auto-crop all platforms" (only 16:9 + 9:16 for v1).
- Workflow fan-out / parallel multi-variant generation (possible future enhancement).
