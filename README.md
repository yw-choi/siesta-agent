# siesta-agent

Minimal, agent-friendly SIESTA workflow skeleton for VS Code + GitHub Copilot Agent on a remote Linux node.

## Quick start
1) Put real pseudopotentials in `examples/pseudopotentials/` and update `examples/pseudopotentials/map.json`.
2) (Optional) Replace `docs/siesta/user_guide.tex` with the official User Guide you have.
3) Install deps on the remote host:
   ```bash
   python3 -m pip install --user jinja2 matplotlib
   ```
4) Build → run → parse via VS Code Tasks:
   - Terminal → Run Task… → **SIESTA: parse & plots**
5) Or via CLI:
   ```bash
   python3 tools/build_fdf.py --calc relax --structure examples/Si.xyz --pseudodb examples/pseudopotentials/map.json --k 8,8,8 --mesh 200 --basis DZP --label job
   python3 tools/run_siesta.py --np 64 --fdf in.fdf
   python3 tools/parse_outputs.py
   test -f EIG && python3 tools/plot_band.py
   ```

## Notes
- Keep long-running jobs under your cluster policy. Edit `.vscode/tasks.json` and `tools/run_siesta.py` as needed (e.g., module loads).
- Copilot Agent will follow `.copilot/instructions.md` and `prompts/*.md`.
