#!/usr/bin/env python3
import re, json, argparse, pathlib

def parse_energy_forces(out_path):
    text=pathlib.Path(out_path).read_text(errors='ignore')
    E=None
    fmax=None
    # total energy
    m=re.search(r'Total=\s*([-\d\.Ee+]+)', text)
    if m: E=float(m.group(1))
    # max force (look for 'Max force')
    m=re.search(r'Max force\s*=\s*([-\d\.Ee+]+)', text, re.I)
    if m: fmax=float(m.group(1))
    return {"total_energy_eV": E, "max_force_eV_per_A": fmax}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out', default='siesta.out')
    ap.add_argument('--json', default='summary.json')
    args=ap.parse_args()
    s=parse_energy_forces(args.out)
    pathlib.Path(args.json).write_text(json.dumps(s, indent=2))
    print(json.dumps(s, indent=2))

if __name__=="__main__":
    main()
