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

---

👉 With this version, you should no longer see `UnicodeDecodeError`, mismatched comparisons, or `AttributeError`.  

Would you like me to also add **debug logging** (like printing out the first few `SEC` and `TIME OF WEEK` values) so you can verify why matches are or aren’t happening?
