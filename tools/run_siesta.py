#!/usr/bin/env python3
import argparse, subprocess, pathlib, os, shlex, datetime

def run(cmd, **kw):
    print("+", cmd, flush=True)
    return subprocess.run(cmd, shell=True, check=True, **kw)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--fdf', default='in.fdf')
    ap.add_argument('--np', type=int, default=32)
    ap.add_argument('--siesta', default='siesta')
    ap.add_argument('--workdir', default=None)
    ap.add_argument('--pre', default='', help='prefix command, e.g. "source ~/.bashrc && module load openmpi siesta &&"')
    args=ap.parse_args()

    tstamp=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    workdir=pathlib.Path(args.workdir or f"runs/{tstamp}")
    workdir.mkdir(parents=True, exist_ok=True)
    # copy provided fdf into workdir as original name and as in.fdf (canonical name expected by redirection)
    src_fdf=pathlib.Path(args.fdf)
    if not src_fdf.exists():
        raise SystemExit(f"FDF not found: {src_fdf}")
    run(f"cp {shlex.quote(str(src_fdf))} {workdir}/")
    if src_fdf.name != 'in.fdf':
        run(f"cp {workdir / src_fdf.name} {workdir / 'in.fdf'}")
    # naive copy of pseudo files referenced by either the provided fdf content
    for ln in open(src_fdf):
        tok=ln.strip().split()
        if tok and (tok[-1].endswith('.psf') or tok[-1].endswith('.psml')):
            ps=tok[-1]
            if os.path.exists(ps):
                run(f"cp {shlex.quote(ps)} {workdir}/")

    os.chdir(workdir)
    cmd=f"{args.pre} mpirun -np {args.np} {args.siesta} < in.fdf > siesta.out"
    run(cmd)
    print(f"Done. Output in {workdir}")

if __name__=="__main__":
    main()
