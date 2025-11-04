#!/usr/bin/env python3
import subprocess, re
from collections import defaultdict, OrderedDict


def run_filter(inputs):
    return subprocess.run(
        ["python3", "filter.py"],
        input="\n".join(map(str, inputs)) + "\n",
        text=True,
        capture_output=True,
    ).stdout


# TABLES 1 & 2 – Linux vs FreeBSD (revocation / no-revocation)

def make_dict():
    return defaultdict(lambda: {"Linux": {"Yes": 0, "No": 0}, "FreeBSD": {"Yes": 0, "No": 0}})

def parse_section(lines, os_name, target):
    for line in lines:
        m = re.match(r'(.+?)\s+Total=\s*(\d+)\s+\|\s+Solved by CHERI\?: Yes=(\d+), No=(\d+)', line.strip())
        if not m:
            continue
        name, total, yes, no = m.groups()
        target[name.strip()][os_name]["Yes"] += int(yes)
        target[name.strip()][os_name]["No"] += int(no)


def normalize_name(name: str) -> str:
    n = name.strip()
    low = n.lower()
    if "race condition" in low and "improper usage of synchronization primitives" in low:
        return "Race condition - Improper usage of synch."


    return n

def cheri_linux_freebsd_tables():
    runs = {
        "With Revocation": [("Linux", [1, 3, 1, 5]), ("FreeBSD", [1, 3, 2, 5])],
        "No Revocation":   [("Linux", [3, 3, 1, 5]), ("FreeBSD", [3, 3, 2, 5])],
    }
    for label, jobs in runs.items():
        print(f"\n------------------------------------------------------------------------\nGenerating Tables 1 and 2 ({label})\n------------------------------------------------------------------------\n")
        sym, cause = make_dict(), make_dict()
        for os_name, inputs in jobs:
            content = run_filter(inputs)
            sb = re.search(r"Symptoms and counts:\n(.*?)\n\nCauses and counts:", content, re.S)
            if sb:
                parse_section(sb.group(1).splitlines(), os_name, sym)
            cb = re.search(r"Causes and counts:\n(.*?)\n\nSelect dataset:", content, re.S)
            if cb:
                parse_section(cb.group(1).splitlines(), os_name, cause)
        print_table12(f"TABLE 1 ({label}): Manifestation-centric view", sym)
        print_table12(f"TABLE 2 ({label}): Cause-centric view", cause)

def print_table12(title, data):
    print(title)
    print(f"{'Category':<45} {'Linux Yes':>10} {'Linux No':>10} {'FreeBSD Yes':>12} {'FreeBSD No':>12} {'Total Yes':>12} {'Total No':>10}")
    total_ly = total_ln = total_fy = total_fn = 0
    for k, d in data.items():
        ly, ln = d["Linux"]["Yes"], d["Linux"]["No"]
        fy, fn = d["FreeBSD"]["Yes"], d["FreeBSD"]["No"]
        total_ly += ly
        total_ln += ln
        total_fy += fy
        total_fn += fn
        name = normalize_name(k)
        print(f"{name:<45} {ly:>10}{ln:>10}{fy:>12}{fn:>12}{ly+fy:>12}{ln+fn:>10}")
    # Total row
    print(f"{'Total':<45} {total_ly:>10}{total_ln:>10}{total_fy:>12}{total_fn:>12}{total_ly+total_fy:>12}{total_ln+total_fn:>10}\n")


# TABLE 4 – Causes vs Manifestations (CSV)

