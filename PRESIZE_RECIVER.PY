Here’s a fully updated version of your script that should run cleanly without encoding issues, header mismatches, or `AttributeError` problems. I’ve added robust handling for stripping whitespace from headers and values, safe integer conversion, and proper CSV writing:

```python
import csv

def process_files(receiver_file, presize_file, output_file):
    # ---- Read receiver file ----
    with open(receiver_file, 'r', encoding='utf-8', errors='replace') as f:
        receiver_reader = csv.DictReader(f)
        # Strip whitespace from headers and values
        receiver_data = [
            {k.strip(): v.strip() for k, v in row.items()}
            for row in receiver_reader
        ]

    # ---- Read presize file ----
    with open(presize_file, 'r', encoding='utf-8', errors='replace') as f:
        presize_reader = csv.DictReader(f)
        presize_data = [
            {k.strip(): v.strip() for k, v in row.items()}
            for row in presize_reader
        ]

    results = []

    # ---- Process receiver rows ----
    for receiver_row in receiver_data:
        # Step 1: Check flags
        if (receiver_row.get('TIME_AV') == 'TIME AV' and
            receiver_row.get('POS_MODE') == '3D' and
            receiver_row.get('POS_AV') == 'POS AV'):

            # Step 2: Check non-zero values safely
            try:
                if (int(receiver_row['POS_X']) != 0 and
                    int(receiver_row['POS_Y']) != 0 and
                    int(receiver_row['POS_Z']) != 0 and
                    int(receiver_row['VEL_X']) != 0 and
                    int(receiver_row['VEL_Y']) != 0 and
                    int(receiver_row['VEL_Z']) != 0):

                    # Step 3: Get SEC
                    receiver_sec = int(receiver_row['SEC'])

                    # Step 4: Search presize rows
                    for presize_row in presize_data:
                        try:
                            presize_time = int(presize_row['TIME OF WEEK'])
                        except ValueError:
                            continue  # skip bad rows

                        if receiver_sec == presize_time:
                            combined = {}
                            combined.update(receiver_row)
                            combined.update(presize_row)
                            results.append(combined)
            except (ValueError, KeyError):
                continue  # skip rows with bad/missing data

    # ---- Write output ----
    if results:
        keys = results[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        print("Process completed.")
        print("Total matches found:", len(results))
    else:
        print("Process completed.")
        print("No matches found.")

if __name__ == "__main__":
    process_files("receiver.csv", "presize.csv", "matched_output.csv")
```

### ✅ Improvements
- **Encoding:** Explicitly set `encoding='utf-8'` with `errors='replace'` to avoid Unicode errors.
- **Header cleanup:** Strip whitespace from headers and values so `" SEC"` and `"SEC"` are treated the same.
- **Safe integer conversion:** Wrapped conversions in `try/except` to skip rows with invalid numbers.
- **Robust writing:** Ensures `writer.writeheader()` is always called inside the `with open(...)` block, only if results exist.
- **Clear output messages:** Prints whether matches were found or not.




==============================================


Sure! Here’s the **full code** with:

* Your original `while` loops preserved for both receiver and presize files
* Output limited to only the columns you requested: `SEC, NANO, X, Y, Z, VX, VY, VZ, POS_MODE, POS_AV, TIME_AV` (from receiver) and `TIME_OF_WEEK` (from presize)
* UTF-8 encoding to avoid Unicode errors
* Safe handling if `NANO` is missing

