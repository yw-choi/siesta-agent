#!/usr/bin/env python3
import argparse, pathlib, matplotlib.pyplot as plt

def read_eig(path):
    ks=[]; bands=[]
    with open(path) as f:
        for ln in f:
            vals=ln.strip().split()
            if not vals: continue
            k=float(vals[0]); es=[float(x) for x in vals[1:]]
            ks.append(k); bands.append(es)
    nb=len(bands[0])
    series=[[bands[i][j] for i in range(len(bands))] for j in range(nb)]
    return ks, series

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--eig', default='EIG')
    ap.add_argument('--png', default='bands.png')
    args=ap.parse_args()
    k, series=read_eig(args.eig)
    for s in series:
        plt.plot(k, s)
    plt.xlabel('k-path'); plt.ylabel('Energy (eV)')
    plt.tight_layout(); plt.savefig(args.png, dpi=150)
    print(f"Saved {args.png}")

if __name__=="__main__":
    main()
