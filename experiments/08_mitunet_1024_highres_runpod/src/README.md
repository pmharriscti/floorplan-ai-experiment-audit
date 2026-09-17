# Fast1024 Source Availability

The exact cloud runner package was recorded at `/workspace/fast1024.zip` and extracted at `/root/fast1024`, but it was not present in the supplied local archive or source tree. The audit therefore does not substitute reconstructed files for `run.sh`, `io_utils.py`, `prepare.py`, or `train.py`.

The original [PROVENANCE.json](../source_provenance/PROVENANCE.json) retains SHA-256 values for `io_utils.py`, `prepare.py`, `train.py`, and all scientific modules imported by the runner. All 15 listed files under `mitunet_cubicasa/` and `study/core.py` match the local repository `/home/pmharris/dev/mitunet_uniform_1024_crop` byte-for-byte.

The local repository is at origin commit `6e55b50ab1cf8be9a40eb82efbb8a22b28c8f3c7`. The user-supplied summary reports that later cloud runtime repair commit `10907a7f6dafcad62a024f12c69b4383586f009d` existed on RunPod; that commit is not present in the local repository.

To complete this source bundle exactly, retrieve the original `fast1024.zip` from the RunPod persistent volume and verify each runner file against the hashes in the preserved provenance before committing it.
