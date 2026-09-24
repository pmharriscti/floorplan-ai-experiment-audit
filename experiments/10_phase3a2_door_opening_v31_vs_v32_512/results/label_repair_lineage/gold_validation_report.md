# Gold Validation Report

Status: `BLOCKED_PENDING_VALIDATION_GOLD_REVIEW`

- Canonical validation plans compared: `400`
- Changed validation plans: `1`
- Changed validation instances requiring review: `1`
- Stratified unchanged instances queued: `48`
- Vanished-at-512 positive instances forced into queue: `1`
- Queue size: `49`

Candidate left/right order is seeded and randomized per queue item. The reviewer-facing queue and overlays contain only blind asset paths; the version key is isolated under `private/` and is not read by the review UI.

The queue includes source floorplan, source SVG instance, door leaf/swing evidence, host wall, jambs, both candidates, and a difference panel. It includes every changed validation instance plus a deterministic stratified audit across orientation, association confidence, opening size, and plan density. The shared vanished-positive instance is mandatory.

No gold masks are frozen and training is prohibited until every queue row is resolved without conflict. If the vanished source instance is confirmed valid, the next gate must report `BLOCKED_512_TARGET_SURVIVABILITY_FAILURE`.

Launch the blinded review UI:

```bash
cd /home/pmharris/dev/mitunet_phase3a2_512
/home/pmharris/dev/mitunet/.venv/bin/python scripts/review_validation_gold.py --reviewer "$USER" --host 127.0.0.1 --port 7895
```
