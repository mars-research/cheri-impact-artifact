

This document describes the data artifact corresponding to the paper “Understanding the Security Impact of CHERI on the Operating System Kernel.”

The raw datasets used in our analysis are available at the following URL:

https://docs.google.com/spreadsheets/d/1nLsI_KLPio3jMF1xHISSkB2t565U0d1Mz0LIf5bieMk/edit


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


Alternatively, we also provide a Python script that uses **pandas** to filter columns and return a breakdown of manifestations and causes. This script can be used to quickly navigate the dataset.

**Repo:** https://github.com/mars-research/cheri-impact-artifact

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
...
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

Finally, choosing the value to filter on such as **1 (Linux)** produces a breakdown of manifestations and causes:

```
Symptoms and counts:
Use after free                                Total=96   | Solved by CHERI?: Yes=96, No=0
...

Causes and counts:
Language - Lifetime violation                 Total=68   | Solved by CHERI?: Yes=38, No=30
...
```

These results correspond to data shown in the tables, in this example some Linux entries from **Table 1** and **Table 2**.

**Terminology clarification:** In the paper “Language – Null byte termination” and "Symptoms" from the dataset are referred to as “Language – Sentinel arrays” and "Manifestations", respectively.

# Recreating Tables 1–5


Some tables contain paired entries denoted **X | Y**, where **X** is the value under the assumption of active capability revocation and **Y** is the value without it. For these tables, the relevant queries must be executed on both the regular and *(No Revocation)* variants of the datasets, which can be selected from the initial *Select dataset:* menu.

For convenience, we also provide a small wrapper script (helper.py) that calls filter.py and prints all table data to the terminal:
> python3 helper.py

The helper script simply parses the output of the following manual queries:


To recreate **Tables 1 and 2**, query each value in the **“OS”** column of the first dataset:

Select dataset:  
> 1. CVEs Dataset  

Available columns:  
> 3. OS  

Values in 'OS':  
> 1. Linux  
> 2. FreeBSD  

Each query returns its respective Linux or FreeBSD portion of the table.  

---

To recreate **Table 4**, query each value in the **“Causes”** column of the same dataset:

Select dataset:  
> 1. CVEs Dataset  

Available columns:  
> 5. Causes  

Values in 'Causes':  
> 1. Language -  Polymorphism  
> 2. Language - Lifetime violation  
> 3. Semantic - Logic error  
> 4. Language - Improper memory initialization  
> 5. Protocol - Missing Protocol Steps  
> 6. Race condition - Improper usage of synchronization primitives  
> 7. Semantic - Spec error  
> 8. Semantic - Improper input validation  
> 9. Race condition - TOUTOC  
> 10. Protocol - Sleeping in atomic context  
> 11. Language - Integer overflow  
> 12. Semantic - Missing return value check  
> 13. Semantic - Loop termination  
> 14. Language - Container_of  
> 15. Semantic - Security and permissions  
> 16. Language - Null byte termination  

Each query returns the manifestation breakdown corresponding to that cause’s row.

---


To recreate **Tables 3 and 5**, query all entries in the second dataset:

Select dataset:  
> 2. Rust vs CHERI Dataset

Available columns:
> 3. OS

Values in 'OS':  
> 1. Linux

This query returns a breakdown of all manifestations and causes from the second dataset. 

