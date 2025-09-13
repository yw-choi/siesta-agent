# Graphene example

This directory contains a minimal monolayer graphene primitive cell for SIESTA.

Files:
- `graphene.xyz`: Structure (Angstrom) with lattice vectors embedded in the comment line.
- `relax.fdf`: Generated input for in-plane relaxation (cell vectors fixed, atomic positions relaxed).

To regenerate `relax.fdf`:
```bash
python3 tools/build_fdf.py \
  --structure examples/graphene/graphene.xyz \
  --pseudodb examples/pseudopotentials/map.json \
  --calc relax \
  --k 24,24,1 \
  --mesh 250 \
  --basis DZP \
  --label graphene_relax \
  --out examples/graphene/relax.fdf
```
