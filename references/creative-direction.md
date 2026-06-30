# Creative direction

The job: in <30s, make a viewer understand and want the product.

## Hook (first ~2s)
Open on the single most striking moment: the outcome, the "wow" screen, or a
bold claim caption. Never open on a logo or a slow fade.
Hook patterns: Problem→agitate, Result-first, "What if…", Bold number/claim.

## Arc (15–30s)
1. Hook (0–2s) — striking outcome + claim caption.
2. Tension (2–8s) — the problem / the old painful way.
3. Reveal (8–20s) — the product doing the thing (real UI clips, animated).
4. Proof (20–26s) — a metric, a second feature, social proof caption.
5. CTA end-card (26–30s) — logo + one action ("Try <name> free").

## Per-shot storyboard fields (-> plan.json shots[])
id, source (real_clip|higgsfield_broll|animated_screenshot), asset,
duration, caption, transition (cut|crossfade|whip|none), motion_preset,
music_beat, aspect_notes.

## Caption style
Short (≤6 words), present tense, benefit-led. One idea per shot. Colors come
from palette.json (caption_fill/outline). Keep inside mobile safe margins.

## Pacing
Cut on the beat grid (see music-selection). Faster cuts in hook + proof,
slightly longer on the reveal so the UI is readable.
