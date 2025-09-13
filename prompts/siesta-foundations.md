# SIESTA Foundations (from user_guide.tex)
- MeshCutoff: 150–300 Ry typical; start 200 Ry, converge test if needed.
- XC: GGA-PBE default unless specified.
- Basis: DZP for production; SZ/DZ for quick tests.
- k-grid: Monkhorst-Pack; metals finer (e.g., 12x12x1 graphene), insulators coarser.
- SCF: DM.Tolerance ~1e-4, MaxSCFIterations ~200.
- Relax: MaxForceTol 0.02 eV/Å, MD.TypeOfRun CG.
- Output: ensure SaveHS true for postproc (bands/PDOS).
- Always check total force, stress, and Fermi level sanity.
