# PDOS workflow
- Request projected DOS via appropriate SIESTA flags (e.g., Projectors.PDOS).
- After run, convert PDOS output to JSON: {"E":[...], "total":[...], "proj": {"Si:s":[...], ...}}
- Plot with tools/plot_pdos.py.
