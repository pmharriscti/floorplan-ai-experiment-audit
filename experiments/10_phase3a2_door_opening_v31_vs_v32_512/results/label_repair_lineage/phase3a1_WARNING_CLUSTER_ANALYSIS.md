# Warning Cluster Analysis

Warnings accounted for: `84`
Unique plans represented: `32`

## Count by cluster

- Family B: border-collapsed localization failure: `37`
- Unresolved: empty seed or unrenderable source instance: `24`
- Family B: false/malformed/mislocalized source instance: `8`
- Family A: door-symbol geometry used as opening seed: `5`
- Family A: seed/wall axis mismatch: `5`
- Family C: low-score plausible seed needs gap-aware association: `3`
- Family C: plausible opening rejected by host-wall association: `2`

## Count by plan

- high_quality_architectural/14483: `10`
- high_quality_architectural/11814: `6`
- high_quality_architectural/3612: `6`
- high_quality_architectural/555: `6`
- high_quality_architectural/8002: `5`
- high_quality_architectural/20107: `4`
- high_quality_architectural/4884: `4`
- high_quality_architectural/7677: `4`
- high_quality_architectural/11709: `3`
- colorful/1077: `3`
- high_quality_architectural/1227: `3`
- high_quality_architectural/7029: `3`
- high_quality_architectural/3501: `3`
- high_quality_architectural/13110: `2`
- high_quality_architectural/14817: `2`
- colorful/11400: `2`
- high_quality/3776: `2`
- colorful/9192: `2`
- high_quality_architectural/10543: `1`
- high_quality_architectural/10620: `1`
- high_quality_architectural/13827: `1`
- high_quality_architectural/14814: `1`
- high_quality_architectural/8690: `1`
- high_quality_architectural/11348: `1`
- high_quality_architectural/12404: `1`
- high_quality_architectural/1757: `1`
- high_quality_architectural/5625: `1`
- colorful/13181: `1`
- high_quality_architectural/12234: `1`
- high_quality_architectural/1193: `1`
- high_quality_architectural/4722: `1`
- high_quality_architectural/6697: `1`

## Count by door/window

- door_opening: `43`
- window_opening: `41`

## Count by review reason

- no wall component intersects or lies near the opening seed: `35`
- opening seed is empty: `24`
- opening seed does not sufficiently overlap a structural wall component: `13`
- multiple nearby wall components have similar association scores: `12`

Empty seeds: `24`
Border-collapsed bboxes: `44`
Seed/wall orientation mismatches: `58`
Plausible seeds rejected by association: `5`

## Representatives

### Family A: door-symbol geometry used as opening seed
- `high_quality_architectural/10543 / door_0003 / door_opening`: door seed follows vertical door leaf; host wall is horizontal
- `high_quality_architectural/10620 / door_0005 / door_opening`: door seed follows horizontal symbol geometry; host wall is vertical
- `high_quality_architectural/11709 / door_0012 / door_opening`: door seed follows vertical door leaf; host wall is horizontal
- `high_quality_architectural/11709 / door_0013 / door_opening`: door seed follows vertical door leaf; host wall is horizontal
- `high_quality_architectural/11709 / door_0014 / door_opening`: door seed follows vertical door leaf; host wall is horizontal

### Family A: seed/wall axis mismatch
- `high_quality_architectural/13110 / door_0006 / door_opening`: door seed long axis is inconsistent with host-wall tangent
- `high_quality_architectural/13827 / door_0004 / door_opening`: door seed long axis is inconsistent with host-wall tangent
- `high_quality_architectural/14814 / door_0007 / door_opening`: door seed long axis is inconsistent with host-wall tangent
- `high_quality_architectural/14817 / door_0008 / door_opening`: door seed long axis is inconsistent with host-wall tangent
- `high_quality_architectural/8690 / door_0005 / door_opening`: door seed long axis is inconsistent with host-wall tangent

### Family B: false/malformed/mislocalized source instance
- `colorful/1077 / door_0007 / door_opening`: opening span is in annotation or margin space
- `colorful/11400 / window_0007 / window_opening`: human-confirmed false window instance
- `high_quality/3776 / window_0000 / window_opening`: bbox collapsed at right image boundary
- `high_quality_architectural/11348 / door_0002 / door_opening`: no recognizable door at highlighted location; source requires review
- `high_quality_architectural/11814 / door_0021 / door_opening`: bbox collapsed at bottom image boundary
- `high_quality_architectural/11814 / door_0022 / door_opening`: bbox collapsed at bottom image boundary
- `high_quality_architectural/11814 / door_0024 / door_opening`: bbox collapsed at bottom image boundary
- `high_quality_architectural/11814 / door_0025 / door_opening`: bbox collapsed at bottom image boundary