```python
import csv

def process_files(receiver_file, presize_file, output_file):

    # Read receiver file
    with open(receiver_file, 'r', encoding='utf-8') as f:
        receiver_reader = csv.DictReader(f)
        receiver_data = list(receiver_reader)

    # Read presize file
    with open(presize_file, 'r', encoding='utf-8') as f:
        presize_reader = csv.DictReader(f)
        presize_data = list(presize_reader)

    results = []

    i = 0
    while i < len(receiver_data):

        receiver_row = receiver_data[i]

        # ---- Step 1: Check 3 flags ----
        if (receiver_row['TIME_AV'] == 'TIME AV' and
            receiver_row['POS_MODE'] == '3D' and
            receiver_row['POS_AV'] == 'POS AV'):

            try:
                # ---- Step 2: Check non-zero ----
                if (int(receiver_row['POS_X']) != 0 and
                    int(receiver_row['POS_Y']) != 0 and
                    int(receiver_row['POS_Z']) != 0 and
                    int(receiver_row['VEL_X']) != 0 and
                    int(receiver_row['VEL_Y']) != 0 and
                    int(receiver_row['VEL_Z']) != 0):

                    # ---- Step 3: Get SEC ----
                    receiver_sec = int(receiver_row['SEC'])

                    # ---- Step 4: Search entire presize using while loop ----
                    j = 0
                    while j < len(presize_data):
                        presize_row = presize_data[j]
                        presize_time = int(presize_row['TIME OF WEEK'])

                        if receiver_sec == presize_time:

                            combined = {
                                # Receiver fields
                                'SEC': receiver_row['SEC'],
                                'NANO': receiver_row.get('NANO', ''),
                                'X': receiver_row['POS_X'],
                                'Y': receiver_row['POS_Y'],
                                'Z': receiver_row['POS_Z'],
                                'VX': receiver_row['VEL_X'],
                                'VY': receiver_row['VEL_Y'],
                                'VZ': receiver_row['VEL_Z'],
                                'POS_MODE': receiver_row['POS_MODE'],
                                'POS_AV': receiver_row['POS_AV'],
                                'TIME_AV': receiver_row['TIME_AV'],
                                # Presize field
                                'TIME_OF_WEEK': presize_row['TIME OF WEEK']
                            }

                            results.append(combined)

                        j += 1  # Next presize row

            except ValueError:
                # Skip rows with invalid numeric data
                pass

        i += 1  # Next receiver row

    # ---- Write output ----
    if results:
        fieldnames = [
            'SEC','NANO','X','Y','Z','VX','VY','VZ',
            'POS_MODE','POS_AV','TIME_AV','TIME_OF_WEEK'
        ]
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    print("Process completed.")
    print("Total matches found:", len(results))


if __name__ == "__main__":
    # Example paths (use raw strings or forward slashes)
    process_files(
        r"C:/Users/MyName/Desktop/G1_12-2025-20_PVT_H1.csv",
        r"C:/Users/MyName/Desktop/presize.csv",
        r"C:/Users/MyName/Desktop/matched_output.csv"
    )
```

---

### ✅ Features of this version

1. Preserves your **original nested `while` loops**.
2. Outputs **only the columns you requested**.
3. Handles Unicode paths and CSV content with `encoding='utf-8'`.
4. Skips rows if numeric conversion fails.

---

If you want, I can also make a **much faster version** that avoids scanning the entire presize file for each receiver row — it can make your script **thousands of times faster** for large files.

Do you want me to do that?

---

👉 With this version, you should no longer see `UnicodeDecodeError`, mismatched comparisons, or `AttributeError`.  

Would you like me to also add **debug logging** (like printing out the first few `SEC` and `TIME OF WEEK` values) so you can verify why matches are or aren’t happening?


====================================


import csv

