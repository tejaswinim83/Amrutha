Got it — here’s the **full modified function** with the `time_diff < 0.001` condition integrated. You can copy-paste this directly:

```python
def process_files(receiver_file, presize_file, output_file):

    print("Loading presize file...")

    presize_dict = {}

    # -------------------------------
    # Load presize data (FIX: consistent key type)
    # -------------------------------
    with open(presize_file, 'r') as f:
        next(f)
        presize_reader = csv.DictReader(f)

        for row in presize_reader:
            try:
                key = int(float(row['TIME OF WEEK'].strip()))
                presize_dict[key] = row
            except:
                continue

    print("Presize entries loaded:", len(presize_dict))

    # -------------------------------
    # Plot arrays
    # -------------------------------
    plot_time = []
    Delta_X = []
    Delta_Y = []
    Delta_Z = []
    RSS_POS = []
    RSS_VEL = []
    ALT = []

    results_written = 0

    print("Processing receiver file...")

    with open(receiver_file, 'r') as rf, open(output_file, 'w', newline='') as wf:

        receiver_reader = csv.DictReader(rf)

        fieldnames = [
            'SEC','NANO','POS_MODE','POS_AV','TIME_AV','TIME_OF_WEEK','TIME_DIFF',
            'POS_X','POS_Y','POS_Z','POS_VX','POS_VY','POS_VZ',
            'PRE_POS_X','PRE_POS_Y','PRE_POS_Z',
            'PRE_POS_VX','PRE_POS_VY','PRE_POS_VZ',
            'ACC_X','ACC_Y','ACC_Z',
            'PRECISE_SV_PROP_X','PRECISE_SV_PROP_Y','PRECISE_SV_PROP_Z'
        ]

        writer = csv.DictWriter(wf, fieldnames=fieldnames)
        writer.writeheader()

        for receiver_row in receiver_reader:

            try:
                # -------------------------------
                # Check flags (FIX: strip)
                # -------------------------------
                if (receiver_row['TIME_AV'].strip() != 'TIME AV' or
                    receiver_row['POS_MODE'].strip() != '3D' or
                    receiver_row['POS_AV'].strip() != 'POS AV'):
                    continue

                # -------------------------------
                # Zero filtering (RESTORED)
                # -------------------------------
                if (float(receiver_row['POS_X']) == 0 or
                    float(receiver_row['POS_Y']) == 0 or
                    float(receiver_row['POS_Z']) == 0 or
                    float(receiver_row['VEL_X']) == 0 or
                    float(receiver_row['VEL_Y']) == 0 or
                    float(receiver_row['VEL_Z']) == 0):
                    continue

                # -------------------------------
                # Time handling (FIX: consistent type)
                # -------------------------------
                receiver_sec = int(float(receiver_row['SEC'].strip()))

                presize_row = presize_dict.get(receiver_sec)
                if presize_row is None:
                    continue

                receiver_nano = float(receiver_row['Sys_NanoSecond']) / 1e9
                receiver_time = receiver_sec + receiver_nano

                presize_time = float(presize_row['TIME OF WEEK'])
                time_diff = receiver_time - presize_time

                # -------------------------------
                # Only compute propagation if time_diff < 0.001
                # -------------------------------
                if time_diff >= 0.001:
                    continue

                # -------------------------------
                # Receiver state
                # -------------------------------
                PVT_SV = [
                    float(receiver_row['POS_X']),
                    float(receiver_row['POS_Y']),
                    float(receiver_row['POS_Z']),
                    float(receiver_row['VEL_X']),
                    float(receiver_row['VEL_Y']),
                    float(receiver_row['VEL_Z'])
                ]

                # -------------------------------
                # Precise state
                # -------------------------------
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

                # -------------------------------
                # Propagation
                # -------------------------------
                PRECISE_SV_PROP = [
                    PRECISE_SV[0] + PRECISE_SV[3]*time_diff + 0.5*PRECISE_SV[6]*time_diff**2,
                    PRECISE_SV[1] + PRECISE_SV[4]*time_diff + 0.5*PRECISE_SV[7]*time_diff**2,
                    PRECISE_SV[2] + PRECISE_SV[5]*time_diff + 0.5*PRECISE_SV[8]*time_diff**2,
                    PRECISE_SV[3] + PRECISE_SV[6]*time_diff,
                    PRECISE_SV[4] + PRECISE_SV[7]*time_diff,
                    PRECISE_SV[5] + PRECISE_SV[8]*time_diff
                ]

                # -------------------------------
                # Differences
                # -------------------------------
                SV_Diff = [
                    PRECISE_SV_PROP[0]-PVT_SV[0],
                    PRECISE_SV_PROP[1]-PVT_SV[1],
                    PRECISE_SV_PROP[2]-PVT_SV[2],
                    PRECISE_SV_PROP[3]-PVT_SV[3],
                    PRECISE_SV_PROP[4]-PVT_SV[4],
                    PRECISE_SV_PROP[5]-PVT_SV[5]
                ]

                RSS_Pos = np.sqrt(SV_Diff[0]**2 + SV_Diff[1]**2 + SV_Diff[2]**2)
                RSS_Vel = np.sqrt(SV_Diff[3]**2 + SV_Diff[4]**2 + SV_Diff[5]**2) * 100

                Altitude = np.sqrt(
                    PRECISE_SV[0]**2 +
                    PRECISE_SV[1]**2 +
                    PRECISE_SV[2]**2
                ) - 6378136.0

                Alt_KM = Altitude / 1000

                # -------------------------------
                # Store plot data
                # -------------------------------
                plot_time.append(receiver_sec)
                Delta_X.append(SV_Diff[0])
                Delta_Y.append(SV_Diff[1])
                Delta_Z.append(SV_Diff[2])
                RSS_POS.append(RSS_Pos)
                RSS_VEL.append(RSS_Vel)
                ALT.append(Alt_KM)

                # -------------------------------
                # Write output
                # -------------------------------
                writer.writerow({
                    'SEC': receiver_sec,
                    'NANO': receiver_time,
                    'POS_MODE': receiver_row['POS_MODE'],
                    'POS_AV': receiver_row['POS_AV'],
                    'TIME_AV': receiver_row['TIME_AV'],
                    'TIME_OF_WEEK': presize_time,
                    'TIME_DIFF': time_diff,
                    'POS_X': PVT_SV[0],
                    'POS_Y': PVT_SV[1],
                    'POS_Z': PVT_SV[2],
                    'POS_VX': PVT_SV[3],
                    'POS_VY': PVT_SV[4],
                    'POS_VZ': PVT_SV[5],
                    'PRE_POS_X': PRECISE_SV[0],
                    'PRE_POS_Y': PRECISE_SV[1],
                    'PRE_POS_Z': PRECISE_SV[2],
                    'PRE_POS_VX': PRECISE_SV[3],
                    'PRE_POS_VY': PRECISE_SV[4],
                    'PRE_POS_VZ': PRECISE_SV[5],
                    'ACC_X': PRECISE_SV[6],
                    'ACC_Y': PRECISE_SV[7],
                    'ACC_Z': PRECISE_SV[8],
                    'PRECISE_SV_PROP_X': PRECISE_SV_PROP[0],
                    'PRECISE_SV_PROP_Y': PRECISE_SV_PROP[1],
                    'PRECISE_SV_PROP_Z': PRECISE_SV_PROP[2]
                })

                results_written += 1

            except Exception as e:
                print("Row error:", e)

    print("Processing completed")
    print("Total matches:", results_written)

    # -------------------------------
    # Sort before plotting (FIX)
    # -------------------------------
    if plot_time:
        data = list(zip(plot_time, Delta_X, Delta_Y, Delta_Z, RSS_POS, RSS_VEL))
        data.sort(key=lambda x: x[0])
        plot_time, Delta_X, Delta_Y, Delta_Z, RSS_POS, RSS_VEL = map(list, zip(*data))
    else:
        print("No valid matched data found.")
        return

    # -------------------------------
    # Plot Position
    # -------------------------------
    plt.figure(figsize=(10,6))
    plt.plot(plot_time, Delta_X, label='ΔX')
    plt.plot(plot_time, Delta_Y, label='ΔY')
    plt.plot(plot_time, Delta_Z, label='ΔZ')
    plt.plot(plot_time, RSS_POS, label='RSS_POS')

    plt.xlabel("Receiver Time (sec)")
    plt.ylabel("Position Error (m)")
    plt.title("Position Differences")

    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))

   
   
   ============================================
   
   
   import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator


def process_files(receiver_file, presize_file, output_file):

    print("Loading presize file...")

    presize_dict = {}

    # -------------------------------
    # Load presize data
    # -------------------------------
    with open(presize_file, 'r') as f:
        next(f)  # skip first line if needed
        presize_reader = csv.DictReader(f)

        for row in presize_reader:
            try:
                key = int(float(row['TIME OF WEEK'].strip()))
                presize_dict[key] = row
            except:
                continue

    print("Presize entries loaded:", len(presize_dict))

    # -------------------------------
    # Plot arrays
    # -------------------------------
    plot_time = []
    Delta_X, Delta_Y, Delta_Z = [], [], []
    RSS_POS, RSS_VEL = [], []
    time_diffs = []

    results_written = 0

    print("Processing receiver file...")

    prev_receiver_time = None  # for successive difference

    with open(receiver_file, 'r') as rf, open(output_file, 'w', newline='') as wf:

        receiver_reader = csv.DictReader(rf)

        fieldnames = [
            'SEC','NANO','POS_MODE','POS_AV','TIME_AV','TIME_OF_WEEK',
            'TIME_DIFF','SUCCESSIVE_DT',
            'POS_X','POS_Y','POS_Z','POS_VX','POS_VY','POS_VZ',
            'PRE_POS_X','PRE_POS_Y','PRE_POS_Z',
            'PRE_POS_VX','PRE_POS_VY','PRE_POS_VZ',
            'ACC_X','ACC_Y','ACC_Z',
            'PRECISE_SV_PROP_X','PRECISE_SV_PROP_Y','PRECISE_SV_PROP_Z'
        ]

        writer = csv.DictWriter(wf, fieldnames=fieldnames)
        writer.writeheader()

        for receiver_row in receiver_reader:
            try:
                # -------------------------------
                # Filter valid rows
                # -------------------------------
                if (receiver_row['TIME_AV'].strip() != 'TIME AV' or
                    receiver_row['POS_MODE'].strip() != '3D' or
                    receiver_row['POS_AV'].strip() != 'POS AV'):
                    continue

                if (float(receiver_row['POS_X']) == 0 or
                    float(receiver_row['POS_Y']) == 0 or
                    float(receiver_row['POS_Z']) == 0 or
                    float(receiver_row['VEL_X']) == 0 or
                    float(receiver_row['VEL_Y']) == 0 or
                    float(receiver_row['VEL_Z']) == 0):
                    continue

                # -------------------------------
                # Time handling
                # -------------------------------
                receiver_sec = int(float(receiver_row['SEC'].strip()))
                receiver_nano = float(receiver_row['Sys_NanoSecond']) / 1e9
                receiver_time = receiver_sec + receiver_nano

                presize_row = presize_dict.get(receiver_sec)
                if presize_row is None:
                    continue

                presize_time = float(presize_row['TIME OF WEEK'])
                time_diff = receiver_time - presize_time

                # -------------------------------
                # Successive time difference
                # -------------------------------
                if prev_receiver_time is not None:
                    successive_dt = receiver_time - prev_receiver_time
                else:
                    successive_dt = 0.0

                prev_receiver_time = receiver_time
                time_diffs.append(successive_dt)

                # -------------------------------
                # Receiver state
                # -------------------------------
                PVT_SV = [
                    float(receiver_row['POS_X']),
                    float(receiver_row['POS_Y']),
                    float(receiver_row['POS_Z']),
                    float(receiver_row['VEL_X']),
                    float(receiver_row['VEL_Y']),
                    float(receiver_row['VEL_Z'])
                ]

                # -------------------------------
                # Precise state
                # -------------------------------
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

                # -------------------------------
                # Propagation
                # -------------------------------
                PRECISE_SV_PROP = [
                    PRECISE_SV[0] + PRECISE_SV[3]*time_diff + 0.5*PRECISE_SV[6]*time_diff**2,
                    PRECISE_SV[1] + PRECISE_SV[4]*time_diff + 0.5*PRECISE_SV[7]*time_diff**2,
                    PRECISE_SV[2] + PRECISE_SV[5]*time_diff + 0.5*PRECISE_SV[8]*time_diff**2,
                    PRECISE_SV[3] + PRECISE_SV[6]*time_diff,
                    PRECISE_SV[4] + PRECISE_SV[7]*time_diff,
                    PRECISE_SV[5] + PRECISE_SV[8]*time_diff
                ]

                # -------------------------------
                # Differences
                # -------------------------------
                SV_Diff = [
                    PRECISE_SV_PROP[0] - PVT_SV[0],
                    PRECISE_SV_PROP[1] - PVT_SV[1],
                    PRECISE_SV_PROP[2] - PVT_SV[2],
                    PRECISE_SV_PROP[3] - PVT_SV[3],
                    PRECISE_SV_PROP[4] - PVT_SV[4],
                    PRECISE_SV_PROP[5] - PVT_SV[5]
                ]

                RSS_Pos = np.sqrt(SV_Diff[0]**2 + SV_Diff[1]**2 + SV_Diff[2]**2)
                RSS_Vel = np.sqrt(SV_Diff[3]**2 + SV_Diff[4]**2 + SV_Diff[5]**2) * 100

                # -------------------------------
                # Store for plotting
                # -------------------------------
                plot_time.append(receiver_sec)
                Delta_X.append(SV_Diff[0])
                Delta_Y.append(SV_Diff[1])
                Delta_Z.append(SV_Diff[2])
                RSS_POS.append(RSS_Pos)
                RSS_VEL.append(RSS_Vel)

                # -------------------------------
                # Write output
                # -------------------------------
                writer.writerow({
                    'SEC': receiver_sec,
                    'NANO': receiver_time,
                    'POS_MODE': receiver_row['POS_MODE'],
                    'POS_AV': receiver_row['POS_AV'],
                    'TIME_AV': receiver_row['TIME_AV'],
                    'TIME_OF_WEEK': presize_time,
                    'TIME_DIFF': time_diff,
                    'SUCCESSIVE_DT': successive_dt,
                    'POS_X': PVT_SV[0],
                    'POS_Y': PVT_SV[1],
                    'POS_Z': PVT_SV[2],
                    'POS_VX': PVT_SV[3],
                    'POS_VY': PVT_SV[4],
                    'POS_VZ': PVT_SV[5],
                    'PRE_POS_X': PRECISE_SV[0],
                    'PRE_POS_Y': PRECISE_SV[1],
                    'PRE_POS_Z': PRECISE_SV[2],
                    'PRE_POS_VX': PRECISE_SV[3],
                    'PRE_POS_VY': PRECISE_SV[4],
                    'PRE_POS_VZ': PRECISE_SV[5],
                    'ACC_X': PRECISE_SV[6],
                    'ACC_Y': PRECISE_SV[7],
                    'ACC_Z': PRECISE_SV[8],
                    'PRECISE_SV_PROP_X': PRECISE_SV_PROP[0],
                    'PRECISE_SV_PROP_Y': PRECISE_SV_PROP[1],
                    'PRECISE_SV_PROP_Z': PRECISE_SV_PROP[2]
                })

                results_written += 1

            except Exception as e:
                print("Row error:", e)

    print("Processing completed")
    print("Total matches:", results_written)

    # -------------------------------
    # Sort before plotting
    # -------------------------------
    if not plot_time:
        print("No valid matched data found.")
        return

    data = list(zip(plot_time, Delta_X, Delta_Y, Delta_Z, RSS_POS, RSS_VEL, time_diffs))
    data.sort(key=lambda x: x[0])

    plot_time, Delta_X, Delta_Y, Delta_Z, RSS_POS, RSS_VEL, time_diffs = map(list, zip(*data))

    # -------------------------------
    # Plot Position
    # -------------------------------
    plt.figure(figsize=(10,6))
    plt.plot(plot_time, Delta_X, label='ΔX')
    plt.plot(plot_time, Delta_Y, label='ΔY')
    plt.plot(plot_time, Delta_Z, label='ΔZ')
    plt.plot(plot_time, RSS_POS, label='RSS_POS')
    plt.xlabel("Receiver Time (sec)")
    plt.ylabel("Position Error (m)")
    plt.title("Position Differences")
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # -------------------------------
    # Plot Velocity
    # -------------------------------
    plt.figure(figsize=(10,6))
    plt.plot(plot_time, RSS_VEL, label='RSS_VEL')
    plt.xlabel("Receiver Time (sec)")
    plt.ylabel("Velocity Error (cm/s)")
    plt.title("Velocity Differences")
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # -------------------------------
    # Plot Successive Time Difference
    # -------------------------------
    plt.figure(figsize=(10,6))
    plt.plot(plot_time, time_diffs, label='Δt (successive)')
    plt.xlabel("Receiver Time (sec)")
    plt.ylabel("Time Difference (sec)")
    plt.title("Successive Receiver Time Difference")
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    process_files("receiver.csv", "presize.csv", "matched_output.csv")
