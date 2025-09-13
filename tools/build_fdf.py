#!/usr/bin/env python3
import json, argparse, pathlib
from jinja2 import Template

def load_structure_xyz(xyz_path):
    atoms = []
    a1=a2=a3=None
    with open(xyz_path,'r') as f:
        lines=f.read().strip().splitlines()
    n=int(lines[0].strip())
    comment=lines[1] if len(lines)>1 else ""
    import re, ast
    latt=re.findall(r'(a[123])=([^;]+)', comment)
    latmap={}
    for k,v in latt:
        try:
            latmap[k]=ast.literal_eval(v)
        except Exception:
            pass
    if all(k in latmap for k in ['a1','a2','a3']):
        a1,a2,a3=latmap['a1'],latmap['a2'],latmap['a3']
    for ln in lines[2:2+n]:
        parts=ln.split()
        if len(parts)<4: continue
        sp,x,y,z=parts[:4]
        atoms.append((sp,float(x),float(y),float(z)))
    species_order=[]
    for sp, *_ in atoms:
        if sp not in species_order:
            species_order.append(sp)
    return atoms, a1,a2,a3, species_order

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--structure', required=True, help='path to .xyz with optional lattice in comment line')
    ap.add_argument('--pseudodb', default='examples/pseudopotentials/map.json', help='symbol->pseudo map json')
    ap.add_argument('--calc', choices=['relax','scf','bands','pdos'], default='relax')
    ap.add_argument('--k', default='12,12,1')
    ap.add_argument('--mesh', type=int, default=200)
    ap.add_argument('--basis', default='DZP')
    ap.add_argument('--label', default='job')
    ap.add_argument('--elecT', type=int, default=300)
    ap.add_argument('--maxF', type=float, default=0.02)
    ap.add_argument('--template', default='templates/base.fdf.j2')
    ap.add_argument('--out', default='in.fdf')
    args=ap.parse_args()

    atoms, a1,a2,a3, species = load_structure_xyz(args.structure)
    if not atoms:
        raise SystemExit("No atoms parsed from structure")
    pseudo_map=json.loads(pathlib.Path(args.pseudodb).read_text())

    species_records=[]
    for s in species:
        if s not in pseudo_map:
            raise SystemExit(f"Missing pseudo mapping for {s} in {args.pseudodb}")
        species_records.append({
            "Z": pseudo_map[s]["Z"],
            "symbol": s,
            "pseudo": pseudo_map[s]["file"]
        })

    atom_rows=[{"x":x,"y":y,"z":z,"species_index":species.index(sp)+1} for sp,x,y,z in atoms]
    kx,ky,kz = [int(x) for x in args.k.split(',')]
    do_relax = (args.calc=='relax')
    ctx=dict(
        system_name=args.label, system_label=args.label,
        n_species=len(species_records), n_atoms=len(atom_rows),
        species=species_records, atoms=atom_rows,
        a1=a1 or [1,0,0], a2=a2 or [0,1,0], a3=a3 or [0,0,1],
        mesh_cutoff_ry=args.mesh, basis_size=args.basis,
        kx=kx, ky=ky, kz=kz, do_relax=do_relax,
        max_force_tol=args.maxF, elec_temp_k=args.elecT
    )

    tpl=Template(pathlib.Path(args.template).read_text())
    pathlib.Path(args.out).write_text(tpl.render(**ctx))
    print(f"Wrote {args.out}")

if __name__=="__main__":
    main()