### Family B: border-collapsed localization failure
- `colorful/1077 / window_0004 / window_opening`: bbox touches image border and collapses to one raster row or column
- `colorful/1077 / window_0005 / window_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality/3776 / window_0001 / window_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality_architectural/11814 / window_0031 / window_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality_architectural/11814 / window_0032 / window_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality_architectural/1227 / door_0017 / door_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality_architectural/1227 / window_0015 / window_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality_architectural/1227 / window_0016 / window_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality_architectural/12404 / door_0032 / door_opening`: bbox touches image border and collapses to one raster row or column
- `high_quality_architectural/14483 / door_0014 / door_opening`: bbox touches image border and collapses to one raster row or column

### Family C: plausible opening rejected by host-wall association
- `colorful/11400 / door_0002 / door_opening`: genuine opening rejected by wall association
- `colorful/13181 / door_0003 / door_opening`: genuine opening rejected by wall association

### Family C: low-score plausible seed needs gap-aware association
- `high_quality_architectural/12234 / door_0004 / door_opening`: nonempty seed with near-zero association score
- `high_quality_architectural/13110 / window_0005 / window_opening`: nonempty seed with near-zero association score
- `high_quality_architectural/14817 / window_0008 / window_opening`: nonempty seed with near-zero association score

### Unresolved: empty seed or unrenderable source instance
- `colorful/9192 / door_0007 / door_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `colorful/9192 / window_0003 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/1193 / window_0000 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/3501 / window_0007 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/3501 / window_0008 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/3501 / window_0009 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/3612 / window_0016 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/3612 / window_0017 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/3612 / window_0018 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted
- `high_quality_architectural/3612 / window_0019 / window_opening`: seed_pixels is zero; source SVG instance must be highlighted

## Human-reviewed examples mapped to clusters

- `colorful/1077 / door_0007 / door_opening` -> `Family B: false/malformed/mislocalized source instance`
- `colorful/11400 / door_0002 / door_opening` -> `Family C: plausible opening rejected by host-wall association`
- `colorful/11400 / window_0007 / window_opening` -> `Family B: false/malformed/mislocalized source instance`
- `colorful/13181 / door_0003 / door_opening` -> `Family C: plausible opening rejected by host-wall association`
- `colorful/9192 / door_0007 / door_opening` -> `Unresolved: empty seed or unrenderable source instance`
- `high_quality/3776 / window_0000 / window_opening` -> `Family B: false/malformed/mislocalized source instance`
- `high_quality_architectural/10543 / door_0003 / door_opening` -> `Family A: door-symbol geometry used as opening seed`
- `high_quality_architectural/10620 / door_0005 / door_opening` -> `Family A: door-symbol geometry used as opening seed`
- `high_quality_architectural/11348 / door_0002 / door_opening` -> `Family B: false/malformed/mislocalized source instance`
- `high_quality_architectural/11709 / door_0012 / door_opening` -> `Family A: door-symbol geometry used as opening seed`
- `high_quality_architectural/11709 / door_0013 / door_opening` -> `Family A: door-symbol geometry used as opening seed`
- `high_quality_architectural/11709 / door_0014 / door_opening` -> `Family A: door-symbol geometry used as opening seed`
- `high_quality_architectural/11814 / door_0021 / door_opening` -> `Family B: false/malformed/mislocalized source instance`
- `high_quality_architectural/11814 / door_0022 / door_opening` -> `Family B: false/malformed/mislocalized source instance`
- `high_quality_architectural/11814 / door_0024 / door_opening` -> `Family B: false/malformed/mislocalized source instance`
- `high_quality_architectural/11814 / door_0025 / door_opening` -> `Family B: false/malformed/mislocalized source instance`
- `high_quality_architectural/6697 / window_0022 / window_opening` -> `Unresolved: empty seed or unrenderable source instance`

No warnings were forced into the three known families; empty seeds and other low-evidence rows remain unresolved/other buckets.
