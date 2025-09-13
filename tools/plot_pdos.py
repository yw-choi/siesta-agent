#!/usr/bin/env python3
import argparse, matplotlib.pyplot as plt, json

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pdos', default='PDOS.json',
                    help='expect {\"E\":[...], \"total\":[...], \"proj\": {\"Si:s\":[...], ...}}')
    ap.add_argument('--png', default='pdos.png')
    args=ap.parse_args()
    data=json.load(open(args.pdos))
    E=data["E"]; total=data["total"]
    plt.plot(E, total, label="total")
    for k,v in data.get("proj",{}).items():
        plt.plot(E, v, label=k)
    plt.xlabel('Energy (eV)'); plt.ylabel('DOS')
    plt.legend(); plt.tight_layout(); plt.savefig(args.png, dpi=150)
    print(f"Saved {args.png}")

if __name__=="__main__":
    main()
