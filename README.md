

This document documents data artifact corresponding 
to paper "Understanding the Security Impact of CHERI
on the Operating System Kernel". 

The raw datasets used in our analysis are available at the following URL:

https://docs.google.com/spreadsheets/d/1nLsI_KLPio3jMF1xHISSkB2t565U0d1Mz0LIf5bieMk/edit

## Navigating the Dataset

Final tables:

- **CVE Table**: Corresponds to Table 1 in Section 5.1
- **CHERI vs Rust Table**: Corresponds to Table 2 in Section 5.2

Source datasets:

- **CVEs**: The full dataset with labeled CVEs
- **CHERI vs Rust CVEs**: The subset of CVEs for Table 2

# Overall Metholodogy.

Each CVEs has following attribute (columns).

| Field              | Description                                               |
|-------------------|----------------------------------------------------------- |
| CVE ID             | Unique ID for a security flaw.                            |
| URL                | Link to more vulnerability details.                       |
| OS                 | Affected operating systems and versions.                  |
| Description        | Summary of the security problem.                          |
| Causes             | High level programming error such as lack of language support. |
| Symptoms           | Low level security primitive such as out-of-bounds access. |
| Solved by CHERI?   | Can CHERI hardware prevent this flaw?                     |
| Solved by Rust?    | Can Rust language prevent this flaw?                      |
| Note               | Additional comments                                       |

One can find different summary of the entire datasets under a few different sheets

- summary by cause
- summary by symptom
- CHERI vs RUST

# Query the dataset

## Google Sheets
1. Go to`CVEs` tab. 
2. Click on top left calculator icon and select `create custom filter`
3. Click on filter icon on desire column (attribute) to set filter.

Example: 
One can view all CVEs that are labeled with cause of polymorphism by only selecting `Language -  Polymorphism` category. 




## Python script


Alternatively, we also provide a Python script that uses **pandas** to filter columns and return a breakdown of manifestations. This script can be used to quickly navigate the dataset.

**Repo:** https://github.com/JoshAgustinT/cheri_AE

**Dependencies:** Python, pandas (Python library)

**Instructions:**  
Clone the repository and navigate into it:

```bash
cd <repo-name>
```

Install pandas if necessary:  
<https://pandas.pydata.org/docs/getting_started/install.html>

Then run:  
```bash
python3 filter.py
```

Once executed, you will see the following menu:

```
Select dataset:
1. All CVEs Dataset
2. Rust vs CHERI Dataset
3. Quit
```

Option 1 corresponds to the **CVEs** dataset:  
<https://docs.google.com/spreadsheets/d/13GzB_10g1z9h21mgp-T2l2h9haLcvQ9AhgLa691QuHI/edit?gid=1583578375#gid=1583578375>  

Option 2 corresponds to the **CHERI vs Rust CVEs** dataset:  
<https://docs.google.com/spreadsheets/d/13GzB_10g1z9h21mgp-T2l2h9haLcvQ9AhgLa691QuHI/edit?gid=1502739052#gid=1502739052>  

After choosing a dataset, you will be prompted to select a column to filter on, for example:

```
Available columns:
1. CVE ID
2. URL
3. OS
4. Description
5. Causes
6. Symptoms
7. Solved by CHERI?
8. Solved by Rust?
9. Notes
```

Next, you will be shown the unique values within that column. In this example, we select option **3 (OS):**

```
Values in 'OS':
1. Linux
2. FreeBSD
```

Finally, choosing the value to filter on such as **1 (Linux)** produces a breakdown of manifestations:

```
Symptoms and counts:
Use after free: 96 | Solved by CHERI?: Yes=96, No=0
OOB access: 67 | Solved by CHERI?: Yes=67, No=0
Invalid pointer dereference: 60 | Solved by CHERI?: Yes=60, No=0
Failure to release CPU: 24 | Solved by CHERI?: Yes=1, No=23
Resource leak: 24 | Solved by CHERI?: Yes=0, No=24
High level spec violation: 17 | Solved by CHERI?: Yes=0, No=17
Uninitialized memory access: 15 | Solved by CHERI?: Yes=0, No=15
Double free: 14 | Solved by CHERI?: Yes=0, No=14
Explicit exception/panic: 11 | Solved by CHERI?: Yes=0, No=11
Access control violation: 10 | Solved by CHERI?: Yes=0, No=10
```

These results correspond to data shown in the tables, in this example the Linux entries from **Table 2**.

**Note:**  
This script provides an alternative way to query and explore the dataset quickly. However, our main reference for creating the tables was through custom queries in Google Sheets. As a result, the script output format may differ slightly. For example, script may split totals by manifestation, whereas the tables present cumulative totals. Or in the given example, two queries would be necessary to retrieve data for Table 2 (one for each entry in OS). 