def cheri_cause_manifestation_table():
    print(f"\n------------------------------------------------------------------------\nGenerating Table 4 (Cause vs Manifestation) as CSV\n------------------------------------------------------------------------\n")
    symptoms = [
        "OOB access", "Use after free", "Double free", "Uninitialized memory access",
        "Resource leak", "Invalid pointer dereference", "Explicit exception/panic",
        "Failure to release CPU", "Control flow violation", "High level spec violation",
        "Access control violation",
    ]
    causes = OrderedDict()
    for i in range(1, 17):
        out = run_filter([1, 5, i, 5])
        m = re.search(r"Filtering rows where Causes = '([^']+)'", out)
        if not m:
            continue
        cause = m.group(1).strip()
        causes[cause] = defaultdict(int)
        block = re.search(r"Symptoms and counts:\n(.*?)\n\nCauses and counts:", out, re.S)
        if not block:
            continue
        for line in block.group(1).splitlines():
            s = re.match(r'(.+?)\s+Total=(\d+)', line.strip())
            if not s:
                continue
            name, total = s.groups()
            causes[cause][name.strip()] += int(total)

    print("TABLE 4: Causes and manifestations\n")
    print("Cause vs. Manifestation," + ",".join(symptoms) + ",Total")
    grand_totals = defaultdict(int)
    for cause, vals in causes.items():
        cname = normalize_name(cause)
        row = [cname] + [str(vals.get(s, 0)) for s in symptoms] + [str(sum(vals.values()))]
        print(",".join(row))
        for s in symptoms:
            grand_totals[s] += vals.get(s, 0)
    total_sum = sum(grand_totals.values())
    print("Total," + ",".join(str(grand_totals[s]) for s in symptoms) + f",{total_sum}\n")


# TABLES 3 & 5 – CHERI vs Rust (revocation / no-revocation)

def cheri_vs_rust_tables():
    runs = {
        "With Revocation": "2\n3\n1\n5\n",
        "No Revocation":   "4\n3\n1\n5\n",
    }
    line_re = re.compile(
        r"(.+?)\s+Total=\d+\s+\|\s+Solved by CHERI\?: Yes=(\d+), No=(\d+)\s+\|\s+Solved by Rust\?: Yes=(\d+), No=(\d+)$"
    )

    def parse_block(title, out):
        blocks = re.findall(
            rf"{title}:\n(.*?)\n\nCauses and counts:|{title}:\n(.*?)\n\nSelect dataset:",
            out, re.S)
        if not blocks:
            return OrderedDict()
        text = next((b[0] or b[1] for b in blocks if b[0] or b[1]), "")
        data = OrderedDict()
        for line in text.splitlines():
            m = line_re.match(line.strip())
            if not m:
                continue
            n, cy, cn, ry, rn = m.groups()
            data[n.strip()] = {"CHERI_yes": int(cy), "CHERI_no": int(cn), "Rust_yes": int(ry), "Rust_no": int(rn)}
        return data

    def print_table(title, data):
        print(title)
        print(f"{'Category':<50} {'CHERI Yes':>10} {'CHERI No':>10} {'Rust Yes':>10} {'Rust No':>10}")
        for n, v in data.items():
            if n.strip() == "Race condition - Improper usage of synchronization primitives":
                n = "Race condition - Improper usage of synch."
            print(f"{n:<50} {v['CHERI_yes']:>10}{v['CHERI_no']:>10}{v['Rust_yes']:>10}{v['Rust_no']:>10}")
        totals = {
            "CHERI_yes": sum(v["CHERI_yes"] for v in data.values()),
            "CHERI_no":  sum(v["CHERI_no"] for v in data.values()),
            "Rust_yes":  sum(v["Rust_yes"] for v in data.values()),
            "Rust_no":   sum(v["Rust_no"] for v in data.values()),
        }
        print(f"{'Total':<50} {totals['CHERI_yes']:>10}{totals['CHERI_no']:>10}{totals['Rust_yes']:>10}{totals['Rust_no']:>10}\n")

    for label, menu_input in runs.items():
        print(f"\n------------------------------------------------------------------------\nGenerating Tables 3 and 5 ({label})\n------------------------------------------------------------------------\n")
        out = subprocess.run(["python3", "filter.py"], input=menu_input, text=True, capture_output=True).stdout
        symptoms = parse_block("Symptoms and counts", out)
        causes   = parse_block("Causes and counts", out)
        print_table(f"TABLE 3 ({label}): CHERI vs Rust by Cause", causes)
        print_table(f"TABLE 5 ({label}): CHERI vs Rust by Manifestation", symptoms)


if __name__ == "__main__":
    cheri_linux_freebsd_tables()
    cheri_cause_manifestation_table()
    cheri_vs_rust_tables()
