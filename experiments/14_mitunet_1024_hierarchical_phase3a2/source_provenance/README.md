# Source Evidence Snapshots

- [source_inventory.json](source_inventory.json) records 76 inspected source/config/test files across `/home/pmharris/dev/mitunet`, `/home/pmharris/dev/mitunet_multihead` and `/home/pmharris/dev/mitunet_phase3a2_512`, plus parent audit records. Each entry contains its path, byte count and SHA-256.
- [contracts/](contracts/) contains five byte-identical YAML copies from the inspected `mitunet/configs/targets` directory: the target contract, v3 mapping, opening derivation, fixture mapping and source taxonomy.
- [phase3a2_repair_scope.json](phase3a2_repair_scope.json) preserves the ten explicit Family A keys and their split identities, extracted from the live opening manifest without copying review decisions or notes.

These contracts describe the local source policies at inspection. The experiment-14 [config](../config.yaml) declares the proposed 1024 adaptations and repair overrides; copying a historical contract does not make it the complete resolved training configuration.

Refresh these snapshots with `python3 scripts/build_experiment14_evidence.py` from the audit repository only when intentionally updating the documented source identities. The helper reads the scientific source trees and writes only this entry's evidence snapshots. An altered repair-scope count requires review before refresh. It does not generate labels, train models, save human decisions or copy datasets/checkpoints.
