# Higgsfield MCP — tool contract

Source verified 2026-06-30 via the community unified server README
(`github.com/Hikhakk/higgsfield-mcp-unified`), which mirrors the hosted
`mcp.higgsfield.ai` surface. The live MCP tool schemas did not load into this
session's tool index, so **confirm names at runtime** before generating:
call `preflight_check` and `list_models` first; if a tool name differs from
below, trust the live MCP and adjust.

## Tools

| Tool | Key params | Use in reeljet |
|------|-----------|----------------|
| `preflight_check` | — | First call. Auth + reachability. |
| `list_models` / `recommend_model` | `kind`, `intent`, `top` | Discover/choose model id per shot. |
| `get_balance` | — | **Cost gate**: read credits before + after generation. |
| `validate_params` | `model_id`, `params` | Sanity-check params before submit. |
| `upload_image` | `path` \| `data_base64` | Host a screenshot / key frame → URL. |
| `generate_image` | `model_id`, `prompt`, `soul_id?` | Stills, end-card art, seeds. |
| `generate_video` | `model_id`, `prompt`, `image_url?` | **Core.** With `image_url` = image-to-video; without = text-to-video. |
| `generate_batch` | `requests[]` | Submit several shots at once. |
| `get_status` / `subscribe` | `job_handle` | Poll / long-poll until the clip URL is ready. |
| `cancel_job` | `job_handle` | Abort a bad/queued job. |
| `list_motions` / `list_soul_styles` | — | Motion/camera + style presets to fill `motion_preset`. |
| `create_character` / `list_characters` | varies | Optional: consistent recurring character. |
| `list_jobs` | `page` | Generation history. |
| `generate_speech_video` | `image_url`, `audio_url` | Talking-head — **out of scope for v1** (captions-only). |

## Models (by backend)
- **Official API (verified):** Soul, Reve, Seedream v4, FLUX.1 Kontext Max, DOP,
  Seedance v1 Pro, Kling v2.1 Pro.
- **Cloud web backend:** Kling 3.0, Seedance 2.0, Wan 2.6, Veo 3 / 3.1, Sora 2,
  Nano Banana, Soul v2.
- Pick via `recommend_model` with the shot intent; prefer the official-API
  models when available (more stable). Aspect ratio (16:9 master, 9:16 hero
  only) and duration are per-model params — read them from `list_models` /
  `validate_params`, do not hardcode.

## Mapping: storyboard source → tool
- `real_clip` → **no Higgsfield** (user footage; just normalize + concat).
- `animated_screenshot` → `upload_image`(screenshot) → `generate_video`
  (`model_id`, `image_url`, `prompt`, motion preset) → `subscribe` → download.
- `higgsfield_broll` → `generate_video` text-to-video (omit `image_url`), or
  `upload_image`(key frame) → `generate_video` from it.

## Generation loop (Phase 2)
1. `preflight_check`; read `get_balance` (record starting credits).
2. For each shot with `status != "done"`: submit `generate_video`
   (or `generate_image` for end-card), `subscribe`/`get_status` until ready.
3. Download the result into `<campaign>/generated/`, set the shot's
   `output_path`, `status: "done"`, and `cost` in plan.json. Idempotent:
   never resubmit a shot already `done`.
4. After the batch, read `get_balance` again; record total spent.

## Cost — surface at the Phase 1 gate
Before generating, estimate total = sum over generated shots of the model's
per-clip credit cost (from `list_models` / pricing). Show the estimate at the
approval gate. Never generate before the user approves the spend.
