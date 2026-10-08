# Visual QA - bim_bridge PM comparison

Six reduced review images (resized, JPEG). Full-size sources stay on the external drive; paths and hashes are in [metadata.json](metadata.json).

| File | Content |
| --- | --- |
| [comparison_sheet_r04_after_repair.jpg](comparison_sheet_r04_after_repair.jpg) | All 15 plans after the bridge repair (r04): source, model masks, masks vs labels, IFC walls vs labels, IFC plan read from the file |
| [comparison_sheet_r01_before_repair.jpg](comparison_sheet_r01_before_repair.jpg) | The same 15 plans before the repair (r01) |
| [com-03_clinic_r01_vs_r04.jpg](com-03_clinic_r01_vs_r04.jpg) | One plan in detail: IFC before and after repair, in plan and in 3D |
| [comparison_sheet_r05_windows.jpg](comparison_sheet_r05_windows.jpg) | All 15 plans at revision r05 (2026-10-08): window apertures exported; panel 5 shows door voids magenta, window voids cyan |
| [cc-01_r04_vs_r05.jpg](cc-01_r04_vs_r05.jpg) | CubiCasa 4712: the r04 row above the r05 row |
| [com-06_r04_vs_r05.jpg](com-06_r04_vs_r05.jpg) | Manufacturing plan, the one with the most windows: r04 above r05 |

Colours in the "vs labels" panels: green correct, red extra, blue missed, orange = label ignore region.

**Labels.** CubiCasa rows use the dataset's labels. AI-generated rows use draft labels made by an AI assistant and not reviewed by a person.

**3D panels.** The r01 panel is the user's screenshot of the local viewer; the r04 panel is an automated headless render of the same viewer. Neither is a recorded viewer inspection.