def process_files(receiver_file, presize_file, output_file):

    # ---- Step 1: Read presize file into a dictionary keyed by TIME OF WEEK ----
    presize_dict = {}
    with open(presize_file, 'r', encoding='utf-8') as f:
        presize_reader = csv.DictReader(f)
        for row in presize_reader:
            presize_time = int(row['TIME OF WEEK'])
            presize_dict[presize_time] = row  # assume 1 row per TIME OF WEEK

    results = []

    # ---- Step 2: Process receiver file ----
    with open(receiver_file, 'r', encoding='utf-8') as f:
        receiver_reader = csv.DictReader(f)
        for receiver_row in receiver_reader:

            # ---- Step 2a: Check 3 flags ----
            if (receiver_row['TIME_AV'] == 'TIME AV' and
                receiver_row['POS_MODE'] == '3D' and
                receiver_row['POS_AV'] == 'POS AV'):

                try:
                    # ---- Step 2b: Check non-zero positions/velocities ----
                    if (int(receiver_row['POS_X']) != 0 and
                        int(receiver_row['POS_Y']) != 0 and
                        int(receiver_row['POS_Z']) != 0 and
                        int(receiver_row['VEL_X']) != 0 and
                        int(receiver_row['VEL_Y']) != 0 and
                        int(receiver_row['VEL_Z']) != 0):

                        rec_sec = int(receiver_row['SEC'])
                        rec_nano = int(receiver_row.get('NANO', 0))
                        time_rec = rec_sec + rec_nano / 1e9

                        # ---- Step 2c: Lookup matching presize row ----
                        presize_row = presize_dict.get(rec_sec)
                        if presize_row is None:
                            continue  # no match

                        presize_time = int(presize_row['TIME OF WEEK'])
                        time_diff = time_rec - presize_time

                        # ---- Receiver PVT_SV ----
                        PVT_SV = [
                            float(receiver_row['POS_X']),
                            float(receiver_row['POS_Y']),
                            float(receiver_row['POS_Z']),
                            float(receiver_row['VEL_X']),
                            float(receiver_row['VEL_Y']),
                            float(receiver_row['VEL_Z'])
                        ]

                        # ---- Presize PRECISE_SV ----
                        PRECISE_SV = [
                            float(presize_row['POS_X']),
                            float(presize_row['POS_Y']),
                            float(presize_row['POS_Z']),
                            float(presize_row['POS_VX']),
                            float(presize_row['POS_VY']),
                            float(presize_row['POS_VZ']),
                            float(presize_row['ACC_X']),
                            float(presize_row['ACC_Y']),
                            float(presize_row['ACC_Z'])
                        ]

                        # ---- Compute PRECISE_SV_PROP ----
                        PRECISE_SV_PROP = [
                            PRECISE_SV[0] + PRECISE_SV[3]*time_diff + 0.5*PRECISE_SV[6]*time_diff**2,
                            PRECISE_SV[1] + PRECISE_SV[4]*time_diff + 0.5*PRECISE_SV[7]*time_diff**2,
                            PRECISE_SV[2] + PRECISE_SV[5]*time_diff + 0.5*PRECISE_SV[8]*time_diff**2
                        ]

                        combined = {
                            'SEC': rec_sec,
                            'NANO': rec_nano,
                            'POS_MODE': receiver_row['POS_MODE'],
                            'POS_AV': receiver_row['POS_AV'],
                            'TIME_AV': receiver_row['TIME_AV'],
                            'TIME_OF_WEEK': presize_time,
                            'TIME_DIFF': time_diff,
                            # Receiver PVT_SV
                            'POS_X': PVT_SV[0],
                            'POS_Y': PVT_SV[1],
                            'POS_Z': PVT_SV[2],
                            'POS_VX': PVT_SV[3],
                            'POS_VY': PVT_SV[4],
                            'POS_VZ': PVT_SV[5],
                            # Presize PRECISE_SV
                            'PRE_POS_X': PRECISE_SV[0],
                            'PRE_POS_Y': PRECISE_SV[1],
                            'PRE_POS_Z': PRECISE_SV[2],
                            'PRE_POS_VX': PRECISE_SV[3],
                            'PRE_POS_VY': PRECISE_SV[4],
                            'PRE_POS_VZ': PRECISE_SV[5],
                            'ACC_X': PRECISE_SV[6],
                            'ACC_Y': PRECISE_SV[7],
                            'ACC_Z': PRECISE_SV[8],
                            # Propagated positions
                            'PRECISE_SV_PROP_X': PRECISE_SV_PROP[0],
                            'PRECISE_SV_PROP_Y': PRECISE_SV_PROP[1],
                            'PRECISE_SV_PROP_Z': PRECISE_SV_PROP[2]
                        }

                        results.append(combined)

                except ValueError:
                    pass

    # ---- Step 3: Write output ----
    if results:
        fieldnames = [
            'SEC','NANO','POS_MODE','POS_AV','TIME_AV','TIME_OF_WEEK','TIME_DIFF',
            'POS_X','POS_Y','POS_Z','POS_VX','POS_VY','POS_VZ',
            'PRE_POS_X','PRE_POS_Y','PRE_POS_Z','PRE_POS_VX','PRE_POS_VY','PRE_POS_VZ',
            'ACC_X','ACC_Y','ACC_Z',
            'PRECISE_SV_PROP_X','PRECISE_SV_PROP_Y','PRECISE_SV_PROP_Z'
        ]
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    print("Process completed.")
    print("Total matches found:", len(results))


if __name__ == "__main__":
    process_files(
        r"C:/Users/MyName/Desktop/G1_12-2025-20_PVT_H1.csv",
        r"C:/Users/MyName/Desktop/presize.csv",
        r"C:/Users/MyName/Desktop/matched_output.csv"
    )
