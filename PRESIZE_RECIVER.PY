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
