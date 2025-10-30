import pandas as pd

# File paths
ALL_CVE_FILE = "CHERI Dataset - CVEs.csv"
RUST_VS_CHERI_FILE = "CHERI Dataset - CHERI vs Rust CVEs.csv"

# normalize true/false to bool
def to_bool(series):
    mapping = {"true": True, "yes": True, "1": True,
               "false": False, "no": False, "0": False}
    s = series.astype(str).str.strip().str.lower()
    s = s.map(mapping)
    return s.where(s.notna(), False).astype(bool)

def bool_cols(df):
    cols = []
    for c in df.columns:
        vals = df[c].dropna().astype(str).str.lower()
        if vals.isin(["true", "false", "yes", "no", "1", "0"]).any():
            cols.append(c)
    return cols


choice = 0
while(choice != 3):
    print("Select dataset:")
    print("1. CVEs Dataset")
    print("2. Rust vs CHERI Dataset")
    print("3. Quit")
    choice = input("Enter 1 or 2 or 3: ").strip()

    # Case 1 — All CVEs
    if choice == "1":
        df = pd.read_csv(ALL_CVE_FILE)

        print("\nAvailable columns:")
        for i, c in enumerate(df.columns, 1):
            print(f"{i}. {c}")

        col = df.columns[int(input("\nPick column number: ")) - 1]
        vals = df[col].dropna().unique()

        print(f"\nValues in '{col}':")
        for i, v in enumerate(vals, 1):
            print(f"{i}. {v}")

        val = vals[int(input("Pick value number: ")) - 1]
        rows = df[df[col] == val]

        print(f"\nFiltering rows where {col} = '{val}'")
        print(f"Total rows: {len(rows)}\n")

        if "Symptoms" in df.columns:
            print("Symptoms and counts:")
            counts = rows["Symptoms"].value_counts()
            if "Solved by CHERI?" in df.columns:
                for symptom, count in counts.items():
                    subset = rows[rows["Symptoms"] == symptom]
                    b = to_bool(subset["Solved by CHERI?"])
                    yes, no = int(b.sum()), int(len(b) - b.sum())
                    print(f"{symptom}: {count} | Solved by CHERI?: Yes={yes}, No={no}")
            else:
                print(rows["Symptoms"].value_counts().to_string())
        else:
            print("No 'Symptoms' column found.")
        print()

    # Case 2 — Rust vs CHERI
    elif choice == "2":
        df = pd.read_csv(RUST_VS_CHERI_FILE)

        print("\nAvailable columns:")
        for i, c in enumerate(df.columns, 1):
            print(f"{i}. {c}")

        col = df.columns[int(input("\nPick column number: ")) - 1]
        vals = df[col].dropna().unique()

        print(f"\nValues in '{col}':")
        for i, v in enumerate(vals, 1):
            print(f"{i}. {v}")

        val = vals[int(input("Pick value number: ")) - 1]
        rows = df[df[col] == val]

        print(f"\nFiltering rows where {col} = '{val}'")
        print(f"Total rows: {len(rows)}\n")

        bcols = bool_cols(rows)
        if bcols:
            group_col = None
            if "Symptoms" in rows.columns:
                group_col = "Symptoms"
            elif "Causes" in rows.columns:
                group_col = "Causes"

            if group_col:
                counts = rows[group_col].value_counts()
                print(f"{group_col} and counts:")
                for val2, count in counts.items():
                    subset = rows[rows[group_col] == val2]
                    extras = []
                    for bc in bcols:
                        b = to_bool(subset[bc])
                        yes, no = int(b.sum()), int(len(b) - b.sum())
                        extras.append(f"{bc}: Yes={yes}, No={no}")
                    extra_str = " | ".join(extras)
                    print(f"{val2}: {count}" + (f" | {extra_str}" if extra_str else ""))
            else:
                print("Boolean totals:")
                for bc in bcols:
                    b = to_bool(rows[bc])
                    yes, no = int(b.sum()), int(len(b) - b.sum())
                    print(f"{bc}: Yes={yes}, No={no}")
        else:
            print("No boolean-like columns found.")
        print()

    else:
        print("Invalid choice.")
        print()
