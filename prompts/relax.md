# Relaxation workflow
Target: ionic relaxation until |F|max < 0.02 eV/Å

Set:
- SystemLabel = job
- MD.TypeOfRun = CG
- MD.MaxForceTol = 0.02 eV/Ang
- MeshCutoff = 200 Ry
- k-grid: metals 12x12x1, semiconductors 8x8x1 baseline
- PulayMixing 0.1–0.3; ElectronicTemperature 300 K if convergence tricky

Validation:
- If not converged in 200 steps → increase MeshCutoff or adjust mixing.
