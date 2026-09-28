# Viewer inspection steps (gate G7)

Status: **NOT_RUN**. Nobody has opened this file in a viewer. This page tells a person how to do it and
what to record. Do not fill in the record on someone else's behalf.

File to open: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_preview/cubicasa-high-quality-architectural-333-val-region-01__PREVIEW_CANDIDATE_UNREVIEWED.ifc`

This file is a **preview of unreviewed candidate geometry**. Its plan scale is an assumption.

1. Open the file in the target BIM application, or in an IFC viewer such as Bonsai (Blender), BIMvision,
   Solibri Anywhere or an online IFC viewer. Record the application name and version.
2. Confirm the file opens without an import error. Copy any warning text.
3. Confirm the spatial tree shows Project > Site > Building > Storey, and that the storey contains
   4 walls.
4. Select each wall on its own. Confirm it is a separate, selectable `IfcWall` with its own GlobalId, and
   compare the GlobalId with `guid_map.json`.
5. Confirm the wall hosting the aperture shows a hole through its full thickness at the expected place, and
   that the `IfcOpeningElement` is related to that wall.
6. Open the property set `AutoAutoCAD_Provenance` on one wall. Confirm you can read `ReviewState`,
   `SemanticScoreAvailability`, `ThicknessOrigin`, `HeightIsAssumption`, `ScaleStatus` and `SourceReferences`.
7. Measure one wall length in the viewer and compare it with `CentrelineLength` in the property set.
8. Save a screenshot of the model and one of the property panel.
9. Copy `viewer_inspection_record_TEMPLATE.json` to `viewer_inspection_record.json` in the same folder
   and fill it in. Re-run `bim-bridge finalize --run-dir <run>`; gate G7 then reads your record.

A local viewer check and acceptance by the target application are different results. Record which one you did.
