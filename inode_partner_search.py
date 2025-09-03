#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path
import sys


# This script takes the tcp_discovery into parameter and looks for the combinations of inodes that communicate together.

def parse_args():
    p = argparse.ArgumentParser(
        description="Extract unique non-zero inode pairs and validate uniqueness"
    )
    p.add_argument("input_csv", help="Path to input CSV (headers: local_id,local_inode_id,remote_id,remote_inode_id)")
    p.add_argument("-o", "--output", default="inode_combos.csv", help="Output CSV file (default: inode_combos.csv)")
    return p.parse_args()

def main():
    args = parse_args()
    input_path = Path(args.input_csv)
    output_path = Path(args.output)

    # Data structures
    combos = set()                 # set of normalized pairs (inode_a, inode_b) with inode_a < inode_b
    pair_counts = {}               # optional count of occurrences per normalized pair
    partner = {}                   # inode -> its unique counterpart (enforce uniqueness)
    violations = []                # list of (inode, seen_partner, conflicting_partner)

    # Read input CSV
    with input_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_cols = {"local_inode_id", "remote_inode_id"}
        missing = required_cols - set(reader.fieldnames or [])
        if missing:
            print(f"Missing required columns: {sorted(missing)}", file=sys.stderr)
            sys.exit(2)

        for row in reader:
            try:
                li = int(row["local_inode_id"])
                ri = int(row["remote_inode_id"])
            except (KeyError, ValueError) as e:
                # Skip malformed rows
                continue

            # Keep only rows where both inode IDs are non-zero
            if li == 0 or ri == 0:
                continue

            # Normalize pair as undirected by sorting
            a, b = sorted((li, ri))
            pair = (a, b)

            # Record unique pair and count
            if pair not in combos:
                combos.add(pair)
                pair_counts[pair] = 1
            else:
                pair_counts[pair] += 1

            # Enforce uniqueness: each inode can have only one partner
            for inode, other in ((a, b), (b, a)):
                prev = partner.get(inode)
                if prev is None:
                    partner[inode] = other
                elif prev != other:
                    violations.append((inode, prev, other))

    # If any inode appears with multiple different partners, fail
    if violations:
        print("Uniqueness violations detected (each inode must relate to only one counterpart):", file=sys.stderr)
        for inode, prev, other in violations:
            print(f"- inode {inode} seen with {prev} and {other}", file=sys.stderr)
        sys.exit(1)

    # Write unique combos
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["inode_a", "inode_b"])  # normalized ascending order
        for a, b in sorted(combos):
            writer.writerow([a, b])

    print(f"Wrote {len(combos)} unique inode pairs to {output_path}")

if __name__ == "__main__":
    main()
