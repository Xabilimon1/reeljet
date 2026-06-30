# reeljet

Claude Code orchestrator skill that turns **real captures of an app / web / SaaS** (screen recordings, screenshots, logo) into **short promo/demo videos** for social and landing pages.

- You provide the real footage; **Higgsfield** generates animations / b-roll / transitions; a **local royalty-free library** provides music; **ffmpeg** assembles the final `.mp4`.
- Outputs **master 16:9** + smart-reframed **9:16**, with kinetic captions colored from the product's extracted palette.
- Trigger: `/reeljet`

See [`docs/specs/2026-06-30-reeljet-design.md`](docs/specs/2026-06-30-reeljet-design.md) for the full design and [`docs/plans/2026-06-30-reeljet.md`](docs/plans/2026-06-30-reeljet.md) for the implementation plan.

## Requirements
- `ffmpeg` (`brew install ffmpeg`) — libass **not** required; captions are drawn with Pillow and composited via the `overlay` filter.
- Python 3 with `pillow` (and `pytest` for the tests).
- The [Higgsfield](https://higgsfield.ai) MCP connected to your agent, with credits.
- A local folder of royalty-free music tracks (see `references/music-selection.md`).

## Install (as a Claude Code skill)
```bash
ln -snf "$PWD" ~/.claude/skills/reeljet
```
Then trigger with `/reeljet`. See [`docs/SETUP.md`](docs/SETUP.md).

## Tests
```bash
python3 -m pytest        # 29 passing
```

## Status
v1 built — deterministic scripts (palette, music match, captions, ffmpeg assembly, plan validation) are unit-tested; Higgsfield generation is agent-driven at runtime via MCP.

## License
[MIT](LICENSE) © 2026 Xabier Ariznabarreta
