# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 11:42:19 2026

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 16:12:52 2026

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 09:15:25 2025

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 11:03:11 2025

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 09:35:03 2025

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 11:32:02 2025

@author: Admin
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 10:07:17 2025

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:21:37 2025

@author: Adminservice
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 13:55:41 2025

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 08:53:39 2025

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 09:09:07 2025

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:10:26 2025

@author: Adminservice
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 14:46:55 2025

@author: Adminservice
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:32:02 2025

@author: Adminservice
"""
import serial
import serial.tools.list_ports
import threading
from tkinter import filedialog
import queue
from tkinter import ttk
from tkinter import *
import tkinter as tk
import time
import time as cmdtime
import time as pytime
import csv
from tkinter import Radiobutton, StringVar
global status_var,status_var1
from datetime import datetime
import os
import platform
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# Global controls
replay_running = False
replay_paused = False
jump_target_sec = None
replay_filepath = None

SESSION_TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


serialData=False
ser=None
counter_value=0
counter_value2=0
counter_value3=0
counter_value4=0
# Threads and running flags for SA3 and SA4
sa3_thread = None
sa3_running = False
sa4_thread = None
sa4_running = False
display_name = "OS3A"





data_queue = queue.Queue()
commands = {
    "playback-off": "0x0002", "playback-on": "0x0003",
    "storage-on": "0x0004", "storage-off": "0x0005",
    "sps-mvn-on": "0x0006", "sps-mvn-off": "0x0007",
    "sps-model1": "0x000A", "sps-model2": "0x000B", "sps-model3": "0x000C",
    "sps-model4": "0x000D", "sps-model5": "0x000E",
    "sps-c-s-E": "0x000F", "sps-c-s-D": "0x0010",
    "sps-iono-c-E": "0x0011", "sps-iono-c-D": "0x0012",
    "sps-raim-chk1-E": "0x0015", "sps-raim-chk1-D": "0x0016",
    "sps-raim-chk2-E": "0x0017", "sps-raim-chk2-D": "0x0018",
    "navic/1g-msg-E": "0x0025", "navic/1g-msg-D": "0x0026",
    "velocity-smoothing-E": "0x0027", "velocity-smoothing-D": "0x0028",
    "port1-conf-gps": "0x0030", "port1-conf-navic": "0x0031", "port1-conf-combained": "0x0032",
    "port1-config-gps": "0x0033", "port1-config-navic": "0x0034", "port1-config-combained": "0x0035",
    "sps iono smoothing E":"0x0038","sps iono smoothing D":"0x0039",
    "pb-ccsds on": "0x003A", "pb-ccsds off": "0x003B",
    "randomizer/scrambler on": "0x003C", "randomizer/scrambler off": "0x003D",
    "pr module new": "0x003E", "pr module old": "0x003F",
    "elevation logic D": "0x0040", "elevation logic E": "0x0041",
    "sps-sw wdt E": "0x0042", "sps-sw wdt D": "0x0043",
    "s/w model change eeprom to prom": "0x0044", "s/w model change prom to eeprom": "0x0045",
    "phase center CAL D": "0x004C", "phase center CAL E": "0x004D",
    "phase center use for SPS D": "0x004E", "phase center use for SPS E": "0x004F",
    "odp1 s/w reset": "0x0050", "odp E": "0x0051", "odp D": "0x0052",
    "odp 10s E": "0x0053", "odp 10s D": "0x0054",
    "filter init commnd": "0x0055", "odp eop E cmd": "0x0056", "odp eop D cmd": "0x0057",
    "odp AnTphc usable": "0x0058", "odp AnTphc not usable": "0x0059",
    "odp Maneuver E": "0x005A", "odp Maneuver D": "0x005B",
    "odp mode change to test mode": "0x005C", "odp mode change to normal mode": "0x005D",
    "odp mode change to disable mode": "0x005E", "odp2 s/w reset": "0x005F",
    "odp power on default config load": "0x0060", "odp clock Steering E": "0x0062",
    "odp clock Steering D": "0x0063",
    "AIS IQ data on": "0x0081", "AIS IQ data off": "0x0082",
    "lais fe reset": "0x0083", "cais fe reset": "0x0084",
    "test demond prbs E": "0x0085", "test demond prbs D": "0x0086",
    "test IQ prbs E": "0x0087", "test IQ prbs D": "0x0088",
    "sps l1 track thres": "0x80B1", "sps l1 acq thres": "0x83B1",
    "sps-c limit value": "0x86B1", "sps-c restart val": "0x87B1",
    "sps iono alpha fac word": "0x90B1", "sps iono height": "0x91B1",
    "sps-storage sampling rate": "0x9300","pb frame length word": "0xAC00",
    "week roll over value": "0xAB00", "pps h/w delay":"0xB000",
    "Elevation Angle Threshold":"0xB100","Navic Tel ID": "0xB300",
    "AIS ch1 thrld_num": "0xC0B1", "AIS ch1 thrld_demon": "0xC1B1",
    "AIS ch1 thrld_ffft": "0xC2B1", "AIS ch1 sync trans": "0xCCB1",
    "AIS ch2 thrld_num": "0xC3B1", "AIS ch2 thrld_demon": "0xC4B1",
    "AIS ch2 thrld_ffft": "0xC5B1", "AIS ch2 sync trans": "0xCDB1",
    "AIS ch3 thrld_num": "0xC6B1", "AIS ch3 thrld_demon": "0xC7B1",
    "AIS ch3 thrld_ffft": "0xC8B1", "AIS ch3 sync trans": "0xCEB1",
    "AIS ch4 thrld_num": "0xC9B1", "AIS ch4 thrld_demon": "0xCAB1",
    "AIS ch4 thrld_ffft": "0xCBB1", "AIS ch4 sync trans": "0xCFB1",

}
# BUS command codes
bus_command_buttons = {}
bus_commands = [
    ("Reset", 0x01),
    ("HWDT Enable", 0x02),
    ("HWDT Disable", 0x03),
    ("SWDT Enable", 0x04),
    ("SWDT Disable", 0x05),
    ("DC/DC ON", 0x06),
    ("DC/DC OFF", 0x07),
]



class Graphics:
    pass

def set_colored_value(entry, value):
    entry.config(state="normal")
    entry.delete(0, tk.END)   # ✅ safe constant
    entry.insert(0, str(value))

    try:
        val = float(value)
    except:
        val = 0

    if val < 0:
        entry.config(fg='red')
    elif val == 0:
        entry.config(fg='orange')
    elif val <= 50:
        entry.config(fg='blue')
    elif val <= 70:
        entry.config(fg='green')
    else:
        entry.config(fg='black')

def set_status_colored(entry, value):
    """
    Insert value into entry with color coding:
    - Green → Enabled / Locked
    - Red   → Disabled / Not Locked / Unlocked
    - Black → Anything else
    """
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, str(value))

    val = str(value).lower()
    if "enabled" in val or "unlocked" in val or "on" in val:
        entry.config(fg="dark green")
    elif "disabled" in val or  "locked" in val or "off" in val:
        entry.config(fg="dark red")
    else:
        entry.config(fg="black")

    entry.config(state="readonly")



def connect_menu_init():
    global root,output_text,END,NORMAL,Button,Label,Entry,LabelFrame,Frame,Tk,Canvas,OptionMenu
    global frame1,project_entry,port_label,refresh_btn,port_bd,file_bd,file_entry1,connect_btn,status_label,manual_data_entry,file_entry,jump_entry,btn_pause_resume
    global send_btn,drop_COM,drop_bd
    global frame2,update_entry,counter_entry,mc,tele_cmd_counter,upset_cmd_counter,mux_entry,tele_entries
    global frame3,time_entry,nanotime_entry,week_entry,time_entry1,nanotime_entry1,week_entry1,time_entry2,nanotime_entry2,week_entry2
    global fix_status,time_entry3,nanotime_entry3,week_entry3
    global frame5,position_entry,velocity_entry,position_entry1,velocity_entry1,position_entry2,velocity_entry2
    global frame4,sol,pos_e,alm,time,d2_3d,pos,ccsds,rand,space_crf_id,navic_cmd
    global frame5,position_entry3,velocity_entry3,position_entry4,velocity_entry4,position_entry5,velocity_entry5
    global frame6,flag
    global frame7,csm,csm1
    global frame8,channel,svid,iode,t,p,e,d,i,r,h,a,cndr,pr,dr
    global ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,ch9,ch10,ch11,ch12,iode1,iode2,iode3,iode4,iode5,iode6,iode7,iode8,iode9,iode10,iode11,iode12,svid1,svid2,svid3,svid4,svid5
    global dr1,dr2,dr3,dr4,dr5,dr6,dr7,dr8,dr9,dr10,dr11,dr12,pr1,pr2,pr3,pr4,pr5,pr6,pr7,pr8,pr9,pr10,pr11,pr12,svid6,svid7,svid8,svid9,svid10,svid11,svid12
    global cndr1,cndr2,cndr3,cndr4,cndr5,cndr6,cndr7,cndr8,cndr9,cndr10,cndr11,cndr12,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12
    global p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12
    global a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12
    global frame9,cb,icb,drift,isd,st_bias,st_drift,clk_crr,U1,U2,word32_entries,last_cmd_b1_b2,last_cmd_b3,last_cmd_b4,acq1_svid,port1,port2
    global frame10,pdop
    global frame11,swdt,lbl,entry,lrt,SI,iode,crs,odp,phase_center,phase_center_sps
    global frame13,btn
    global status_var,status_var1,bus_var,dataword_entry,gui_entry_dict,wdt_entries,word25_entries,odp_entries
    global frame14,lbl,entry,label,ttf,TTF
    global frame15,raw_data,orbit_ph
    global frame_cndr_plot,ax_cndr,canvas_cndr,cmd_btn,btn_replay,display_name
    global tmillcond,tmillcondlim,cond_pre,cond_post,odp_prop,pre_chk_cntr,post_chk_cntr
    
    window = Tk()
    window.title("OS3A 12 CHANNNEL INTERFACE")
    window.configure(bg="lavender")
    window.geometry("1400x800")

    project_name_var = StringVar(value="OS3A")

    # === Header Banner ===
    header_label = Label(
        window,
        text="SPS TELEMETRY AND TELECOMMAND INTERFACE: OS3A",
        font=("Algerian", 20, "bold"),
        bg="light blue",
        fg="dark blue",
        pady=10
    )
    header_label.grid(row=0, column=0, columnspan=2, sticky="ew")

    # === Scrollable Canvas Setup ===
    canvas = Canvas(window, bg="lavender", highlightthickness=0)
    scrollbar_y = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(window, orient="horizontal", command=canvas.xview)
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar_y.grid(row=1, column=1, sticky="ns")
    scrollbar_x.grid(row=2, column=0, sticky="ew")

    root = Frame(canvas, bg="lavender")
    canvas.create_window((0, 0), window=root, anchor="nw")

    # Configure grid expansion
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Allow root columns to expand
    for i in range(5):
        root.grid_columnconfigure(i, weight=1)

    # Update scroll region
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    root.bind("<Configure>", on_frame_configure)

    def update_project_name(*args):
        global display_name
        input_name = project_name_var.get().strip()

        # Use "Os3A" if empty or equal to OS3A (case-insensitive)
        if not input_name or input_name.lower() == "os3a":
            display_name = "OS3A"
        else:
            display_name = input_name.upper()

        header_label.config(text=f"{display_name} TELEMETRY AND COMMAND INTERFACE")


    # Enable mouse wheel scrolling
    def bind_mousewheel(widget):
        system = platform.system()
        if system == 'Windows' or system == 'Darwin':
            widget.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        else:  # Linux
            widget.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
            widget.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    bind_mousewheel(canvas)

    #  ======================= COM MANAGER ===============
    frame1 = LabelFrame(
    root,
    text="  COM MANAGER  ",  # extra spacing in title gives a round feel
    bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame1.grid(row=0,column=0,padx=1,pady=1,sticky="nsew")

    status_var1 = StringVar(value="port Status:")


    status_label = Label(
        frame1,
        textvariable=status_var1,
        anchor="w",
        font=("Calibri", 11,"bold"),bg="lavender",fg="BLUE",
        wraplength=700,  # Adjust as needed to fit frame width
        justify="left"
    )
    status_label.grid(row=2, column=0, columnspan=8, sticky="w", padx=5, pady=(0, 5))

    project_label = Label(frame1, text = "Project Name: ", font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    project_label.grid(column=0,row=0,pady=2,padx=2)
    project_entry = Entry(frame1, textvariable=project_name_var, font=("Calibri", 11,"bold"),bg="lavender",fg="purple", width=10, justify="center")
    project_entry.grid(row=0, column=1,pady=2,padx=2)
    project_name_var.trace_add("write", update_project_name)
    port_label = Label(frame1, text = "Available port[s]: ", font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    port_label.grid(column=0,row=1,pady=2,padx=2)
    refresh_btn=Button(frame1,text="Refresh",width=10,font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=update_coms)
    refresh_btn.grid(column=2,row=1,pady=2,padx=2)
    port_bd=Label(frame1,text="Baud Rate:",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    port_bd.grid(column=3,row=1,pady=2,padx=2)
    file_bd=Label(frame1,text="File:",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    file_bd.grid(column=5,row=1,pady=2,padx=2)
    file_entry1=Entry(frame1,width=10,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    file_entry1.grid(column=6,row=1,pady=2,padx=2)
    connect_btn=Button(frame1,text="Connect",width=10,state="disabled",font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=connexion)
    connect_btn.grid(column=7,row=1,pady=2,padx=2)
    btn_replay = tk.Button(frame1, text="Replay", width=10, font=("Calibri", 11,"bold"),
                       bg="lavender", fg="purple", command=replay_from_file)
    btn_replay.grid(column=2, row=0, padx=2, pady=2)

    tk.Label(frame1, text="Jump to SYS_SEC:", font=("Calibri", 11,"bold"), bg="lavender").grid(column=3, row=0, padx=2, pady=2)

    jump_entry = tk.Entry(frame1, width=10)
    jump_entry.grid(column=4, row=0, padx=2, pady=2)

    btn_jump = tk.Button(frame1, text="Jump", width=10, font=("Calibri", 11,"bold"),bg="lavender",fg="purple", command=jump_to_sys_sec)
    btn_jump.grid(column=5, row=0, padx=2, pady=2)
    btn_pause_resume = tk.Button(frame1, text="Pause ⏸", width=10, font=("Calibri", 11,"bold"),
                                 bg="light yellow", fg="black", command=toggle_pause_resume)
    btn_pause_resume.grid(column=6, row=0, padx=2, pady=2)
    btn_stop_replay = tk.Button(frame1, text="Stop Replay", width=10, font=("Calibri", 11,"bold"),
                                bg="lavender", fg="red", command=stop_replay)
    btn_stop_replay.grid(column=7, row=0, padx=2, pady=2)
    # Pause/Resume toggle button


    # =============== COMMAND FRAME ================
    # =============== COMMAND FRAME ================
    frame13 = LabelFrame(root, text="COMMANDS",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame13.grid(row=0, column=2, pady=2,padx=2,sticky="nsew")



    status_var = StringVar(value="CMD Status:")


    status_label = Label(
        frame1,
        textvariable=status_var,
        anchor="w",
        font=("Calibri", 11,"bold"),bg="lavender",fg="BLUE",
        wraplength=700,  # Adjust as needed to fit frame width
        justify="left"
    )
    status_label.grid(row=3, column=0, columnspan=8, sticky="w", padx=5, pady=(0, 5))

    '''all_commands = list(command_data.items())
    for idx, (cmd_name, cmd_data) in enumerate(all_commands):
        btn = Button(frame13, text=cmd_name, width=10)
        btn.grid(row=5 + idx // 5, column=idx % 5, padx=2, pady=2)
        command_buttons[cmd_name] = btn

    def make_show_data_word(name):
        return lambda: show_data_word(name)
    for cmd_name in command_buttons:
        command_buttons[cmd_name].config(command=make_show_data_word(cmd_name))'''

    # SA1 Manual Entry
    Label(frame13, text="RSA1:",font=("Calibri", 11,"bold"),bg="lavender",fg="purple").grid(row=1, column=0, padx=2, pady=2, sticky='e')
    manual_entries['SA1'] = Entry(frame13, width=20,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    manual_entries['SA1'].grid(row=1, column=1, padx=2, pady=2)
    manual_entries['SA1'].insert(0, "0x0000 0x0004 0x0055")
    btn_sa1_send = Button(frame13, text="Send RSA1(hex)", width=12,font=("Calibri", 11,"bold"),bg="lavender",fg="purple", command=lambda: send_general_command(manual_entries['SA1'].get(), "SA1"))
    btn_sa1_send.grid(row=1, column=2, padx=2, pady=2)

    # SA2 Manual Entry
    Label(frame13, text="RSA2:",font=("Calibri", 11,"bold"),bg="lavender",fg="purple").grid(row=2, column=0, padx=2, pady=2, sticky='e')
    manual_entries['SA2'] = Entry(frame13, width=20,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    manual_entries['SA2'].grid(row=2, column=1, padx=2, pady=2)
    manual_entries['SA2'].insert(0, "0x0000 0x0004 0x0055")
    btn_sa2_send = Button(frame13, text="Send RSA2(hex)", width=12,font=("Calibri", 11,"bold"),bg="lavender",fg="purple" ,command=lambda: send_general_command(manual_entries['SA2'].get(), "SA2"))
    btn_sa2_send.grid(row=2, column=2, padx=2, pady=2)

    # SA3 File Browse + Send + Stop
    Label(frame13, text="RSA3:",font=("Calibri", 11,"bold"),bg="lavender",fg="purple").grid(row=3, column=0,padx=2, pady=2, sticky='e')
    file_entries['SA3'] = Entry(frame13, width=20,font=("Calibri", 11,"bold"),bg="lavender",fg="purple",)
    file_entries['SA3'].grid(row=3, column=1,padx=2, pady=2)

    def browse_file_sa3():
        filename = filedialog.askopenfilename(title="Select RSA3 Command File", filetypes=[("All Files", "*.*")])
        if filename:
            file_entries['SA3'].delete(0, tk.END)
            file_entries['SA3'].insert(0, filename)

    btn_browse_sa3 = Button(frame13, text="Browse", width=10, font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=browse_file_sa3)
    btn_browse_sa3.grid(row=3, column=2, padx=2, pady=2)

    btn_sa3_send = Button(frame13, text="Send RSA3(hex)", width=12,font=("Calibri", 11,"bold"),bg="lavender",fg="purple", command=lambda: send_general_command(None, "SA3"))
    btn_sa3_send.grid(row=3, column=3, padx=2, pady=2)

    btn_sa3_stop = Button(frame13, text="Stop RSA3", width=10,font=("Calibri", 11,"bold"),bg="lavender",fg="purple", command=stop_sa3)
    btn_sa3_stop.grid(row=3, column=4, padx=2, pady=2)

    # SA4 File Browse + Send + Stop
    Label(frame13, text="RSA4:",font=("Calibri", 11,"bold"),bg="lavender",fg="purple").grid(row=4, column=0, padx=2, pady=2, sticky='e')
    file_entries['SA4'] = Entry(frame13, width=20,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    file_entries['SA4'].grid(row=4, column=1, padx=2, pady=2)

    def browse_file_sa4():
        filename = filedialog.askopenfilename(title="Select RSA4 Command File", filetypes=[("All Files", "*.*")])
        if filename:
            file_entries['SA4'].delete(0, tk.END)
            file_entries['SA4'].insert(0, filename)

    btn_browse_sa4 = Button(frame13, text="Browse", width=10, font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=browse_file_sa4)
    btn_browse_sa4.grid(row=4, column=2, padx=2, pady=2)

    btn_sa4_send = Button(frame13, text="Send RSA4(hex)", width=12, font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=lambda: send_general_command(None, "SA4"))
    btn_sa4_send.grid(row=4, column=3, padx=5, pady=5)

    btn_sa4_stop = Button(frame13, text="Stop RSA4", width=10, font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=stop_sa4)
    btn_sa4_stop.grid(row=4, column=4, padx=2, pady=2)

    cmd_btn = Button(frame13, text="List of Commands", font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=open_popup)
    cmd_btn.grid(row=1, column=3, padx=2, pady=2)


    # ====== BUS COMMAND Section ====== # --- Show Toggle Packet Button ---
    frame_bus = LabelFrame(root, text="BUS COMMAND",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame_bus.grid(row=1, column=2, padx=2, pady=2, sticky="nsew")

    bus_var = StringVar(value=" ")  # Start with no selection

    Radiobutton(frame_bus, text="BUS A", variable=bus_var, value="A",font=("Calibri", 11,"bold"),bg="lavender",fg="purple").grid(row=0, column=0, padx=2, pady=2)
    Radiobutton(frame_bus, text="BUS B", variable=bus_var, value="B",font=("Calibri", 11,"bold"),bg="lavender",fg="purple").grid(row=0, column=1, padx=2, pady=2)

    bus_var.trace_add('write', on_bus_toggle)

    Label(frame_bus, text="RT Add(Hex):",font=("Calibri", 11,"bold"),bg="lavender",fg="purple").grid(row=1, column=0, padx=5, pady=5)
    dataword_entry = Entry(frame_bus, width=6,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    dataword_entry.grid(row=1, column=1,padx=2, pady=2)
    dataword_entry.insert(1, "00")  # default

    for i, (cmd_name, cmd_val) in enumerate(bus_commands):
        btn = Button(frame_bus, text=cmd_name, width=11, font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=lambda v=cmd_val: send_bus_command_button(v))
        btn.grid(row=2+i//4, column=i%4, padx=5, pady=5)
        bus_command_buttons[cmd_name] = btn

    send_bus_manual = Button(frame_bus, text="Bus cmd Send", width=15,font=("Calibri", 11,"bold"),bg="lavender",fg="purple",command=send_bus_command_entry)
    send_bus_manual.grid(row=1, column=3, padx=2, pady=2)

    # ====================  COUNTER ==================
    frame2=LabelFrame(root,text='COUNTERS and No of sat',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame2.grid(row=0,column=1,padx=2, pady=2,sticky="nsew")


    update_count=Label(frame2,text="Update Counter:",font=("Calibri", 11,"bold"),bg='lavender')
    update_count.grid(row=0, column=0)
    update_entry=Entry(frame2,width=12,state="readonly",font=("Calibri", 11,"bold"))
    update_entry.grid(column=1,row=0,padx=2, pady=2)

    '''counter=Label(frame2,text=" Display Counter:",font=("Calibri", 11,"bold"),bg='lavender')
    counter.grid(row=1, column=0)
    counter_entry=Entry(frame2,width=12,state="readonly",font=("Calibri", 11,"bold"))
    counter_entry.grid(column=1,row=1,padx=2, pady=2)'''

    memory_count=Label(frame2,text="Memory Count:",font=("Calibri", 11,"bold"),bg='lavender')
    memory_count.grid(row=2, column=0)
    mc=Entry(frame2,width=12,state="readonly",font=("Calibri", 11,"bold"))
    mc.grid(column=1,row=2,padx=2, pady=2)

    tele_cmd_counter=Label(frame2,text=" Tele CMD Counter:",font=("Calibri", 11,"bold"),bg='lavender')
    tele_cmd_counter.grid(row=3, column=0)
    tele_cmd_counter=Entry(frame2,width=12,state="readonly",font=("Calibri", 11,"bold"))
    tele_cmd_counter.grid(column=1,row=3,padx=2, pady=2)

    upset_cmd_counter=Label(frame2,text=" UPSET CMD Counter:",font=("Calibri", 11,"bold"),bg='lavender')
    upset_cmd_counter.grid(row=4, column=0)
    upset_cmd_counter=Entry(frame2,width=12,state="readonly",font=("Calibri", 11,"bold"))
    upset_cmd_counter.grid(column=1,row=4,padx=2, pady=2)

    labels = ["Interupt CMD Counter", "No Of Satellite"]
    tele_entries = {}

    for i, label_txt in enumerate(labels):
        lbl = tk.Label(frame2, text=label_txt + ":", font=("Calibri", 11,"bold"),bg='lavender')
        lbl.grid(row=i+5, column=0,padx=2, pady=2)

        entry = tk.Entry(frame2, width=12, state="readonly", font=("Calibri", 11,"bold"),bg='lavender')
        entry.grid(row=i+5, column=1, padx=2, pady=2)

        tele_entries[label_txt] = entry



    # ===================== MULTIPLEXER =====================
    frame2=LabelFrame(root,text='Multiplexer',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame2.grid(row=2,column=2,padx=2, pady=2,sticky="nsw")

    mux=Label(frame2,text="MUX:",font=("Calibri", 11,"bold"),bg='lavender')
    mux.grid(row=0, column=0)
    mux_entry=Entry(frame2,width=40,state="readonly",font=("Calibri", 11,"bold"))
    mux_entry.grid(column=1,row=0,padx=2, pady=2)

    #====================== TIME Availablity ==========================
    frame4=LabelFrame(root,text='Time AV',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame4.grid(row=3,column=2,padx=2, pady=2,sticky="new")

    sol=Label(frame4,text="Sol:",font=("Calibri", 11,"bold"),bg='lavender')
    sol.grid(row=0, column=0)
    sol=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    sol.grid(column=1,row=0,padx=2, pady=2)

    pos_e=Label(frame4,text="POS EST:",font=("Calibri", 11,"bold"),bg='lavender')
    pos_e.grid(row=0, column=2)
    pos_e=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    pos_e.grid(column=3,row=0,padx=2, pady=2)

    alm=Label(frame4,text="ALM:",font=("Calibri", 11,"bold"),bg='lavender')
    alm.grid(row=0, column=4)
    alm=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    alm.grid(column=5,row=0,padx=2, pady=2)

    time=Label(frame4,text="Time:",font=("Calibri", 11,"bold"),bg='lavender')
    time.grid(row=0, column=6)
    time=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    time.grid(column=7,row=0,padx=2, pady=2)

    d2_3d=Label(frame4,text="Pos Mode:",font=("Calibri", 11,"bold"),bg='lavender')
    d2_3d.grid(row=1, column=0)
    d2_3d=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    d2_3d.grid(column=1,row=1,padx=2, pady=2)

    pos=Label(frame4,text="POS:",font=("Calibri", 11,"bold"),bg='lavender')
    pos.grid(row=1, column=2)
    pos=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    pos.grid(column=3,row=1,padx=2, pady=2)

    ccsds=Label(frame4,text="Swap_mil_flag:",font=("Calibri", 11,"bold"),bg='lavender')
    ccsds.grid(row=1, column=4)
    ccsds=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    ccsds.grid(column=5,row=1,padx=2, pady=2)

    rand=Label(frame4,text="Rand_sts:",font=("Calibri", 11,"bold"),bg='lavender')
    rand.grid(row=1, column=6)
    rand=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    rand.grid(column=7,row=1,padx=2, pady=2)

    space_crf_id=Label(frame4,text="S_cft_id:",font=("Calibri", 11,"bold"),bg='lavender')
    space_crf_id.grid(row=2, column=0)
    space_crf_id=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    space_crf_id.grid(column=1,row=2,padx=2, pady=2)

    navic_cmd=Label(frame4,text="N_CMD:",font=("Calibri", 11,"bold"),bg='lavender')
    navic_cmd.grid(row=2, column=2)
    navic_cmd=Entry(frame4,width=5,state="readonly",font=("Calibri", 11,"bold"))
    navic_cmd.grid(column=3,row=2,padx=2, pady=2)

    # ===================== VALIDATION FLAG ====================
    frame6=LabelFrame(root,text='ODP_FLAG',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame6.grid(row=2,column=1,padx=2, pady=2,sticky="nsew")

    validation=Label(frame6,text="ODP_FLAG:",font=("Calibri", 11,"bold"),bg='lavender')
    validation.grid(row=3, column=0)
    flag=Entry(frame6,width=25,state="readonly",font=("Calibri", 11,"bold"))
    flag.grid(column=1,row=3,padx=2, pady=2)

    # ====================SYNC,SYSTEM,H2SYNC TIME ,PPS TIME =================
    frame3=LabelFrame(root,text="TIME",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame3.grid(row=1,column=0,padx=2, pady=2,sticky="nsew")

    Name=Label(frame3,text=" SYNC Time:",font=("Calibri", 11,"bold"),bg='lavender',padx=2, pady=2)
    Name.grid(row=1, column=1)

    time_label=Label(frame3,text="Second:",font=("Calibri", 11,"bold"),bg='lavender')
    time_label.grid(row=1, column=6)
    time_entry=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    time_entry.grid(row=1, column=7, padx=2, pady=2)

    nanotime_label=Label(frame3,text="Nano Second:",font=("Calibri", 11,"bold"),bg='lavender')
    nanotime_label.grid(row=1, column=8)
    nanotime_entry=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    nanotime_entry.grid(row=1, column=9, padx=2, pady=2)

    weeks_label=Label(frame3,text="Week Number:",font=("Calibri", 11,"bold"),bg='lavender')
    weeks_label.grid(row=1, column=10)
    week_entry=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    week_entry.grid(row=1, column=11, padx=2, pady=2)


    Name=Label(frame3,text=" SYS Time:",font=("Calibri", 11,"bold"),bg='lavender',padx=5,pady=5)
    Name.grid(row=2, column=1)

    time_label1=Label(frame3,text="Second:",font=("Calibri", 11,"bold"),bg='lavender')
    time_label1.grid(row=2, column=6)
    time_entry1=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    time_entry1.grid(row=2, column=7, padx=2, pady=2)

    nanotime_label1=Label(frame3,text="Nano Second:",font=("Calibri", 11,"bold"),bg='lavender')
    nanotime_label1.grid(row=2, column=8)
    nanotime_entry1=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    nanotime_entry1.grid(row=2, column=9, padx=2, pady=2)

    weeks_label1=Label(frame3,text="Week Number:",font=("Calibri", 11,"bold"),bg='lavender')
    weeks_label1.grid(row=2, column=10)
    week_entry1=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    week_entry1.grid(row=2, column=11, padx=2, pady=2)

    Name=Label(frame3,text=" PPS Time:",font=("Calibri", 11,"bold"),bg='lavender',padx=5,pady=5)
    Name.grid(row=3, column=1)

    time_label3=Label(frame3,text="PPS Sec:",font=("Calibri", 11,"bold"),bg='lavender')
    time_label3.grid(row=3, column=6)
    time_entry3=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    time_entry3.grid(row=3, column=7, padx=2, pady=2)

    nanotime_label3=Label(frame3,text="PPS Nano Sec:",font=("Calibri", 11,"bold"),bg='lavender')
    nanotime_label3.grid(row=3, column=8)
    nanotime_entry3=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    nanotime_entry3.grid(row=3, column=9, padx=2, pady=2)

    weeks_label3=Label(frame3,text="PPS Week No:",font=("Calibri", 11,"bold"),bg='lavender')
    weeks_label3.grid(row=3, column=10)
    week_entry3=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    week_entry3.grid(row=3, column=11, padx=2, pady=2)

    fix_status=Label(frame3,text="PPS 3D fix status:",font=("Calibri", 11,"bold"),bg='lavender')
    fix_status.grid(row=4, column=6)
    fix_status=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    fix_status.grid(row=4, column=7, padx=2, pady=2)

    '''Name=Label(frame3,text=" Header2 Time:",font=("Calibri", 11,"bold"),bg='lavender',padx=5,pady=5)
    Name.grid(row=5, column=1)

    time_label2=Label(frame3,text="Header2 Sec:",font=("Calibri", 11,"bold"),bg='lavender')
    time_label2.grid(row=5, column=6)
    time_entry2=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    time_entry2.grid(row=5, column=7, padx=2, pady=2)

    nanotime_label2=Label(frame3,text="Header2 NS:",font=("Calibri", 11,"bold"),bg='lavender')
    nanotime_label2.grid(row=5, column=8)
    nanotime_entry2=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    nanotime_entry2.grid(row=5, column=9, padx=2, pady=2)

    weeks_label2=Label(frame3,text="Header2 WN:",font=("Calibri", 11,"bold"),bg='lavender')
    weeks_label2.grid(row=5, column=10)
    week_entry2=Entry(frame3,width=15, state="readonly",font=("Calibri", 11,"bold"))
    week_entry2.grid(row=5, column=11, padx=2, pady=2)'''




    # =================== VECTOR DATA X,Y,Z,VX,VY,VZ ==============
    frame5=LabelFrame(root,text="STATE VECTOR DATA",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame5.grid(row=2,column=0,padx=2, pady=2,sticky="nsew")

    Name=Label(frame5,text="  INSTANTIATE :",font=("Calibri", 11,"bold"),bg='lavender',padx=5,pady=5)
    Name.grid(row=1, column=1)
    position_label = Label(frame5, text="X_DX:",font=("Calibri", 11,"bold"),bg='lavender')
    position_label.grid(row=1, column=3, sticky="W")
    velocity_label = Label(frame5, text="Vel_x:",font=("Calibri", 11,"bold"),bg='lavender')
    velocity_label.grid(row=1, column=9, sticky="W")
    position_label1 = Label(frame5, text="Y_DX:",font=("Calibri", 11,"bold"),bg='lavender')
    position_label1.grid(row=1, column=5, sticky="W")
    velocity_label1 = Label(frame5, text="Vel_y:",font=("Calibri", 11,"bold"),bg='lavender')
    velocity_label1.grid(row=1, column=11, sticky="W")
    position_label2 = Label(frame5, text="Z_DX:",font=("Calibri", 11,"bold"),bg='lavender')
    position_label2.grid(row=1, column=7, sticky="W")
    velocity_label2 = Label(frame5, text="Vel_z:",font=("Calibri", 11,"bold"),bg='lavender')
    velocity_label2.grid(row=1, column=13, sticky="W")

    position_entry = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    position_entry.grid(row=1, column=4,padx=2, pady=2)
    velocity_entry = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    velocity_entry.grid(row=1, column=10, padx=2, pady=2)
    position_entry1 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    position_entry1.grid(row=1, column=6, padx=2, pady=2)
    velocity_entry1 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    velocity_entry1.grid(row=1, column=12, padx=2, pady=2)
    position_entry2 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    position_entry2.grid(row=1, column=8, padx=2, pady=2)
    velocity_entry2 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    velocity_entry2.grid(row=1, column=14, padx=2, pady=2)

    Name1=Label(frame5,text="  ODP                    :",padx=2, pady=2,font=("Calibri", 11,"bold"),bg='lavender')
    Name1.grid(row=2, column=1)
    position_label3 = Label(frame5, text="X:",font=("Calibri", 11,"bold"),bg='lavender')
    position_label3.grid(row=2, column=3, sticky="W")
    velocity_label3 = Label(frame5, text="Vel_x:",font=("Calibri", 11,"bold"),bg='lavender')
    velocity_label3.grid(row=2, column=9, sticky="W")
    position_label4 = Label(frame5, text="Y:",font=("Calibri", 11,"bold"),bg='lavender')
    position_label4.grid(row=2, column=5, sticky="W")
    velocity_label4 = Label(frame5, text="Vel_y:",font=("Calibri", 11,"bold"),bg='lavender')
    velocity_label4.grid(row=2, column=11, sticky="W")
    position_label5 = Label(frame5, text="Z:",font=("Calibri", 11,"bold"),bg='lavender')
    position_label5.grid(row=2, column=7, sticky="W")
    velocity_label5 = Label(frame5, text="Vel_z:",font=("Calibri", 11,"bold"),bg='lavender')
    velocity_label5.grid(row=2, column=13, sticky="W")

    position_entry3 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    position_entry3.grid(row=2, column=4, padx=2, pady=2)
    velocity_entry3 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    velocity_entry3.grid(row=2, column=10, padx=2, pady=2)
    position_entry4 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    position_entry4.grid(row=2, column=6, padx=2, pady=2)
    velocity_entry4 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    velocity_entry4.grid(row=2, column=12, padx=2, pady=2)
    position_entry5 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    position_entry5.grid(row=2, column=8, padx=2, pady=2)
    velocity_entry5 = Entry(frame5, width=10, state="readonly",font=("Calibri", 11,"bold"))
    velocity_entry5.grid(row=2, column=14, padx=2, pady=2)

    # ====================== CHECKSUM  =============================
    frame7=LabelFrame(root,text='CHECKSUM ',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame7.grid(row=2,column=3,padx=2, pady=2,sticky="nsew")

    CSM=Label(frame7,text="Checksum SA2:",font=("Calibri", 11,"bold"),bg="lavender")
    CSM.grid(row=7, column=0)
    csm=Entry(frame7,width=10,state="readonly",font=("Calibri", 11,"bold"))
    csm.grid(column=1,row=7,padx=2, pady=2)

    CSM1=Label(frame7,text="Checksum SA3:",font=("Calibri", 11,"bold"),bg="lavender")
    CSM1.grid(row=8, column=0)
    csm1=Entry(frame7,width=10,state="readonly",font=("Calibri", 11,"bold"))
    csm1.grid(column=1,row=8,padx=2, pady=2)





    # ======================== CLOCK AND DRIFT====================

    frame9=LabelFrame(root,text='CLOCK & DRIFT',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame9.grid(row=1,column=1,padx=2, pady=2,sticky="nsew")

    validation=Label(frame9,text="Clock bias:",font=("Calibri", 11,"bold"),bg="lavender")
    validation.grid(row=3, column=0)
    cb=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    cb.grid(column=1,row=3,padx=2, pady=2)

    Ivalidation=Label(frame9,text="ISB:",font=("Calibri", 11,"bold"),bg="lavender")
    Ivalidation.grid(row=4, column=0)
    icb=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    icb.grid(column=1,row=4,padx=2, pady=2)

    drift=Label(frame9,text="Drift:",font=("Calibri", 11,"bold"),bg="lavender")
    drift.grid(row=5, column=0)
    drift=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    drift.grid(column=1,row=5,padx=2, pady=2)

    InterSystemDrift=Label(frame9,text="ISD:",font=("Calibri", 11,"bold"),bg='lavender')
    InterSystemDrift.grid(row=6, column=0)
    isd=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    isd.grid(column=1,row=6,padx=2, pady=2)

    st_bias=Label(frame9,text="St_Bias:",font=("Calibri", 11,"bold"),bg='lavender')
    st_bias.grid(row=7, column=0)
    st_bias=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    st_bias.grid(column=1,row=7,padx=2, pady=2)

    st_drift=Label(frame9,text="St_Drift:",font=("Calibri", 11,"bold"),bg="lavender")
    st_drift.grid(row=8, column=0)
    st_drift=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    st_drift.grid(column=1,row=8,padx=2, pady=2)

    clk_crr=Label(frame9,text="Clk_corr:",font=("Calibri", 11,"bold"),bg="lavender")
    clk_crr.grid(row=9, column=0)
    clk_crr=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    clk_crr.grid(column=1,row=9,padx=2, pady=2)

    U1=Label(frame9,text="U1:",font=("Calibri", 11,"bold"),bg="lavender")
    U1.grid(row=3, column=2)
    U1=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    U1.grid(column=3,row=3,padx=2, pady=2)

    U2=Label(frame9,text="U2:",font=("Calibri", 11,"bold"),bg="lavender")
    U2.grid(row=4, column=2)
    U2=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    U2.grid(column=3,row=4,padx=2, pady=2)

    labels = ["Str_Est","Str_En","Reset_C","Init"]
    word32_entries = {}

    for i, label_txt in enumerate(labels):
        lbl = tk.Label(frame9, text=label_txt + ":", font=("Calibri", 11,"bold"),bg='lavender')
        lbl.grid(row=i+5, column=2, sticky='w')

        entry = tk.Entry(frame9, width=8, state="readonly", font=("Calibri", 11,"bold"))
        entry.grid(row=i+5, column=3, padx=2, pady=2)

        word32_entries[label_txt] = entry
        
    orbit_ph=Label(frame9,text="orbit_ph:",font=("Calibri", 11,"bold"),bg="lavender")
    orbit_ph.grid(row=9, column=2)
    orbit_ph=Entry(frame9,width=8,state="readonly",font=("Calibri", 11,"bold"))
    orbit_ph.grid(column=3,row=9,padx=2, pady=2)

    #===============================LAST CMD EXE=======================

    frame9=LabelFrame(root,text='LAST_CMD_EXE',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame9.grid(row=3,column=3,padx=1,pady=1,sticky="new")

    last_cmd_b1_b2=Label(frame9,text="Last_cmd_b1_b2:",font=("Calibri", 11,"bold"),bg="lavender")
    last_cmd_b1_b2.grid(row=3, column=0)
    last_cmd_b1_b2=Entry(frame9,width=10,state="readonly",font=("Calibri", 11,"bold"))
    last_cmd_b1_b2.grid(column=1,row=3,padx=2, pady=2)

    last_cmd_b3=Label(frame9,text="Last_cmd_b3:",font=("Calibri", 11,"bold"),bg="lavender")
    last_cmd_b3.grid(row=4, column=0)
    last_cmd_b3=Entry(frame9,width=10,state="readonly",font=("Calibri", 11,"bold"))
    last_cmd_b3.grid(column=1,row=4,padx=2, pady=2)

    last_cmd_b4=Label(frame9,text="Last_cmd_b4:",font=("Calibri", 11,"bold"),bg='lavender')
    last_cmd_b4.grid(row=5, column=0)
    last_cmd_b4=Entry(frame9,width=10,state="readonly",font=("Calibri", 11,"bold"))
    last_cmd_b4.grid(column=1,row=5,padx=2, pady=2)

    acq1_svid=Label(frame9,text="ACQ1_SVID:",font=("Calibri", 11,"bold"),bg='lavender')
    acq1_svid.grid(row=6, column=0)
    acq1_svid=Entry(frame9,width=10,state="readonly",font=("Calibri", 11,"bold"))
    acq1_svid.grid(column=1,row=6,padx=2, pady=2)



     #===============================ODP PARAMETERS=======================

    frame9=LabelFrame(root,text='ODP PARAMETERS',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame9.grid(row=3,column=3,padx=1,pady=1,sticky="sew")

    odp_labels = [
        "No of I/P sat to odp",
        "No of sat est",
        "Filter Init reason",
        "Filter Init Flag",
        "KF Est Flag",
        "PPP Est Flag Unsing",
        "Ph_center En Flag"
    ]

    odp_entries = {}

    for i, label_txt in enumerate(odp_labels):
        lbl = tk.Label(frame9, text=label_txt + ":",font=("Calibri", 11,"bold"), bg='lavender')
        lbl.grid(row=i+1, column=0, sticky='w')

        entry = tk.Entry(frame9, width=12, state="readonly", font=("Calibri", 11,"bold"))
        entry.grid(row=i+1, column=1, padx=2, pady=2)

        odp_entries[label_txt] = entry

    tmillcond=Label(frame9,text="ill cond Val:",font=("Calibri", 11,"bold"),bg="lavender")
    tmillcond.grid(row=9, column=0)
    tmillcond=Entry(frame9,width=12,state="readonly",font=("Calibri", 11,"bold"))
    tmillcond.grid(column=1,row=9,padx=2, pady=2)

    tmillcondlim=Label(frame9,text="ill cond Limit:",font=("Calibri", 11,"bold"),bg="lavender")
    tmillcondlim.grid(row=10, column=0)
    tmillcondlim=Entry(frame9,width=12,state="readonly",font=("Calibri", 11,"bold"))
    tmillcondlim.grid(column=1,row=10,padx=2, pady=2)

    pre_chk_cntr=Label(frame9,text="Pre Check Counter:",font=("Calibri", 11,"bold"),bg='lavender')
    pre_chk_cntr.grid(row=11, column=0)
    pre_chk_cntr=Entry(frame9,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pre_chk_cntr.grid(column=1,row=11,padx=2, pady=2)

    post_chk_cntr=Label(frame9,text="Post Check Counter:",font=("Calibri", 11,"bold"),bg='lavender')
    post_chk_cntr.grid(row=12, column=0)
    post_chk_cntr=Entry(frame9,width=12,state="readonly",font=("Calibri", 11,"bold"))
    post_chk_cntr.grid(column=1,row=12,padx=2, pady=2)

    cond_pre=Label(frame9,text="Cond Pre check:",font=("Calibri", 11,"bold"),bg='lavender')
    cond_pre.grid(row=13, column=0)
    cond_pre=Entry(frame9,width=12,state="readonly",font=("Calibri", 11,"bold"))
    cond_pre.grid(column=1,row=13,padx=2, pady=2)

    cond_post=Label(frame9,text="Cond Post check:",font=("Calibri", 11,"bold"),bg='lavender')
    cond_post.grid(row=14, column=0)
    cond_post=Entry(frame9,width=12,state="readonly",font=("Calibri", 11,"bold"))
    cond_post.grid(column=1,row=14,padx=2, pady=2)

    odp_prop=Label(frame9,text="ODP_PROP_used:",font=("Calibri", 11,"bold"),bg='lavender')
    odp_prop.grid(row=15, column=0)
    odp_prop=Entry(frame9,width=12,state="readonly",font=("Calibri", 11,"bold"))
    odp_prop.grid(column=1,row=15,padx=2, pady=2)


    # ======================== PDOP ==========================

    frame10=LabelFrame(root,text='PDOP',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame10.grid(row=2,column=2,padx=2, pady=2,sticky="nse")

    pdop=Label(frame10,text="PDOP:",font=("Calibri", 11,"bold"),bg='lavender')
    pdop.grid(row=3, column=0)
    pdop=Entry(frame10,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pdop.grid(column=1,row=3,padx=2, pady=2)


    # ========================== SWDT AND HWDT ======================

    frame11 = tk.LabelFrame(root, text='H/W counter S/W id', bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame11.grid(row=0, column=3, padx=2, pady=2, sticky="nsew")

    swdt=Label(frame11,text="SWDT Reset counter:",font=("Calibri", 11,"bold"),bg='lavender')
    swdt.grid(row=0, column=0)
    swdt=Entry(frame11,width=10,state="readonly",font=("Calibri", 11,"bold"))
    swdt.grid(column=1,row=0,padx=2, pady=2)

    labels = ["HWDT Reset Counter", "SWDT Reset ID", "PB Storage Mode"]
    word25_entries = {}

    for i, label_txt in enumerate(labels):
        lbl = tk.Label(frame11, text=label_txt + ":", font=("Calibri", 11,"bold"),bg='lavender')
        lbl.grid(row=i+1, column=0, sticky='w')

        entry = tk.Entry(frame11, width=10, state="readonly", font=("Calibri", 11,"bold"))
        entry.grid(row=i+1, column=1, padx=2, pady=2)

        word25_entries[label_txt] = entry

    port1=Label(frame11,text="PORT1:",font=("Calibri", 11,"bold"),bg='lavender')
    port1.grid(row=7, column=0)
    port1=Entry(frame11,width=10,state="readonly",font=("Calibri", 11,"bold"))
    port1.grid(column=1,row=7,padx=2, pady=2)

    port2=Label(frame11,text="PORT2:",font=("Calibri", 11,"bold"),bg='lavender')
    port2.grid(row=8, column=0)
    port2=Entry(frame11,width=10,state="readonly",font=("Calibri", 11,"bold"))
    port2.grid(column=1,row=8,padx=2, pady=2)

    # ========================= SYS MODE AND WDT STATUS ===============================================
    frame14 = LabelFrame(root, text='System Mode and  WDT Status',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame14.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")

    labels = [
    "Iono Smoothing", "INONO Enable", "GP2015 Lock", "RFFC5071 Lock", "Nav 1A",
    "Velocity Smoothing", "GPS2015 Ant2 Lock", "RAIM", "Carrier Smoothing",
    "System Mode", "Time Aligned To"
    ]

    gui_entry_dict = {}

    for i, label_text in enumerate(labels):
        label = Label(frame14, text=label_text+ ":",font=("Calibri", 11,"bold"), bg="lavender")
        label.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        entry = Entry(frame14, width=12, state="readonly",font=("Calibri", 11,"bold"))
        entry.grid(row=i, column=1, padx=5, pady=2)
        gui_entry_dict[label_text] = entry
    #===========================================================================
    wdt_labels = [
        "Valid 1553 CMD CTR",
        "TM Selection",
        "SW Line/WDT Status",
        "HW WDT Status",
        "SPS Software Status"
    ]

    wdt_entries = {}

    for i, label_txt in enumerate(wdt_labels):
        lbl = tk.Label(frame14, text=label_txt + ":",font=("Calibri", 11,"bold"), bg='lavender')
        lbl.grid(row=i+12, column=0, sticky='w')

        entry = tk.Entry(frame14, width=12, state="readonly", font=("Calibri", 11,"bold"))
        entry.grid(row=i+12, column=1, padx=2, pady=2)

        wdt_entries[label_txt] = entry

    # =========================== TRACKING INFO ======================

    frame8=LabelFrame(root,text="TRACKING INFO",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame8.grid(row=3,column=0,padx=2, pady=2,sticky="nsew")

    channel=Label(frame8,text="Channel",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    channel.grid(row=4,column=1,padx=10,pady=10)

    ch1=Label(frame8,text="1",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch1.grid(row=5, column=1)
    ch2=Label(frame8,text="2",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch2.grid(column=1,row=6,pady=2,padx=2)
    ch3=Label(frame8,text="3",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch3.grid(column=1,row=7,pady=2,padx=2)
    ch4=Label(frame8,text="4",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch4.grid(column=1,row=8,pady=2,padx=2)
    ch5=Label(frame8,text="5",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch5.grid(column=1,row=9,pady=2,padx=2)
    ch6=Label(frame8,text="6",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch6.grid(column=1,row=10,pady=2,padx=2)
    ch7=Label(frame8,text="7",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch7.grid(column=1,row=11,pady=2,padx=2)
    ch8=Label(frame8,text="8",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch8.grid(column=1,row=12,pady=2,padx=2)
    ch9=Label(frame8,text="9",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch9.grid(column=1,row=13,pady=2,padx=2)
    ch10=Label(frame8,text="10",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch10.grid(column=1,row=14,pady=2,padx=2)
    ch11=Label(frame8,text="11",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch11.grid(column=1,row=15,pady=2,padx=2)
    ch12=Label(frame8,text="12",padx=5,pady=5,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    ch12.grid(column=1,row=16,pady=2,padx=2)

    svid=Label(frame8,width=6,text="SVID",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    svid.grid(row=4,column=2,padx=10,pady=10)

    svid1=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid1.grid(column=2,row=5,pady=2,padx=2)
    svid2=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid2.grid(column=2,row=6,pady=2,padx=2)
    svid3=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid3.grid(column=2,row=7,pady=2,padx=2)
    svid4=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid4.grid(column=2,row=8,pady=2,padx=2)
    svid5=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid5.grid(column=2,row=9,pady=2,padx=2)
    svid6=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid6.grid(column=2,row=10,pady=2,padx=2)
    svid7=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid7.grid(column=2,row=11,pady=2,padx=2)
    svid8=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid8.grid(column=2,row=12,pady=2,padx=2)
    svid9=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid9.grid(column=2,row=13,pady=2,padx=2)
    svid10=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid10.grid(column=2,row=14,pady=2,padx=2)
    svid11=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid11.grid(column=2,row=15,pady=2,padx=2)
    svid12=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    svid12.grid(column=2,row=16,pady=2,padx=2)

    cndr=Label(frame8,width=6,text="CNDR",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    cndr.grid(row=4,column=3,padx=10,pady=10)

    cndr1=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr1.grid(column=3,row=5,pady=2,padx=2)
    cndr2=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr2.grid(column=3,row=6,pady=2,padx=2)
    cndr3=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr3.grid(column=3,row=7,pady=2,padx=2)
    cndr4=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr4.grid(column=3,row=8,pady=2,padx=2)
    cndr5=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr5.grid(column=3,row=9,pady=2,padx=2)
    cndr6=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr6.grid(column=3,row=10,pady=2,padx=2)
    cndr7=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr7.grid(column=3,row=11,pady=2,padx=2)
    cndr8=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr8.grid(column=3,row=12,pady=2,padx=2)
    cndr9=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr9.grid(column=3,row=13,pady=2,padx=2)
    cndr10=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr10.grid(column=3,row=14,pady=2,padx=2)
    cndr11=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr11.grid(column=3,row=15,pady=2,padx=2)
    cndr12=Entry(frame8,width=6,state="readonly",font=("Calibri", 11,"bold"))
    cndr12.grid(column=3,row=16,pady=2,padx=2)

    t=Label(frame8,text="T",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    t.grid(row=4,column=4,padx=5,pady=5)

    t1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t1.grid(column=4,row=5,pady=2,padx=2)
    t2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t2.grid(column=4,row=6,pady=2,padx=2)
    t3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t3.grid(column=4,row=7,pady=2,padx=2)
    t4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t4.grid(column=4,row=8,pady=2,padx=2)
    t5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t5.grid(column=4,row=9,pady=2,padx=2)
    t6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t6.grid(column=4,row=10,pady=2,padx=2)
    t7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t7.grid(column=4,row=11,pady=2,padx=2)
    t8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t8.grid(column=4,row=12,pady=2,padx=2)
    t9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t9.grid(column=4,row=13,pady=2,padx=2)
    t10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t10.grid(column=4,row=14,pady=2,padx=2)
    t11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t11.grid(column=4,row=15,pady=2,padx=2)
    t12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    t12.grid(column=4,row=16,pady=2,padx=2)


    p=Label(frame8,text="P",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    p.grid(row=4,column=5,padx=5,pady=5)

    p1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p1.grid(column=5,row=5,pady=2,padx=2)
    p2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p2.grid(column=5,row=6,pady=2,padx=2)
    p3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p3.grid(column=5,row=7,pady=2,padx=2)
    p4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p4.grid(column=5,row=8,pady=2,padx=2)
    p5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p5.grid(column=5,row=9,pady=2,padx=2)
    p6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p6.grid(column=5,row=10,pady=2,padx=2)
    p7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p7.grid(column=5,row=11,pady=2,padx=2)
    p8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p8.grid(column=5,row=12,pady=2,padx=2)
    p9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p9.grid(column=5,row=13,pady=2,padx=2)
    p10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p10.grid(column=5,row=14,pady=2,padx=2)
    p11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p11.grid(column=5,row=15,pady=2,padx=2)
    p12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    p12.grid(column=5,row=16,pady=2,padx=2)


    e=Label(frame8,text="E",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    e.grid(row=4,column=6,padx=5,pady=5)

    e1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e1.grid(column=6,row=5,pady=2,padx=2)
    e2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e2.grid(column=6,row=6,pady=2,padx=2)
    e3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e3.grid(column=6,row=7,pady=2,padx=2)
    e4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e4.grid(column=6,row=8,pady=2,padx=2)
    e5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e5.grid(column=6,row=9,pady=2,padx=2)
    e6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e6.grid(column=6,row=10,pady=2,padx=2)
    e7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e7.grid(column=6,row=11,pady=2,padx=2)
    e8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e8.grid(column=6,row=12,pady=2,padx=2)
    e9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e9.grid(column=6,row=13,pady=2,padx=2)
    e10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e10.grid(column=6,row=14,pady=2,padx=2)
    e11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e11.grid(column=6,row=15,pady=2,padx=2)
    e12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    e12.grid(column=6,row=16,pady=2,padx=2)

    d=Label(frame8,text="D",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    d.grid(row=4,column=7,padx=5,pady=5)

    d1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d1.grid(column=7,row=5,pady=2,padx=2)
    d2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d2.grid(column=7,row=6,pady=2,padx=2)

    d3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d3.grid(column=7,row=7,pady=2,padx=2)
    d4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d4.grid(column=7,row=8,pady=2,padx=2)
    d5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d5.grid(column=7,row=9,pady=2,padx=2)
    d6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d6.grid(column=7,row=10,pady=2,padx=2)
    d7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d7.grid(column=7,row=11,pady=2,padx=2)
    d8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d8.grid(column=7,row=12,pady=2,padx=2)
    d9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d9.grid(column=7,row=13,pady=2,padx=2)
    d10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d10.grid(column=7,row=14,pady=2,padx=2)
    d11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d11.grid(column=7,row=15,pady=2,padx=2)
    d12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    d12.grid(column=7,row=16,pady=2,padx=2)


    i=Label(frame8,text="I",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    i.grid(row=4,column=8,padx=5,pady=5)

    i1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i1.grid(column=8,row=5,pady=2,padx=2)
    i2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i2.grid(column=8,row=6,pady=2,padx=2)
    i3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i3.grid(column=8,row=7,pady=2,padx=2)
    i4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i4.grid(column=8,row=8,pady=2,padx=2)
    i5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i5.grid(column=8,row=9,pady=2,padx=2)
    i6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i6.grid(column=8,row=10,pady=2,padx=2)
    i7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i7.grid(column=8,row=11,pady=2,padx=2)
    i8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i8.grid(column=8,row=12,pady=2,padx=2)
    i9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i9.grid(column=8,row=13,pady=2,padx=2)
    i10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i10.grid(column=8,row=14,pady=2,padx=2)
    i11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i11.grid(column=8,row=15,pady=2,padx=2)
    i12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    i12.grid(column=8,row=16,pady=2,padx=2)


    r=Label(frame8,text="R",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    r.grid(row=4,column=9,padx=5,pady=5)

    r1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r1.grid(column=9,row=5,pady=2,padx=2)
    r2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r2.grid(column=9,row=6,pady=2,padx=2)
    r3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r3.grid(column=9,row=7,pady=2,padx=2)
    r4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r4.grid(column=9,row=8,pady=2,padx=2)
    r5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r5.grid(column=9,row=9,pady=2,padx=2)
    r6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r6.grid(column=9,row=10,pady=2,padx=2)
    r7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r7.grid(column=9,row=11,pady=2,padx=2)
    r8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r8.grid(column=9,row=12,pady=2,padx=2)
    r9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r9.grid(column=9,row=13,pady=2,padx=2)
    r10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r10.grid(column=9,row=14,pady=2,padx=2)
    r11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r11.grid(column=9,row=15,pady=2,padx=2)
    r12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    r12.grid(column=9,row=16,pady=2,padx=2)


    h=Label(frame8,text="H",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    h.grid(row=4,column=10,padx=5,pady=5)

    h1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h1.grid(column=10,row=5,pady=2,padx=2)
    h2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h2.grid(column=10,row=6,pady=2,padx=2)
    h3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h3.grid(column=10,row=7,pady=2,padx=2)
    h4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h4.grid(column=10,row=8,pady=2,padx=2)
    h5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h5.grid(column=10,row=9,pady=2,padx=2)
    h6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h6.grid(column=10,row=10,pady=2,padx=2)
    h7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h7.grid(column=10,row=11,pady=2,padx=2)
    h8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h8.grid(column=10,row=12,pady=2,padx=2)
    h9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h9.grid(column=10,row=13,pady=2,padx=2)
    h10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h10.grid(column=10,row=14,pady=2,padx=2)
    h11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h11.grid(column=10,row=15,pady=2,padx=2)
    h12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    h12.grid(column=10,row=16,pady=2,padx=2)

    a=Label(frame8,text="A",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    a.grid(row=4,column=11,padx=5,pady=5)

    a1=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a1.grid(column=11,row=5,pady=2,padx=2)
    a2=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a2.grid(column=11,row=6,pady=2,padx=2)
    a3=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a3.grid(column=11,row=7,pady=2,padx=2)
    a4=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a4.grid(column=11,row=8,pady=2,padx=2)
    a5=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a5.grid(column=11,row=9,pady=2,padx=2)
    a6=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a6.grid(column=11,row=10,pady=2,padx=2)
    a7=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a7.grid(column=11,row=11,pady=2,padx=2)
    a8=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a8.grid(column=11,row=12,pady=2,padx=2)
    a9=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a9.grid(column=11,row=13,pady=2,padx=2)
    a10=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a10.grid(column=11,row=14,pady=2,padx=2)
    a11=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a11.grid(column=11,row=15,pady=2,padx=2)
    a12=Entry(frame8,width=2,state="readonly",font=("Calibri", 11,"bold"))
    a12.grid(column=11,row=16,pady=2,padx=2)

    iode=Label(frame8,width=12,text="IODE",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    iode.grid(row=4,column=12,padx=10,pady=10)

    iode1=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode1.grid(column=12,row=5,pady=2,padx=2)
    iode2=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode2.grid(column=12,row=6,pady=2,padx=2)
    iode3=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode3.grid(column=12,row=7,pady=2,padx=2)
    iode4=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode4.grid(column=12,row=8,pady=2,padx=2)
    iode5=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode5.grid(column=12,row=9,pady=2,padx=2)
    iode6=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode6.grid(column=12,row=10,pady=2,padx=2)
    iode7=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode7.grid(column=12,row=11,pady=2,padx=2)
    iode8=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode8.grid(column=12,row=12,pady=2,padx=2)
    iode9=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode9.grid(column=12,row=13,pady=2,padx=2)
    iode10=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode10.grid(column=12,row=14,pady=2,padx=2)
    iode11=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode11.grid(column=12,row=15,pady=2,padx=2)
    iode12=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode12.grid(column=12,row=16,pady=2,padx=2)

    pr=Label(frame8,width=12,text="PR(cm)",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    pr.grid(row=4,column=13,padx=10,pady=10)

    pr1=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr1.grid(column=13,row=5,pady=2,padx=2)
    pr2=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr2.grid(column=13,row=6,pady=2,padx=2)
    pr3=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr3.grid(column=13,row=7,pady=2,padx=2)
    pr4=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr4.grid(column=13,row=8,pady=2,padx=2)
    pr5=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr5.grid(column=13,row=9,pady=2,padx=2)
    pr6=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr6.grid(column=13,row=10,pady=2,padx=2)
    pr7=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr7.grid(column=13,row=11,pady=2,padx=2)
    pr8=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr8.grid(column=13,row=12,pady=2,padx=2)
    pr9=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr9.grid(column=13,row=13,pady=2,padx=2)
    pr10=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr10.grid(column=13,row=14,pady=2,padx=2)
    pr11=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr11.grid(column=13,row=15,pady=2,padx=2)
    pr12=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    pr12.grid(column=13,row=16,pady=2,padx=2)


    dr=Label(frame8,width=12,text="DR(m/s)",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    dr.grid(row=4,column=14,padx=10,pady=10)

    dr1=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr1.grid(column=14,row=5,pady=2,padx=2)
    dr2=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr2.grid(column=14,row=6,pady=2,padx=2)
    dr3=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr3.grid(column=14,row=7,pady=2,padx=2)
    dr4=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr4.grid(column=14,row=8,pady=2,padx=2)
    dr5=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr5.grid(column=14,row=9,pady=2,padx=2)
    dr6=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr6.grid(column=14,row=10,pady=2,padx=2)
    dr7=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr7.grid(column=14,row=11,pady=2,padx=2)
    dr8=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr8.grid(column=14,row=12,pady=2,padx=2)
    dr9=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr9.grid(column=14,row=13,pady=2,padx=2)
    dr10=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr10.grid(column=14,row=14,pady=2,padx=2)
    dr11=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr11.grid(column=14,row=15,pady=2,padx=2)
    dr12=Entry(frame8,width=12,state="readonly",font=("Calibri", 11,"bold"))
    dr12.grid(column=14,row=16,pady=2,padx=2)


    #======================================++++++++++++++
    frame11=LabelFrame(root,text='TABLE',bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame11.grid(row=1,column=3,pady=2,padx=2,sticky="nsew")

    Last_Reset_Time=Label(frame11,text="Last_Reset_Time:",font=("Calibri", 11,"bold"),bg='lavender')
    Last_Reset_Time.grid(row=1, column=0)
    lrt=Entry(frame11,width=12,state="readonly",font=("Calibri", 11,"bold"))
    lrt.grid(column=1,row=1,pady=2,padx=2)

    SVID_IODE=Label(frame11,text="SVID:",font=("Calibri", 11,"bold"),bg='lavender')
    SVID_IODE.grid(row=2, column=0)
    SI=Entry(frame11,width=12,state="readonly",font=("Calibri", 11,"bold"))
    SI.grid(column=1,row=2,pady=2,padx=2)

    iode=Label(frame11,text="IODE:",font=("Calibri", 11,"bold"),bg='lavender')
    iode.grid(row=3, column=0)
    iode=Entry(frame11,width=12,state="readonly",font=("Calibri", 11,"bold"))
    iode.grid(column=1,row=3,pady=2,padx=2)

    CRS=Label(frame11,text="CRS:",font=("Calibri", 11,"bold"),bg='lavender')
    CRS.grid(row=4, column=0)
    crs=Entry(frame11,width=12,state="readonly",font=("Calibri", 11,"bold"))
    crs.grid(column=1,row=4,pady=2,padx=2)

    odp=Label(frame11,text="ODP status:",font=("Calibri", 11,"bold"),bg='lavender')
    odp.grid(row=5, column=0)
    odp=Entry(frame11,width=12,state="readonly",font=("Calibri", 11,"bold"))
    odp.grid(column=1,row=5,pady=2,padx=2)

    phase_center=Label(frame11,text="Phase_center_Corr:",font=("Calibri", 11,"bold"),bg='lavender')
    phase_center.grid(row=6, column=0)
    phase_center=Entry(frame11,width=12,state="readonly",font=("Calibri", 11,"bold"))
    phase_center.grid(column=1,row=6,pady=2,padx=2)

    phase_center_sps=Label(frame11,text="Phase cen for SPS:",font=("Calibri", 11,"bold"),bg='lavender')
    phase_center_sps.grid(row=7, column=0)
    phase_center_sps=Entry(frame11,width=12,state="readonly",font=("Calibri", 11,"bold"))
    phase_center_sps.grid(column=1,row=7,pady=2,padx=2)

     # ===========================SA29 RAW INFO ======================

    frame15=LabelFrame(root,text="SA29_RAW_DATA",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame15.grid(row=4,column=0,padx=2, pady=2,sticky="w")

    raw=Label(frame15,text="HEX_DATA:",font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    raw.grid(row=0,column=0,padx=10,pady=10)
    raw_data=Entry(frame15,width=70,state="readonly",font=("Calibri", 15,"bold"))
    raw_data.grid(column=1,row=0,pady=2,padx=2)

    





    # ==================== TTF ====================================
    '''frame12 = LabelFrame(root, text="TTF",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )
    frame12.grid(row=3, column=3, padx=2, pady=2, sticky="new")

    TTF=Label(frame12,text="TTF:",font=("Calibri", 11,"bold"),bg='lavender')
    TTF.grid(row=0, column=0)
    ttf=Entry(frame12,width=20,state="readonly",font=("Calibri", 11,"bold"))
    ttf.grid(column=1,row=0,padx=2, pady=2)

    def reset_ttf():
        global TTF
        TTF = None
        ttf.config(text="TTF: --")
        print("TTF has been reset.")

    reset_ttf_button = Button(frame12, text="Reset TTF", command=reset_ttf, bg="lavender", font=("Arial", 9))
    reset_ttf_button.grid(row=0, column=2, padx=5, pady=2, sticky="w")'''

    # ========================== GRAPH ============================
    frame_cndr_plot = tk.LabelFrame(root, text="CNDR VS SVID PLOT",bg="lavender",
    fg="purple",
    font=("Calibri", 13, "bold"),
    relief="solid",         # makes edges visible(solid,ridge,raised,groove,sunken,flat)
    bd=2,                    # border thickness
    padx=2, pady=2         # internal padding simulates rounded spacing
    )

    frame_cndr_plot.grid(row=3, column=2, padx=2, pady=2, sticky="sw")



    frame_cndr_plot.grid_rowconfigure(0, weight=1)
    frame_cndr_plot.grid_columnconfigure(0, weight=1)

    fig_cndr = Figure(figsize=(5.2, 3.6), dpi=100)
    ax_cndr = fig_cndr.add_subplot(111)

    ax_cndr.set_title("CNDR Values")
    ax_cndr.set_xlabel("SVIDs")
    ax_cndr.set_ylabel("CNDR Values")
    ax_cndr.set_ylim(0, 60)
    ax_cndr.set_yticks([0, 10, 20, 30, 35, 40, 45, 50, 60])

    canvas_cndr = FigureCanvasTkAgg(fig_cndr, master=frame_cndr_plot)
    canvas_cndr.get_tk_widget().grid(row=0, column=0, sticky="SW")









    # === Footer Section inside scrollable area ===
    separator = Frame(window, bg="black", height=2)
    separator.grid(row=99, column=0, columnspan=40, sticky="ew", pady=(10, 0))

    footer_label = Label(
        window,
        text="@ 2025 ISRO @ OS3A Interface | Version 1.0",
        font=("Segoe UI", 10, "italic"),
        bg="purple",
        fg="white",
        pady=2
    )
    footer_label.grid(row=100, column=0, columnspan=20, sticky="nsew")


    root.grid_rowconfigure(0, weight=2)
    root.grid_rowconfigure(1, weight=2)
    root.grid_rowconfigure(2, weight=2)
    root.grid_rowconfigure(3, weight=2)
    root.grid_columnconfigure(0,weight=2)
    root.grid_columnconfigure(1,weight=2)
    root.grid_columnconfigure(2,weight=2)
    root.grid_columnconfigure(3,weight=2)
    baud_select()
    update_coms()
    canvas.create_window((0, 0), window=root, anchor="nw")
    root.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    #root.protocol("WM_DELETE_WINDOW",close_window)
    root.mainloop()
def connect_check(args):
    global clicked_bd,clicked_com
    if "-" in clicked_com.get() or "-" in clicked_bd.get():
        connect_btn["state"]="disabled"
    else:
         connect_btn["state"]="active"
def baud_select():
    global clicked_bd,drop_bd,frame1,StringVar,OptionMenu
    clicked_bd=StringVar()
    bds = ["-",
           "300",
           "600",
           "1200",
           "2400",
           "4800",
           "9600",
           "14400",
           "19200",
           "28800",
           "38400",
           "56000",
           "57600",
           "115200",
           "128000",
           "256000"]
    clicked_bd.set("115200")
    drop_bd = OptionMenu(frame1, clicked_bd, *bds, command=connect_check)
    drop_bd.config(height=1,width=10,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    drop_bd.grid(column=4, row=1, padx=2,pady=2)
def update_coms():
    global clicked_com,drop_COM, frame1
    ports=serial.tools.list_ports.comports()
    coms=[com[0] for com in ports]
    coms.insert(0,"-")
    try:
        drop_COM.destroy()
    except:
        pass
    clicked_com=StringVar()
    clicked_com.set(coms[0])
    drop_COM=OptionMenu(frame1, clicked_com, *coms, command=connect_check)
    drop_COM.config(height=1,width=10,font=("Calibri", 11,"bold"),bg="lavender",fg="purple")
    drop_COM.grid(column=1,row=1,padx=2,pady=2)
    connect_check(0)


def reverse_and_concatenate(hex_list, scale=1, is_signed=False):
    if len(hex_list) in [1, 2, 3, 4, 8]:
        if len(hex_list) in [1, 2, 3]:
            concatenated_hex = ''.join(hex_list)
            decimal_value = int(concatenated_hex, 16)

        elif len(hex_list) == 4:
            first_half = ''.join(hex_list[:2])
            second_half = ''.join(hex_list[2:])
            concatenated_hex = second_half + first_half
            decimal_value = int(concatenated_hex, 16)

        elif len(hex_list) == 8:
            first_half = ''.join(hex_list[:4])
            second_half = ''.join(hex_list[4:])
            reversed_first_half = first_half[6:8] + first_half[4:6] + first_half[2:4] + first_half[0:2]
            reversed_second_half = second_half[6:8] + second_half[4:6] + second_half[2:4] + second_half[0:2]
            concatenated_hex = reversed_first_half + reversed_second_half
            decimal_value = int(concatenated_hex, 16)

        # Handle signed two's complement
        if is_signed:
            if decimal_value >= 0x80000000:
                decimal_value -= 0x100000000 # Adjust for signed value

        return decimal_value

    return None
def split_hex_string(hex_str):
    return [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]


'''def reverse_and_concatenate(hex_list, scale=1 ,is_signed=False):
    # Ensure the length of hex_list is valid for conversion
    if len(hex_list) in [1, 2, 3, 4, 8]:
        if len(hex_list) == 1:
            concatenated_hex = ''.join(hex_list)
            decimal_value = int(concatenated_hex, 16)
        elif len(hex_list) == 2:
            concatenated_hex = ''.join(hex_list)
            decimal_value = int(concatenated_hex, 16)

        elif len(hex_list) == 3:
            concatenated_hex = ''.join(hex_list)
            decimal_value = int(concatenated_hex, 16)

        elif len(hex_list) == 4:
            first_half = ''.join(hex_list[:2])
            second_half = ''.join(hex_list[2:])
            concatenated_hex = second_half + first_half
            decimal_value = int(concatenated_hex, 16)

        elif len(hex_list) == 8:
            first_half = ''.join(hex_list[:4])
            second_half = ''.join(hex_list[4:])
            reversed_first_half = first_half[6:8] + first_half[4:6] + first_half[2:4] + first_half[0:2]
            reversed_second_half = second_half[6:8] + second_half[4:6] + second_half[2:4] + second_half[0:2]
            concatenated_hex = reversed_first_half + reversed_second_half
            decimal_value = int(concatenated_hex, 16)

        # Handle signed values
        if is_signed:
            if decimal_value >= 0x80000000:
                decimal_value -= 0x100000000  # Adjust for signed value

        return decimal_value

    return None

def check_and_store_TTF(EST_x, EST_y, EST_z, SYN_Second, SYN_NanoSecond, SYN_Weeknumber, UpdateCounter):
    global TTF
    if TTF is None:
        if all(val != 0 for val in [EST_x, EST_y, EST_z, SYN_Second, SYN_NanoSecond, SYN_Weeknumber]):
            TTF = UpdateCounter
            print(f"TTF stored: {TTF}")'''

def convert_to_decimal(hex_str):
    reversed_hex = ''.join([hex_str[i:i+2]for i in range(0,len(hex_str),2)][::-1])
    return int(reversed_hex,16)
def chechsum_calulation_covert_decimal(NanoSecond_hex,Second_hex,Weeknumber_hex,CHECKSUM):
    global checksum
    NanoSecond_part1 = convert_to_decimal(NanoSecond_hex[:4])
    NanoSecond_part2 = convert_to_decimal(NanoSecond_hex[4:])
    Second_part1 = convert_to_decimal(Second_hex[:4])
    Second_part2 = convert_to_decimal(Second_hex[4:])
    Week = convert_to_decimal(Weeknumber_hex)
    total = NanoSecond_part1+NanoSecond_part2+Second_part1+Second_part2+Week
    exepected_checksum = (0-total) & 0xFFFF

    #print(exepected_checksum)
    #print(CHECKSUM)
    if exepected_checksum == CHECKSUM:

        checksum = "Pass"
        csm.config(fg="dark green")
    else:
        checksum =  "Fail"
        csm.config(fg="dark red")
    return checksum

def SA4chechsum_calulation_covert_decimal(SYS_NanoSecond_hex,SYS_Second_hex,SYS_Weeknumber_hex,SPS_x,SPS_y,SPS_z,SPS_vx,SPS_vy,SPS_vz,UpdateCounter_hex,INT_x_hex ,INT_y_hex ,INT_z_hex ,INT_vx_hex ,INT_vy_hex ,INT_vz_hex ,validation_flag_hex,CHECKSUM1):
    global checksum1
    SYS_NanoSecond_part1 = convert_to_decimal(SYS_NanoSecond_hex[:4])
    SYS_NanoSecond_part2 = convert_to_decimal(SYS_NanoSecond_hex[4:])
    SYS_Second_part1 = convert_to_decimal(SYS_Second_hex[:4])
    SYS_Second_part2 = convert_to_decimal(SYS_Second_hex[4:])
    SYS_Weeknumber = convert_to_decimal(SYS_Weeknumber_hex)
    SPS_x_part1 = convert_to_decimal(SPS_x[:4])
    SPS_x_part2 = convert_to_decimal(SPS_x[4:])
    SPS_y_part1 = convert_to_decimal(SPS_y[:4])
    SPS_y_part2 = convert_to_decimal(SPS_y[4:])
    SPS_z_part1 = convert_to_decimal(SPS_z[:4])
    SPS_z_part2 = convert_to_decimal(SPS_z[4:])
    SPS_vx_part1 = convert_to_decimal(SPS_vx[:4])
    SPS_vx_part2 = convert_to_decimal(SPS_vx[4:])
    SPS_vy_part1 = convert_to_decimal(SPS_vy[:4])
    SPS_vy_part2 = convert_to_decimal(SPS_vy[4:])
    SPS_vz_part1 = convert_to_decimal(SPS_vz[:4])
    SPS_vz_part2 = convert_to_decimal(SPS_vz[4:])
    UpdateCounter_part = convert_to_decimal(UpdateCounter_hex)
    INT_x_part1 = convert_to_decimal(INT_x_hex [:4])
    INT_x_part2 = convert_to_decimal(INT_x_hex [4:])
    INT_y_part1 = convert_to_decimal(INT_y_hex [:4])
    INT_y_part2 = convert_to_decimal(INT_y_hex [4:])
    INT_z_part1 = convert_to_decimal(INT_z_hex [:4])
    INT_z_part2 = convert_to_decimal(INT_z_hex [4:])
    INT_vx_part1 = convert_to_decimal(INT_vx_hex [:4])
    INT_vx_part2 = convert_to_decimal(INT_vx_hex [4:])
    INT_vy_part1 = convert_to_decimal(INT_vy_hex [:4])
    INT_vy_part2 = convert_to_decimal(INT_vy_hex [4:])
    INT_vz_part1 = convert_to_decimal(INT_vz_hex [:4])
    INT_vz_part2 = convert_to_decimal(INT_vz_hex [4:])
    Validation_part = convert_to_decimal(validation_flag_hex)


    total = SYS_NanoSecond_part1+SYS_NanoSecond_part2+SYS_Second_part1+SYS_Second_part2+SYS_Weeknumber+SPS_x_part1+SPS_x_part2+SPS_y_part1+SPS_y_part2+SPS_z_part1+SPS_z_part2+SPS_vx_part1+SPS_vx_part2+SPS_vy_part1+SPS_vy_part2+SPS_vz_part1+SPS_vz_part2+UpdateCounter_part+INT_x_part1+INT_x_part2+INT_y_part1+INT_y_part2+INT_z_part1+INT_z_part2+INT_vx_part1+INT_vx_part2+INT_vy_part1+INT_vy_part2+INT_vz_part1+INT_vz_part2+Validation_part

    exepected_checksum = (0-total) & 0xFFFF
    #print(exepected_checksum)
    #print(CHECKSUM1)

    if exepected_checksum == CHECKSUM1:

        checksum1 = "Pass"
        csm1.config(fg="dark green")
    else:
        checksum1 =  "Fail"
        csm1.config(fg="dark red")
    return checksum1

def decode_validation_flag(validation_flag):

    # Convert to integer if needed
    if isinstance(validation_flag, str):
        validation_flag = int(validation_flag, 16)
    elif isinstance(validation_flag, tuple):
        validation_flag = (validation_flag[0] << 8) | validation_flag[1]
    elif not isinstance(validation_flag, int):
        raise ValueError("Input must be int, hex string, or (MSB, LSB) tuple")

    #raw_flag = validation_flag
    B1_B0 = validation_flag & 0x03
    #B3_B2 = (validation_flag >> 2) & 0x03

    # Decode EKF level/orbit status
    if B1_B0 == 0b00:
        orbit_status = "NO SOL, 0"
    elif B1_B0 == 0b01:
        orbit_status = "ESTIMATED, 1"
    elif B1_B0 == 0b10:
        orbit_status = "INSTANTANEOUS, 2"
    elif B1_B0 == 0b11:
        orbit_status = "PROPAGATED, 3"
    else:
        orbit_status = "Unknown EKF level"

    # ODP run mode
    #odp_run_mode = B3_B2

    # EKF level (same as B1_B0)
    #ekf_level = B1_B0

    # OD&P state vectors usability
    #odp_vectors_usable = B1_B0 in [0b01, 0b11]

    return orbit_status

    '''return {
        'odp': orbit_status,
        'val': format(B1_B0, '02b'),
        #'ODP_run_mode': odp_run_mode,
        #'EKF_level': ekf_level,
        #'ODP_vectors_usable': odp_vectors_usable,
        #'B3_B2_bin': format(B3_B2, '02b'),
        #'raw_flag': raw_flag
    }'''

def Multiplexing(word31):
    """
    Decodes the multiplexed Word #31 and returns a clean output string.
    Also stores decoded values in global 'decoded_data' dictionary.

    Args:
        word31 (int, hex str, or (MSB, LSB) tuple)

    Returns:
        str: A formatted output like:
             - "MUX: 0 : 1200"
             - "MUX: 11 : NavIC Cmd=45, GPS_alm_chk=12"
             - "MUX: 12 : P2E=2, ALM_usel=17, ALM_col=6"
    """
    global decoded_data

    # Convert input to 16-bit integer
    if isinstance(word31, str):
        word31 = int(word31, 16)
    elif isinstance(word31, tuple):
        word31 = (word31[0] << 8) | word31[1]
    elif not isinstance(word31, int):
        raise ValueError("Input must be int, hex string, or (MSB, LSB) tuple")

    mux_sel = (word31 >> 12) & 0xF  # Bits B15–B12
    data = word31 & 0xFFF           # Bits B11–B0

    decoded_data = {'Selector': mux_sel}

    # Define per selector
    if mux_sel == 0:
        decoded_data['Acq threshold'] = data
        return f"MUX: {mux_sel} : {data}  (Acq threshold)"
    elif mux_sel == 1:
        decoded_data['Trk threshold'] = data
        return f"MUX: {mux_sel} : {data}  (Trk threshold)"
    elif mux_sel == 2:
        decoded_data['Search reg 12 bits [b31-b24]'] = data
        return f"MUX: {mux_sel} : {data}  (Write SVID Search)"
    elif mux_sel == 3:
        decoded_data['Search reg 12 bits [b23-b12]'] = data
        return f"MUX: {mux_sel} : {data}  (Write SVID Search)"
    elif mux_sel == 4:
        decoded_data['SW Version'] = data
        return f"MUX: {mux_sel} : {data} (Dummy)"
    elif mux_sel == 5:
        decoded_data['uialm_cpy-cnt'] = data
        return f"MUX: {mux_sel} : {data} (Dummy)"
    elif mux_sel == 6:
        decoded_data['Search reg 8 bits [b11-b0]'] = data & 0xFF
        return f"MUX: {mux_sel} : {data & 0xFF} (Write SVID Search)"
    elif mux_sel == 7:
        decoded_data['alm_av_flag 16'] = data
        return f"MUX: {mux_sel} : {data} (Alm flag AV)"
    elif mux_sel == 8:
        decoded_data['alm+ctr_24'] = data
        return f"MUX: {mux_sel} : {data} (Alm availablity ctrl)"
    elif mux_sel == 9:
        decoded_data['CCSDS Spacecraft ID'] = data
        return f"MUX: {mux_sel} : {data}  (S/C ID)"
    elif mux_sel == 10:
        decoded_data['Elevation angle Threshold'] = data
        return f"MUX: {mux_sel} : {data} (Elev Threshold)"
    elif mux_sel == 11:
        navic_cmd = data & 0x7F
        gps_chk = (data >> 7) & 0x1F
        decoded_data['NavIC Cmd sat'] = navic_cmd
        decoded_data['Stored GPS alm_ucAlm_num_chk'] = gps_chk
        return f"MUX: {mux_sel} : NavIC Cmd={navic_cmd}, GPS_alm_chk={gps_chk}"
    elif mux_sel == 12:
        p2e = (data >> 10) & 0x03
        alm_usel = (data >> 5) & 0x1F
        alm_col = data & 0x1F
        decoded_data['P2E_3bits'] = p2e
        decoded_data['GPS_ALM_usel'] = alm_usel
        decoded_data['GPS_ALM_collected'] = alm_col
        return f"MUX: {mux_sel} : P2E={p2e}, ALM_usel={alm_usel}, ALM_col={alm_col}"
    else:
        decoded_data['Reserved/Unknown'] = data
        return f"MUX: {mux_sel} : {data} (Reserved)"


def decode_wdt_status_word(status_word):
    """
    Decodes the 16-bit WDT status and command counter word.

    Args:
        status_word (int, str, or tuple): A 16-bit unsigned int, hex string, or (high_byte, low_byte)

    Returns:
        dict: Decoded fields with descriptive labels.
    """
    if isinstance(status_word, str):
        status_word = int(status_word, 16)
    elif isinstance(status_word, tuple):
        status_word = (status_word[0] << 8) | status_word[1]
    elif not isinstance(status_word, int):
        raise ValueError("Input must be int, hex string, or (high_byte, low_byte) tuple")

    result = {}

    # Bits B15–B10: 6-bit Valid 1553 Command Counter
    result["Valid 1553 CMD CTR"] = (status_word >> 10) & 0x3F

    # Bit B9: TM selection
    result["TM Selection"] = "TM2" if (status_word >> 9) & 1 else "TM1"

    # Bit B8: SW line/SW WDT status
    b8 = (status_word >> 8) & 1
    result["SW Line/WDT Status"] = (
        "Disabled" if b8
        else "Enabled "
    )

    # Bit B7: HW WDT status
    result["HW WDT Status"] = "Disabled" if (status_word >> 7) & 1 else "Enabled"

    # Bit B6: MNV ON/OFF
    result["MNV Status"] = "Disabled" if (status_word >> 6) & 1 else "Enabled"

    # Bit B4: SPS Software Status
    result["SPS Software Status"] = "PROM Mode" if (status_word >> 4) & 1 else "EEPROM Mode"

    return result


def decode_system_mode_status(system_flag):
    """
    Decodes the 16-bit system mode and status flag.
    """
    if isinstance(system_flag, str):
        system_flag = int(system_flag, 16)
    elif isinstance(system_flag, tuple):
        system_flag = (system_flag[0] << 8) | system_flag[1]
    elif not isinstance(system_flag, int):
        raise ValueError("Input should be an integer, hex string, or tuple")

    flags = {
        "Iono Smoothing": "Enabled" if (system_flag >> 13) & 1 else "Disabled",
        "INONO Enable": "Enabled" if (system_flag >> 12) & 1 else "Disabled",
        "GP2015 Lock": "Locked" if (system_flag >> 11) & 1 else "Unlocked",
        "RFFC5071 Lock": "Locked" if (system_flag >> 10) & 1 else "Unlocked",
        "Nav 1A": "Enabled" if (system_flag >> 9) & 1 else "Disabled",
        "Velocity Smoothing": "Enabled" if (system_flag >> 8) & 1 else "Disabled",
        "GPS2015 Ant2 Lock": "Locked" if (system_flag >> 7) & 1 else "Unlocked",
        "RAIM": "Enabled" if (system_flag >> 6) & 1 else "Disabled",
        "Carrier Smoothing": "Enabled" if (system_flag >> 5) & 1 else "Disabled",
    }

    # System Mode (B4–B2)
    system_mode_val = (system_flag >> 2) & 0b111
    system_mode_map = {
        0b001: "GPS + NAVIC + SBAS",
        0b010: "GPS + NAVIC",
        0b011: "NAVIC only",
        0b100: "GPS + SBAS",
        0b101: "GPS only"
    }
    flags["System Mode"] = system_mode_map.get(system_mode_val, f"Unknown ({system_mode_val:03b})")

    # Time alignment system (B1)
    flags["Time Aligned To"] = "NavIC" if (system_flag >> 1) & 1 else "GPS"

    return flags

def decode_word25(word25):
    """
    Decodes HWDT Reset Counter, SWDT Reset ID, and PB Storage Mode from a 16-bit word.

    Args:
        word25 (int, str, or tuple): 16-bit word (int), hex string, or (MSB, LSB) tuple.

    Returns:
        dict: Decoded values
    """
    if isinstance(word25, str):
        word25 = int(word25, 16)
    elif isinstance(word25, tuple):
        word25 = (word25[0] << 8) | word25[1]
    elif not isinstance(word25, int):
        raise ValueError("Input must be int, hex string, or (MSB, LSB) tuple")

    result = {}
    result["HWDT Reset Counter"] = (word25 >> 8) & 0xFF
    result["SWDT Reset ID"] = word25 & 0x0F
    pb_storage_mode_code = (word25 >> 4) & 0x0F

    pb_storage_mode_map = {
        1: "1s", 2: "2s", 5: "5s", 10: "10s"
    }
    result["PB Storage Mode"] = pb_storage_mode_map.get(pb_storage_mode_code, f"Unknown ({pb_storage_mode_code})")
    return result

def decode_sa9word32(word32):
    """
    Decodes HWDT Reset Counter, SWDT Reset ID, and PB Storage Mode from a 16-bit word.

    Args:
        word25 (int, str, or tuple): 16-bit word (int), hex string, or (MSB, LSB) tuple.

    Returns:
        dict: Decoded values
    """
    if isinstance(word32, str):
        word32 = int(word32, 16)
    elif isinstance(word32, tuple):
        word32 = (word32[0] << 8) | word32[1]
    elif not isinstance(word32, int):
        raise ValueError("Input must be int, hex string, or (MSB, LSB) tuple")

    result = {}
    result["Str_Est"] = word32 & 0x3
    result["Str_En"] = "Enabled" if (word32 >> 2) & 0x1 else "Disabled"
    result["Reset_C"] = (word32 >> 3) & 0x7
    result["Init"] = "Enabled" if (word32 >> 6) & 0x1 else "Disabled"

    return result

def odp_parameter(word1):
    """
    Decodes HWDT Reset Counter, SWDT Reset ID, and PB Storage Mode from a 16-bit word.

    Args:
        word25 (int, str, or tuple): 16-bit word (int), hex string, or (MSB, LSB) tuple.

    Returns:
        dict: Decoded values
    """
    if isinstance(word1, str):
        word1 = int(word1, 16)
    elif isinstance(word1, tuple):
        word1 = (word1[0] << 8) | word1[1]
    elif not isinstance(word1, int):
        raise ValueError("Input must be int, hex string, or (MSB, LSB) tuple")

    odp_par = {
   "No of I/P sat to odp" :(word1 & 0xF000) >> 12,
   "No of sat est" :(word1 & 0x0F00) >> 8,
   "Filter Init reason" :(word1 & 0x00F0) >> 4,
   "Filter Init Flag" :"Enabled" if (word1 >> 3) & 1 else "Disabled",
   "KF Est Flag" :"Enabled" if (word1 >> 2) & 1 else "Disabled",
   "PPP Est Flag Unsing" :"Enabled" if (word1 >> 1) & 1 else "Disabled",
   "Ph_center En Flag" :"Enabled" if word1  & 1 else "Disabled",

    }
    return odp_par

def decode_word15(word15):
    """
    Decodes Telecommand interrupt counter and number of satellites tracked from a 16-bit word.

    Args:
        word15 (int, str, or tuple): 16-bit unsigned int, hex string, or (MSB, LSB) tuple

    Returns:
        dict: Decoded values
    """
    if isinstance(word15, str):
        word15 = int(word15, 16)
    elif isinstance(word15, tuple):
        word15 = (word15[0] << 8) | word15[1]
    elif not isinstance(word15, int):
        raise ValueError("Input must be int, hex string, or (MSB, LSB) tuple")

    result = {}
    result["Interupt CMD Counter"] = (word15 >> 5) & 0x7FF  # 11 bits: B15-B5
    result["No Of Satellite"] = word15 & 0x1F           # 5 bits: B4-B0
    return result



def open_popup():
    popup = tk.Toplevel()
    popup.title("Commands")
    popup.geometry("300x300")

    popup.grid_rowconfigure(1, weight=1)
    popup.grid_columnconfigure(0, weight=1)

    search_var = tk.StringVar()

    search_entry = tk.Entry(popup, textvariable=search_var, fg="blue")
    search_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    search_entry.insert(0, " ")

    text_area = tk.Text(popup, wrap=tk.WORD, height=10)
    text_area.grid(row=1, column=0, sticky="nsew", padx=(5,0), pady=(0,5))

    scrollbar = tk.Scrollbar(popup, command=text_area.yview)
    scrollbar.grid(row=1, column=1, sticky="ns", pady=(0,5))
    text_area.config(yscrollcommand=scrollbar.set)

    def highlight(term):
        text_area.tag_remove("highlight", "1.0", tk.END)
        if not term:
            return
        start = "1.0"
        while True:
            pos = text_area.search(term, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(term)}c"
            text_area.tag_add("highlight", pos, end)
            start = end
        text_area.tag_config("highlight", background="yellow")

    def display_commands():
        term = search_var.get().strip().lower()
        text_area.delete("1.0", tk.END)
        for cmd, desc in commands.items():
            combined = f"{cmd}: {desc}".lower()
            if term in combined:
                text_area.insert(tk.END, f"{cmd}: {desc}\n")
        highlight(term)

    def on_focus_in(event):
        if search_entry.get() == "Search cmd":
            search_entry.delete(0, tk.END)
            search_entry.config(fg="black")

    def on_focus_out(event):
        if not search_entry.get():
            search_entry.insert(0, "Search cmd")
            search_entry.config(fg="grey")

    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)
    search_entry.bind("<KeyRelease>", lambda e: display_commands())

    display_commands()



def send_general_command(data_str, cmd_type):
    global sa3_thread, sa3_running, sa4_thread, sa4_running

    if not (ser and ser.is_open):
        status_var.set("❌ Serial port not open.")
        return

    if cmd_type in ("SA3", "SA4"):
        filepath = file_entries[cmd_type].get()
        if not filepath or not os.path.exists(filepath):
            status_var.set(f"❌ Please select a valid file for {cmd_type} commands.")
            return

        if cmd_type == "SA3":
            if sa3_thread and sa3_thread.is_alive():
                status_var.set("❌ SA3 sending already running!")
                return
            sa3_running = True
            sa3_thread = threading.Thread(target=send_sax_from_file, args=(filepath, 0.128, cmd_type), daemon=True)
            sa3_thread.start()
            status_var.set("▶️ SA3 sending started.")
        else:  # SA4
            if sa4_thread and sa4_thread.is_alive():
                status_var.set("❌ SA4 sending already running!")
                return
            sa4_running = True
            sa4_thread = threading.Thread(target=send_sax_from_file, args=(filepath, 1.0, cmd_type), daemon=True)
            sa4_thread.start()
            status_var.set("▶️ SA4 sending started.")
        return

    # SA1 and SA2 manual send
    try:
        parts = data_str.strip().split()
        if len(parts) != 3:
            status_var.set("❌ Enter exactly 3 words (e.g. 0x0000 0x0004 0x0055)")
            return

        words = [int(word, 16) for word in parts]

        if cmd_type == "SA1":
            header = [0xAC, 0xCA, 0x1F, 0x01]
        elif cmd_type == "SA2":
            header = [0xAC, 0xCA, 0x1F, 0x02]
        else:
            status_var.set("❌ Unknown subaddress type!")
            return

        data_bytes = [b for word in words for b in word.to_bytes(2, byteorder='big')]
        full_packet = header + data_bytes

        ser.write(bytes(full_packet))
        sent_str = f"Manual {cmd_type} command sent: {[f'0x{b:02X}' for b in full_packet]}"
        status_var.set(f"✅ {sent_str}")
        print(sent_str)
        with open("(SA1-SA4)command_log.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | MANUAL {cmd_type} | {sent_str}\n")

    except ValueError:
        status_var.set("❌ Invalid hex format. Use e.g. 0x0000 0x0004 0x0055")
    except Exception as e:
        status_var.set(f"❌ Error sending manual command: {e}")

def send_sax_from_file(filepath, interval, cmd_type):
    global sa3_running, sa4_running

    try:
        with open(filepath, 'rb') as f:
            raw = f.read()

        try:
            as_text = raw.decode('ascii')
            hexstr = ''.join(c for c in as_text if c in '0123456789abcdefABCDEF')
            file_bytes = bytes.fromhex(hexstr)
        except Exception:
            file_bytes = raw

        if len(file_bytes) < 64:
            status_var.set(f"❌ File must contain at least 64 bytes of data for {cmd_type}.")
            if cmd_type == "SA3":
                sa3_running = False
            else:
                sa4_running = False
            return

        header = [0xAC, 0xCA, 0x1F, 0x03] if cmd_type == "SA3" else [0xAC, 0xCA, 0x1F, 0x04]
        num_blocks = len(file_bytes) // 64

        idx = 0

        while (sa3_running if cmd_type == "SA3" else sa4_running) and ser and ser.is_open:
            start = idx * 64
            end = start + 64
            if end > len(file_bytes):
                if cmd_type == "SA3":
                    sa3_running = False
                else:
                    sa4_running = False
                status_var.set(f"⏹️ {cmd_type} sending finished.")
                break

            chunk = file_bytes[start:end]
            packet = bytes(header) + chunk
            ser.write(packet)

            sent_str = f"{cmd_type} packet sent (block {idx+1}/{num_blocks}): {[f'0x{b:02X}' for b in packet]}"
            status_var.set(f"✅ {sent_str}")
            print(sent_str)
            with open("(SA1-SA4)command_log.txt", "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {cmd_type} | {sent_str}\n")

            idx += 1
            for _ in range(int(interval * 1000 / 10)):
                if not (sa3_running if cmd_type == "SA3" else sa4_running):
                    status_var.set(f"⏹️ {cmd_type} sending stopped.")
                    return
                cmdtime.sleep(0.01)

    except Exception as e:
        status_var.set(f"❌ Error in {cmd_type} send: {e}")
        if cmd_type == "SA3":
            sa3_running = False
        else:
            sa4_running = False
def stop_sa3():
    global sa3_running
    if sa3_running:
        sa3_running = False
        status_var.set("⏹️ Stopping SA3 sending...")

def stop_sa4():
    global sa4_running
    if sa4_running:
        sa4_running = False
        status_var.set("⏹️ Stopping SA4 sending...")

# GUI Entries storage
manual_entries = {}
file_entries = {}


def on_bus_toggle(*args):
    try:
        if not (ser and ser.is_open):
            status_var.set("❌ Serial port not open.")
            return
        if bus_var.get() not in ["A", "B"]:
            return
        header = [0xAC, 0xCA, 0x1F, 0x0B]
        rt_address = 0x00
        bus_val = 0x78 if bus_var.get() == "A" else 0x77
        packet = header + [rt_address, bus_val]
        bus_name = "BUS A" if bus_val == 0x78 else "BUS B"
        ser.write(bytes(packet))
        sent_str = f"Packet for toggle: {[f'0x{b:02X}' for b in packet]} ({bus_name})"
        status_var.set(sent_str)
        with open("Buscmd.txt", "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | BUS_TOGGLE | {sent_str}\n")
    except Exception as e:
        status_var.set(f"❌ Error sending bus command (button): {e}")

'''def show_bus_toggle_packet():
    try:
        if not (ser and ser.is_open):
            status_var.set("❌ Serial port not open.")
            return
        header = [0xAC, 0xCA, 0x1F, 0x0B]
        rt_address = 0x00
        bus_val = 0x78 if bus_var.get() == "A" else 0x77
        packet = header + [rt_address, bus_val]
        bus_name = "BUS A" if bus_val == 0x78 else "BUS B"
        ser.write(bytes(packet))
        sent_str = f"Packet for toggle: {[f'0x{b:02X}' for b in packet]} ({bus_name})"
        status_var.set(sent_str)
        with open("Buscmd.txt", "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | BUSCMD_TOGGELE | {sent_str}\n")
    except Exception as e:
        status_var.set(f"❌ Error sending bus command (button): {e}")'''


def send_bus_command_button(cmd_value=None):
    """
    For preset bus command buttons: HEADER + RT Address (0x00) + Dataword
    """
    try:
        if not (ser and ser.is_open):
            status_var.set("❌ Serial port not open.")
            return
        rt_address = 0x00  # always 0x00 for buttons
        if cmd_value is not None:
            data_word = cmd_value
            cmd_name = [k for k, v in bus_commands if v == cmd_value][0]
        else:
            status_var.set("❌ Command value not provided.")
            return
        header = [0xAC, 0xCA, 0x1F, 0x0B]
        packet = header + [rt_address, data_word]
        ser.write(bytes(packet))
        sent_str = f"Sent (Button): {[f'0x{b:02X}' for b in packet]}  ({cmd_name}, RT=0x00, Data=0x{data_word:02X})"
        status_var.set(f"✅ {sent_str}")
        print(sent_str)
        with open("Buscmd.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | BUSCMD_BTN | {sent_str}\n")
    except Exception as e:
        status_var.set(f"❌ Error sending bus command (button): {e}")

def send_bus_command_entry():
    """
    For manual entry: HEADER + Entered Dataword + RT Address (0xCE)
    """
    try:
        if not (ser and ser.is_open):
            status_var.set("❌ Serial port not open.")
            return
        rt_address = 0xCE  # always 0xCE for entry/manual
        dataword_str = dataword_entry.get().strip()
        if dataword_str.lower().startswith("0x"):
            data_word = int(dataword_str, 16)
        else:
            data_word = int(dataword_str, 16) if all(c in "0123456789abcdefABCDEF" for c in dataword_str) else int(dataword_str)
        if not (0 <= data_word <= 0xFF):
            status_var.set("❌ Data word must be 1 byte (00-FF)")
            return
        header = [0xAC, 0xCA, 0x1F, 0x0B]
        packet = header + [data_word, rt_address]
        sent_str = f"Sent (Entry): {[f'0x{b:02X}' for b in packet]}  (Manual Data=0x{data_word:02X}, RT=0xCE)"
        ser.write(bytes(packet))
        status_var.set(f"✅ {sent_str}")
        print(sent_str)
        with open("Buscmd.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | BUSCMD_ENTRY | {sent_str}\n")
    except Exception as e:
        status_var.set(f"❌ Error sending bus command (entry): {e}")

def get_timestamped_filename(base_name: str, suffix: str) -> str:
    """
    Generate consistent file name in format:
    OS3A_YYYY-MM-DD_HH-MM-SS_BASENAME_SUFFIX.csv

    Example:
    OS3A_2025-08-21_20-35-10_MYDATA_PVT.csv

    """
    global display_name
    return f"{display_name}_{SESSION_TIMESTAMP}_{base_name}_{suffix}.csv"
# =========================
# RAW DATA WITH HEADER LOGGING
# =========================
def write_to_raw_withheader1(data, base_name):
    file_name = get_timestamped_filename(base_name, "Raw1_withheader")
    header = ['TimeStamp','RAW DATA']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:   # write header only once
            writer.writerow(header)
        writer.writerow(data)

def write_to_raw_withheader2(data, base_name):
    file_name = get_timestamped_filename(base_name, "Raw2_withheader")
    header = ['TimeStamp','RAW DATA']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)

def write_to_raw_withheader3(data, base_name):
    file_name = get_timestamped_filename(base_name, "Raw3_withheader")
    header = ['TimeStamp','RAW DATA']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)

def write_to_raw_withheader4(data, base_name):
    file_name = get_timestamped_filename(base_name, "Raw4_withheader")
    header = ['TimeStamp','RAW DATA']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)


# =========================
# RAW DATA LOGGING
# =========================
def write_to_raw(data, base_name):
    file_name = get_timestamped_filename(base_name, "Raw")
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def write_to_rawh2(data, base_name):
    file_name = get_timestamped_filename(base_name, "Rawh2")
    header = ['TimeStamp','RAW DATA']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)

def write_to_rawh3(data, base_name):
    file_name = get_timestamped_filename(base_name, "Rawh3")
    header = ['TimeStamp','RAW DATA']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)

def write_to_rawh4(data, base_name):
    file_name = get_timestamped_filename(base_name, "Rawh4")
    header = ['TimeStamp','RAW DATA']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)


# =========================
# SYNC DATA LOGGING
# =========================
'''def write_to_SYN(data, base_name):
    file_name = get_timestamped_filename(base_name, "Sync")
    header = ['TimeStamp','SYN_SECOND','SYN_NANOSECOND','SYN_WEEKNUMBER']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)'''

def write_to_SYNh2(data, base_name):
    file_name = get_timestamped_filename(base_name, "Sync_Time")
    header = ['TimeStamp','h2SYN_SECOND','h2SYN_NANOSECOND','h2SYN_WEEKNUMBER']
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)


# =========================
# MAIN PVT DATA LOGGING
# =========================
def write_to_csv(data, base_name):
    file_name = get_timestamped_filename(base_name, "PVT")

    header = [
        'TimeStamp','SYS_Second','SYS_NanoSecond','SYS_WeekNumber',
        'PPS Sec','PPS NS','PPS WN','PPS 3D Fix',
        'INST_X','INST_Y','INST_Z','INST_VX','INST_VY','INST_VZ',
        'EST_X','EST_Y','EST_Z','EST_VX','EST_VY','EST_VZ',
        'UpdateCounter','Memory count','SPU cmd Counter','Upset cmd Counter',
        'Checksum SA2','Checksum SA4','Validation Flag','PDOP',
        'Clock bias','InterSystem bias','Drift','Inter System Drift','Steering Bias','Steering Drift','Streening Clock','U1','U2',
        'Last_cmd_B1_B2','Last_cmd_B3','Last_cmd_B4','ACQ1_SVID',
        'SWDT Reset Counter','Str_Est','Str_En','Reset_C','Initialization',
        'HWDT Reset Counter','SWDT Reset ID','PB Storage Mode',
        'Tele CMD Counter','No Of Satellite','Valid 1553 Command Counter',
        'TM Selection','SW Line/WDT Status','HW WDT Status','MNV Status',
        'SPS Software Status','Iono Smoothing','INONO Enable','GP2015 Lock',
        'RFFC5071 Lock','Nav 1A','Velocity Smoothing','GPS2015 Ant2 Lock',
        'RAIM','Carrier Smoothing','System Mode','Time Aligned To','Last_reset_time',
        'SVID','IODE','CRS','MUX','ODP Status','Phase center correction',
        'Phase center correction SPS','PORT1','PORT2','SOL','POS_E','ALM','TIME',
        'Pos Mode','POS','CCSDS','Randomzier','Spacecraft_id','Navic_cmd',
         'No of I/P sat to odp','No of sat est','Filter Init reason','Filter Init Flag',
        'KF Est Flag','PPP Est Flag Unsing','Ph_center En Flag',
        'TM_Ill_cond','TM_Ill_cond_lim','Cond_pre','Cond_post','Orbit_phase','odp_prop_use',


        # CH1 → CH12 details
        'CH1','SVID1','CNDR1','T','P','E','D','I','R','H','A','IODE1','Pr(cm)1','Dr(m/s)1',
        'CH2','SVID2','CNDR2','T','P','E','D','I','R','H','A','IODE2','Pr(cm)2','Dr(m/s)2',
        'CH3','SVID3','CNDR3','T','P','E','D','I','R','H','A','IODE3','Pr(cm)3','Dr(m/s)3',
        'CH4','SVID4','CNDR4','T','P','E','D','I','R','H','A','IODE4','Pr(cm)4','Dr(m/s)4',
        'CH5','SVID5','CNDR5','T','P','E','D','I','R','H','A','IODE5','Pr(cm)5','Dr(m/s)5',
        'CH6','SVID6','CNDR6','T','P','E','D','I','R','H','A','IODE6','Pr(cm)6','Dr(m/s)6',
        'CH7','SVID7','CNDR7','T','P','E','D','I','R','H','A','IODE7','Pr(cm)7','Dr(m/s)7',
        'CH8','SVID8','CNDR8','T','P','E','D','I','R','H','A','IODE8','Pr(cm)8','Dr(m/s)8',
        'CH9','SVID9','CNDR9','T','P','E','D','I','R','H','A','IODE9','Pr(cm)9','Dr(m/s)9',
        'CH10','SVID10','CNDR10','T','P','E','D','I','R','H','A','IODE10','Pr(cm)10','Dr(m/s)10',
        'CH11','SVID11','CNDR11','T','P','E','D','I','R','H','A','IODE11','Pr(cm)11','Dr(m/s)11',
        'CH12','SVID12','CNDR12','T','P','E','D','I','R','H','A','IODE12','Pr(cm)12','Dr(m/s)12'
    ]

    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(header)  # write header once
        writer.writerow(data)

# Plot update function

def update_cndr_plot_func(svid_labels, cndr_values):
    colors = []
    for val in cndr_values:
        if 30 <= val < 40:
            colors.append("orange")  # Mid range
        elif 40 <= val <= 60:
            colors.append("blue")   # High range
        else:
            colors.append("lightgray")  # Other values
    ax_cndr.clear()
    ax_cndr.set_title("CNDR Values")
    ax_cndr.set_xlabel("SVIDs")
    ax_cndr.set_ylabel("CNDR Values")
    ax_cndr.set_ylim(0, 60)
    ax_cndr.set_yticks([0, 10, 20, 30, 35, 40, 45, 50, 60])

    ax_cndr.bar(range(1, 13), cndr_values, color=colors,edgecolor='black')
    ax_cndr.set_xticks(range(1, 13))
    ax_cndr.set_xticklabels(svid_labels, rotation=45)

    canvas_cndr.draw_idle()


def refresh_cndr_plot():
    try:
        root.update_idletasks()  # make sure entries are updated

        cndr_list_values = [
            float(cndr1.get() or 0), float(cndr2.get() or 0), float(cndr3.get() or 0), float(cndr4.get() or 0),
            float(cndr5.get() or 0), float(cndr6.get() or 0), float(cndr7.get() or 0), float(cndr8.get() or 0),
            float(cndr9.get() or 0), float(cndr10.get() or 0), float(cndr11.get() or 0), float(cndr12.get() or 0)
        ]

        svid_labels = [
            svid1.get() or "CH1", svid2.get() or "CH2", svid3.get() or "CH3", svid4.get() or "CH4",
            svid5.get() or "CH5", svid6.get() or "CH6", svid7.get() or "CH7", svid8.get() or "CH8",
            svid9.get() or "CH9", svid10.get() or "CH10", svid11.get() or "CH11", svid12.get() or "CH12"
        ]

        update_cndr_plot_func(svid_labels, cndr_list_values)

    except Exception as e:
        print("CNDR plot update error:", e)

def readSerial():
    global serialData, ser, data_queue
    import collections

    # HEADER_INFO: header byte sequence (hex strings) and payload length (in bytes) AFTER the header
    HEADER_INFO = {
        "header1": (["ac", "ca", "1f", "0a"], 1026),
        "header2": (["ac", "ca", "1f", "0b"], 60),
        "header3": (["ac", "ca", "1f", "0c"], 1026),
        "header4": (["ac", "ca", "1f", "0d"], 1026),
    }

    # State: how many header bytes matched so far, current buffer, collecting flag, and target total length
    State = collections.namedtuple("State", ["match_index", "buffer", "collecting", "target_len"])
    state = {}
    for key, (hdr_seq, payload_len) in HEADER_INFO.items():
        target_len = len(hdr_seq) + payload_len  # total bytes to have: header + payload
        state[key] = State(0, bytearray(), False, target_len)

    try:
        while serialData:
            if ser.in_waiting > 0:
                b = ser.read(1)
                if not b:
                    continue
                b_hex = b.hex()  # two hex chars, lowercase

                for header_name, (header_seq, payload_len) in HEADER_INFO.items():
                    idx, buf, collecting, target_len = state[header_name]

                    # If currently collecting payload for this header, append the byte
                    if collecting:
                        buf += b
                        # When buffer reaches the target total length (header + payload) → packet complete
                        if len(buf) >= target_len:
                            data_hex = buf.hex().upper()  # make it uppercase for readability
                            print(f"{header_name.upper()} FOUND! {data_hex}")
                            # put tuple (header_type, hexString) on queue for processing
                            data_queue.put((header_name, data_hex))
                            # Reset this header state
                            state[header_name] = State(0, bytearray(), False, target_len)
                        else:
                            # keep collecting
                            state[header_name] = State(idx, buf, True, target_len)
                        continue

                    # Not collecting: try to match the header byte sequence
                    expected_byte = header_seq[idx]
                    if b_hex == expected_byte:
                        idx += 1
                        # If we've matched the full header sequence, start collecting payload
                        if idx == len(header_seq):
                            hdr_bytes = bytes.fromhex(''.join(header_seq))
                            buf = bytearray(hdr_bytes)  # include header bytes in buffer
                            state[header_name] = State(idx, buf, True, target_len)
                        else:
                            state[header_name] = State(idx, bytearray(), False, target_len)
                    else:
                        # If mismatch, check if this byte could be the start of the header (e.g., "ac")
                        if b_hex == header_seq[0]:
                            state[header_name] = State(1, bytearray(), False, target_len)
                        else:
                            state[header_name] = State(0, bytearray(), False, target_len)

    except KeyboardInterrupt:
        print("Reading from serial port stopped")
    except Exception as e:
        print("readSerial error:", e)



def process_data():
    global base_name,filename
    try:
        while True:


                            item = data_queue.get()
                            if not item:
                                continue
                            data_type,hexDecodedData = item
                            if data_type == "header1":

                                header_length = 10
                                Raw_data = ' '.join([hexDecodedData[i:i+2]for i in range(header_length,len(hexDecodedData),2)])
                                #formatted_data = ''.join([hexDecodedData[i:i+2]for i in range(0,len(without_header),2)])
                                #=================SUBADDRESS 2 STRAT====================
                                SYN_NanoSecond_hex=hexDecodedData[12:20] #SA2W1-W2
                                #print(f"SYN_NanoSecond_hex:{SYN_NanoSecond_hex}")
                                SYN_Second_hex=hexDecodedData[20:28] #SA2W3-W4
                                SYN_Weeknumber_hex=hexDecodedData[28:32] #SA2W5
                                CHECKSUM_hex = hexDecodedData[32:36] #SA2W6

                                #=====================SUBADDRESS 3 START=================
                                SYS_NanoSecond_hex=hexDecodedData[140:148]#SA3W1-W2
                                #print(f"\nSYS_NanoSecond_hex:{SYS_NanoSecond_hex}")
                                SYS_Second_hex=hexDecodedData[148:156]#SA3W3-W4
                                #print(SYS_Second_hex)
                                SYS_Weeknumber_hex=hexDecodedData[156:160]#SA3W5
                                #print(SYS_Weeknumber_hex)
                                SPS_x = hexDecodedData[160:168] #SA3W6-W7
                                #print(SPS_x)
                                SPS_y = hexDecodedData[168:176] #SA3W8-W9
                                #print(SPS_y)
                                SPS_z = hexDecodedData[176:184] #SA3W10-W11
                                #print(SPS_z)
                                SPS_vx = hexDecodedData[184:192] #SA3W12-W13
                                #print(SPS_vx)
                                SPS_vy = hexDecodedData[192:200] #SA3W14-W15
                                #print(SPS_vy)
                                SPS_vz = hexDecodedData[200:208] #SA3W16-W17
                                #print(SPS_vz)

                                UpdateCounter_hex=hexDecodedData[208:212] # SA3W18
                                #print(UpdateCounter_hex)

                                INT_x_hex = hexDecodedData[212:220] #SA3W19-W20
                                #print(INT_x_hex)
                                INT_y_hex  = hexDecodedData[220:228] #SA3W21-W22
                                #print(INT_y_hex)
                                INT_z_hex  = hexDecodedData[228:236] #SA3W23-W24
                                #print(INT_z_hex)
                                INT_vx_hex  = hexDecodedData[236:244] #SA3W25-W26
                                #print(INT_vx_hex)
                                INT_vy_hex  = hexDecodedData[244:252] #SA3W27-W28
                                #print(INT_vy_hex)
                                INT_vz_hex  = hexDecodedData[252:260] #SA3W29-W30
                                #print(INT_vz_hex)

                                validation_flag_hex=hexDecodedData[260:264] #SA3W31
                                #print(validation_flag_hex)
                                validation_flag=reverse_and_concatenate(validation_flag_hex)
                                #print(f"\nvalidation flag:{validation_flag}")
                                ODP_FLAG=decode_validation_flag(validation_flag)



                                CHECKSUM1_hex = hexDecodedData[264:268] #SA3W32
                                #print(f"CHECKSUM1_hex:{CHECKSUM1_hex}")

                                #========================SUBADRESS 4 START==================
                                SVID1_hex = hexDecodedData[400:402] #SA4W1-W2
                                SVID2_hex = hexDecodedData[402:404] #SA4W3-W4
                                SVID3_hex = hexDecodedData[396:398] #SA4W5-W6
                                SVID4_hex = hexDecodedData[398:400] #SA4W7-W8
                                SVID5_hex = hexDecodedData[408:410] #SA4W9-W10
                                SVID6_hex = hexDecodedData[410:412] #SA4W11-W12
                                SVID7_hex = hexDecodedData[404:406] #SA4W13-W14
                                SVID8_hex = hexDecodedData[406:408] #SA4W15-W16

                                #Delta SV1
                                DR1_hex = hexDecodedData[332:340] #SA4W17-W18
                                DR2_hex = hexDecodedData[340:348] #SA4W19-W20
                                DR3_hex = hexDecodedData[348:356] #SA4W21-W22
                                DR4_hex = hexDecodedData[356:364] #SA4W23-W24
                                DR5_hex = hexDecodedData[364:372] #SA4W25-W26
                                DR6_hex = hexDecodedData[372:380] #SA4W27-W28
                                DR7_hex = hexDecodedData[380:388] #SA4W29-W30
                                DR8_hex = hexDecodedData[388:396] #SA4W31-W32

                                CLOCKBIAS_hex = hexDecodedData[428:436] #SA4
                                PDOP_hex = hexDecodedData[436:440]

                                system_flag_hex = hexDecodedData[448:452] #
                                system_flag = reverse_and_concatenate(system_flag_hex)

                                decoded_flags = decode_system_mode_status(system_flag)

                                # Example: Update GUI entry widgets
                                for label, value in decoded_flags.items():
                                    entry = gui_entry_dict.get(label)
                                    if entry:
                                        entry.config(state="normal")
                                        entry.delete(0, END)
                                        entry.insert(0, value)
                                        entry.config(state="readonly")
                                        set_status_colored(entry, value)   # ✅ instead of manual insert

                                #INTER_BIAS_hex = hexDecodedData[456:460]

                                Last_cmd_excuted_byte3_hex = hexDecodedData[476:478]
                                Last_cmd_excuted_byte4_hex = hexDecodedData[478:480]
                                Last_cmd_excuted_byte1_2_hex = hexDecodedData[480:484]

                                wdt_status_hex = hexDecodedData[484:488]
                                wdt_status = reverse_and_concatenate(wdt_status_hex)

                                decoded_wdt = decode_wdt_status_word(wdt_status)

                                for label, value in decoded_wdt.items():
                                    entry = wdt_entries.get(label)
                                    if entry:
                                        entry.config(state="normal")
                                        entry.delete(0, tk.END)
                                        entry.insert(0, value)
                                        entry.config(state="readonly")
                                        set_status_colored(entry, value)

                                ACQ1_SVID_hex = hexDecodedData[488:490]
                                SWDT_RST_COUNTER_hex = hexDecodedData[490:492]

                                word25_hex = hexDecodedData[492:496]  # Word#25
                                word25 = reverse_and_concatenate(word25_hex)
                                decoded25 = decode_word25(word25)

                                for label, value in decoded25.items():
                                    entry = word25_entries.get(label)
                                    if entry:
                                        entry.config(state="normal")
                                        entry.delete(0, tk.END)
                                        entry.insert(0, str(value))
                                        entry.config(state="readonly")

                                word32_hex = hexDecodedData[1032:1036]  # Word#25
                                word32 = reverse_and_concatenate(word32_hex)
                                decoded32 = decode_sa9word32(word32)


                                for label, value in decoded32.items():
                                    entry = word32_entries.get(label)
                                    if entry:
                                        entry.config(state="normal")
                                        entry.delete(0, tk.END)
                                        entry.insert(0, str(value))
                                        entry.config(state="readonly")
                                        set_status_colored(entry, value)   # ✅ instead of manual insert


                                MC_hex = hexDecodedData[496:500]

                                sa5w22_hex = hexDecodedData[484:488]
                                sa5w22 = reverse_and_concatenate(sa5w22_hex)
                                ODP_prop_used = (sa5w22 & 0x0008) >> 3

                                LAST_RESET_TIME_hex = hexDecodedData[504:508]
                                sa5w27_hex = hexDecodedData[504:508]
                                sa5w27 = reverse_and_concatenate(sa5w27_hex)

                                ill_cnd_val = (sa5w27 & 0xFFF8) >> 3

                                INTER_BIAS_hex = hexDecodedData[456:460]
                                sa5w15_hex = hexDecodedData[456:460]
                                sa5w15 = reverse_and_concatenate(sa5w15_hex)
                                ill_cnd_Limit = (sa5w15 &0xFFC0) >> 6

                                post_cntr = ((sa5w27 & 0x0007)<<6) |(sa5w15 & 0x003f)


                                sa5w28_hex = hexDecodedData[508:512]  # Adjust index as per actual layout

                                # Convert to integer
                                sa5w28 = reverse_and_concatenate(sa5w28_hex)

                                cond_pre_check = (sa5w28 &0x1000)>>12
                                cond_post_check = (sa5w28 & 0x2000)>>13

                                sa5w29_hex= hexDecodedData[512:516]  # Adjust index if needed



                                # Convert to int
                                sa5w29 = reverse_and_concatenate(sa5w29_hex)
                                pre_cntr = (sa5w29 & 0xf000)>>12




                                INTER_SYSTEM_Drift_hex = hexDecodedData[520:524]

                                IODE_hex = hexDecodedData[524:526]
                                SVID_hex = hexDecodedData[526:528]
                                CRS_hex = hexDecodedData[528:532]

                                DRIFT_LSB_hex = hexDecodedData[684:688]
                                #print(f"Drift_lsb:{DRIFT_LSB_hex}")
                                DRIFT_MSB_hex = hexDecodedData[704:708]
                                #print(f"Drift_msb:{DRIFT_MSB_hex}")


                                DRIFT_MSB_LSB_HEX = DRIFT_MSB_hex + DRIFT_LSB_hex
                                #print(f"drift hex:{DRIFT_MSB_LSB_HEX}")
                                DRIFT = reverse_and_concatenate(DRIFT_MSB_LSB_HEX, is_signed=True)/1000.0
                                #print(f"drift:{DRIFT}")




                                word15_hex = hexDecodedData[708:712]
                                word15=reverse_and_concatenate(word15_hex)
                                decoded_cmd = decode_word15(word15)

                                # When you decode:
                                for label, value in decoded_cmd.items():
                                    entry = tele_entries[label]
                                    entry.config(state="normal")
                                    entry.delete(0, END)
                                    entry.insert(0, value)
                                    entry.config(state="readonly")
                                    set_status_colored(entry, value)

                                TELE_CMD_COUNTER_hex = hexDecodedData[744:746]
                                UPSET_COUNTER_hex = hexDecodedData[746:748]






                                SVID9_hex = hexDecodedData[688:690]
                                SVID10_hex = hexDecodedData[690:692]
                                SVID11_hex = hexDecodedData[748:750]
                                SVID12_hex = hexDecodedData[750:752]

                                CNDR1_hex = hexDecodedData[464:466]
                                CNDR2_hex = hexDecodedData[466:468]
                                CNDR3_hex = hexDecodedData[460:462]
                                CNDR4_hex = hexDecodedData[462:464]
                                CNDR5_hex = hexDecodedData[472:474]
                                CNDR6_hex = hexDecodedData[474:476]
                                CNDR7_hex = hexDecodedData[468:470]
                                CNDR8_hex = hexDecodedData[470:472]
                                CNDR9_hex = hexDecodedData[700:702]
                                CNDR10_hex = hexDecodedData[702:704]
                                CNDR11_hex = hexDecodedData[760:762]
                                CNDR12_hex = hexDecodedData[762:764]

                                IODE1_hex = hexDecodedData[416:418]
                                IODE2_hex = hexDecodedData[418:420]
                                IODE3_hex = hexDecodedData[412:414]
                                IODE4_hex = hexDecodedData[414:416]
                                IODE5_hex = hexDecodedData[424:426]
                                IODE6_hex = hexDecodedData[426:428]
                                IODE7_hex = hexDecodedData[420:422]
                                IODE8_hex = hexDecodedData[422:424]
                                IODE9_hex = hexDecodedData[696:698]
                                IODE10_hex = hexDecodedData[698:700]
                                IODE11_hex = hexDecodedData[756:758]
                                IODE12_hex = hexDecodedData[758:760]

                                PR1_hex = hexDecodedData[268:276]
                                PR2_hex = hexDecodedData[276:284]
                                PR3_hex = hexDecodedData[284:292]
                                PR4_hex = hexDecodedData[292:300]
                                PR5_hex = hexDecodedData[300:308]
                                PR6_hex = hexDecodedData[308:316]
                                PR7_hex = hexDecodedData[316:324]
                                PR8_hex = hexDecodedData[324:332]
                                PR9_hex = hexDecodedData[652:660]
                                PR10_hex = hexDecodedData[660:668]
                                PR11_hex = hexDecodedData[712:720]
                                PR12_hex = hexDecodedData[720:728]




                                DR9_hex = hexDecodedData[668:676]
                                DR10_hex = hexDecodedData[676:684]
                                DR11_hex = hexDecodedData[728:736]
                                DR12_hex = hexDecodedData[736:744]

                                ephem_constel_word = hexDecodedData[440:444]  # Word#12
                                ephem_constel_hex = reverse_and_concatenate(ephem_constel_word)

                                # Constellation flag (B0 to B7) → for channels 1 to 8
                                constel_flag = [(ephem_constel_hex >> i) & 1 for i in range(8)]  # B0 to B7
                                # Ephemeris flag (B8 to B15) → for channels 1 to 8
                                ephem_flag   = [(ephem_constel_hex >> i) & 1 for i in range(8, 16)]  # B8 to B15

                                # P (Constellation): 0 = Used → Y, 1 = Not used → N
                                constel_flag_display = ['Y' if flag == 1 else 'N' for flag in constel_flag]

                                # E (Ephemeris): 0 = Available → Y, 1 = Not available → N
                                ephem_flag_display = ['Y' if flag == 1 else 'N' for flag in ephem_flag]


                                E_T_P_D9_10 = hexDecodedData[692:696]
                                E_T_P_D9_10_hex = reverse_and_concatenate(E_T_P_D9_10)

                                # Extract each field using bitwise ops
                                eph_10_bits = (E_T_P_D9_10_hex >> 13) & 0x1
                                #print(f"E10:{eph_10_bits}")
                                eph_9_bits  = (E_T_P_D9_10_hex >> 12) & 0x1
                                #print(f"E9:{eph_9_bits}")
                                status_10_bits = (E_T_P_D9_10_hex >>10) & 0x3
                                status_9_bits  = (E_T_P_D9_10_hex >> 8) & 0x3

                                constel_10 = (E_T_P_D9_10_hex >> 7) & 0x1
                                constel_9  = (E_T_P_D9_10_hex >> 6) & 0x1

                                dr_10 = (E_T_P_D9_10_hex >> 5) & 0x1
                                dr_9  = (E_T_P_D9_10_hex >> 4) & 0x1

                                # TOA-aLM: lower 4 bits from this word (b3–b0)
                                #toa_alm_ls_4 = E_T_P_D9_10_hex & 0xF

                                # You can combine this with MS 4 bits from next word to form full TOA if needed

                                # Format displays


                                if eph_9_bits == 0b00:
                                    e9_flag = 'N'
                                elif eph_9_bits == 0b01:
                                    e9_flag = 'Y'
                                else:
                                    e9_flag ="UN"

                                if eph_10_bits == 0b00:
                                    e10_flag = 'N'
                                elif eph_10_bits == 0b01:
                                    e10_flag = 'Y'
                                else:
                                    eph_10_bits ="UN"







                                t_map = {0b00: 'I', 0b01: 'A', 0b10: 'T', 0b11: 'N'}

                                t9_flag = t_map.get(status_9_bits, 'N')
                                t10_flag = t_map.get(status_10_bits, 'N')

                                p9_flag  = 'Y' if constel_9 == 1 else 'N'
                                p10_flag  = 'Y' if constel_10 == 1 else 'N'

                                d9_flag  = 'Y' if dr_9 == 1 else 'N'
                                d10_flag  = 'Y' if dr_10 == 1 else 'N'

                                E_T_P_D11_12 = hexDecodedData[752:756]
                                E_T_P_D11_12_hex = reverse_and_concatenate(E_T_P_D11_12)

                                # Extract bit fields
                                eph_12_bits = (E_T_P_D11_12_hex >> 13) & 0x1
                                #print(f"E12:{eph_12_bits}")
                                eph_11_bits = (E_T_P_D11_12_hex >> 12) & 0x1
                                #print(f"E11:{eph_11_bits}")

                                status_12_bits = (E_T_P_D11_12_hex >> 10) & 0X3
                                status_11_bits = (E_T_P_D11_12_hex >> 8) & 0X3

                                constel_12 = (E_T_P_D11_12_hex >> 7) & 0x1
                                constel_11 = (E_T_P_D11_12_hex >> 6) & 0x1

                                dr_12 = (E_T_P_D11_12_hex >> 5) & 0x1
                                dr_11 = (E_T_P_D11_12_hex >> 4) & 0x1

                                # Format the display outputs
                                e11_flag  = 'Y' if eph_11_bits == 1 else 'N'
                                e12_flag  = 'Y' if eph_12_bits == 1 else 'N'

                                t_map = {0b00: 'I', 0b01: 'A', 0b10: 'T', 0b11: 'N'}
                                t11_flag  = t_map.get(status_11_bits, 'N')
                                t12_flag  = t_map.get(status_12_bits, 'N')

                                p11_flag  = 'Y' if constel_11 == 1 else 'N'
                                p12_flag  = 'Y' if constel_12 == 1 else 'N'

                                d11_flag  = 'Y' if dr_11 == 1 else 'N'
                                d12_flag  = 'Y' if dr_12 == 1 else 'N'

                                T = hexDecodedData[444:448]  # Word#13 (2 bytes = 1 word)

                                # Convert to integer
                                channel_status_word = reverse_and_concatenate(T)

                                # Mapping of 2-bit status to display
                                status_map = {
                                    0b00: 'I',  # IDLE
                                    0b01: 'A',  # ACQ
                                    0b10: 'T',  # TRK
                                    0b11: 'N'   # NA
                                }

                                # Extract and decode status for channels 1 to 8
                                T_flag_display = []
                                for i in range(8):
                                    status_bits = (channel_status_word >> (i * 2)) & 0b11
                                    T_flag_display.append(status_map.get(status_bits, 'N'))  # Default to 'N' if unknown

                                D = hexDecodedData[452:456]

                                # Convert full word to integer
                                word15_int = reverse_and_concatenate(D)

                                # Extract LSB (lower 8 bits) for DR flags
                                dr_status_lsb = word15_int & 0xFF

                                # DR Flag Display (Channel 1–8)
                                D_flag_display = []
                                for i in range(8):
                                    bit = (dr_status_lsb >> i) & 1
                                    D_flag_display.append('Y' if bit else 'N')

                                Sol_config =  (word15_int >> 15) & 0x1
                                if Sol_config == 0b00:
                                    Sol = "NA"
                                    sol.config(fg="dark red")
                                if Sol_config == 0b01:
                                    Sol = "A"
                                    sol.config(fg="dark green")
                                else:
                                    Sol = "UN"
                                    sol.config(fg="black")


                                Pos_E_config = (word15_int >> 14) & 0x1
                                if Pos_E_config == 0b00:
                                    Pos_E = "NA"
                                    pos_e.config(fg="dark red")
                                if Pos_E_config == 0b01:
                                    Pos_E = "A"
                                    pos_e.config(fg="dark green")
                                else:
                                    Pos_E = "UN"
                                    pos_e.config(fg="black")


                                alm_config = (word15_int >> 12) & 0x3

                                if alm_config == 0b00:
                                    ALM = "A"
                                    alm.config(fg="dark green")
                                elif alm_config == 0b01:
                                    ALM = "NA"
                                    alm.config(fg="dark red")
                                elif alm_config == 0b10:
                                    ALM = "No"
                                    alm.config(fg="black")
                                else:
                                    ALM = "Unknown"
                                    alm.config(fg="black")

                                Time_config = (word15_int >> 11) & 0x1
                                if Time_config == 0b00:
                                    Time = "NA"
                                    time.config(fg="dark red")
                                elif Time_config == 0b01:
                                    Time = "A"
                                    time.config(fg="dark green")
                                else:
                                    Time = "UN"
                                    time.config(fg="black")

                                d_2d = (word15_int >> 9) & 0x3
                                if d_2d == 0b00:
                                    D2_3D_config = "3D"
                                    d2_3d.config(fg="dark green")
                                elif d_2d == 0b01:
                                    D2_3D_config = "2D"
                                    d2_3d.config(fg="dark red")
                                elif d_2d == 0b10:
                                    D2_3D_config = "NA"
                                    d2_3d.config(fg="red")
                                else:
                                    D2_3D_config = "Unknown"
                                    d2_3d.config(fg="black")
                                '''d_map = {
                                    0b00: "3D",
                                    0b01: "2D",
                                    0b10: "NA"
                                }
                                D2_3D_config = d_map[d_2d]'''

                                pos_config = (word15_int >> 8) & 0x1
                                if pos_config == 0b00:
                                    Pos = "NA"
                                    pos.config(fg="dark red")
                                elif pos_config == 0b01:
                                    Pos = "A"
                                    pos.config(fg="dark green")
                                else:
                                    Pos = "UN"
                                    pos.config(fg="black")



                                H = hexDecodedData[500:504]

                                # Convert to integer
                                word27_int = reverse_and_concatenate(H)

                                # Extract bits B0 to B11 → CH1 to CH12 SV Health/URA Status
                                H_flag_display = []
                                for i in range(12):
                                    bit = (word27_int >> i) & 0x1
                                    H_flag_display.append('G' if bit == 0 else 'B')
                                # Decode Port1 (B13:B12)
                                port1_bits = (word27_int >> 12) & 0x3
                                port1_map = {
                                    0b00: "GPS",
                                    0b01: "NAVIC",
                                    0b10: "Combined",
                                    0b11: "Reserved"
                                }
                                port1_config = port1_map[port1_bits]

                                # Decode Port2 (B15:B14)
                                port2_bits = (word27_int >> 14) & 0x3
                                port2_map = {
                                    0b00: "GPS",
                                    0b01: "NAVIC",
                                    0b10: "Combined",
                                    0b11: "Reserved"
                                }
                                port2_config = port2_map[port2_bits]


                                I = hexDecodedData[508:512]  # Adjust index as per actual layout

                                # Convert to integer
                                word29_int = reverse_and_concatenate(I)

                                # Decode B0–B11 → CH1 to CH12
                                I_flag_display = []
                                for i in range(12):
                                    bit = (word29_int >> i) & 0x1
                                    I_flag_display.append('N' if bit == 1 else 'A')


                                A = hexDecodedData[512:516]  # Adjust index if needed

                                # Convert to int
                                word30_int = reverse_and_concatenate(A)

                                # Decode B0–B11: RF chain per channel
                                A_flag_display = []
                                for i in range(12):  # Ch1–Ch12
                                    bit = (word30_int >> i) & 0x1
                                    A_flag_display.append('1' if bit else '0')  # 0 → RF1, 1 → RF2

                                R = hexDecodedData[516:520]  # Adjust index if required

                                # Convert to integer
                                word31_int = reverse_and_concatenate(R)

                                # Decode B0–B11: Health/URA Rejection Flags
                                R_flag_display = []
                                for i in range(12):
                                    bit = (word31_int >> i) & 0x1
                                    R_flag_display.append('R' if bit else 'P')  # 0 = Healthy, 1 = Unhealthy

                                # Decode Additional Bits
                                odp_status = 'Enabled' if ((word31_int >> 12) & 0x1) == 1 else 'Disabled'
                                phase_corr = 'Enabled' if ((word31_int >> 13) & 0x1) == 1 else 'Disabled'
                                phase_corr_sps = 'Enabled' if ((word31_int >> 14) & 0x1) == 1 else 'Disabled'

                                sbas_fast_crr = hexDecodedData[776:780]  # Adjust index if needed

                                # Convert to int
                                word32_int = reverse_and_concatenate(sbas_fast_crr)
                                # Decode Additional Bits
                                #elev_flag = 'Disabled' if ((word32_int >> 12) & 0x1) == 0 else 'Enabled'
                                ccsds_flag = 'Enabled' if ((word32_int >> 15) & 0x1) == 1 else 'Disabled'
                                randomizer_flag = 'on' if ((word32_int >> 14) & 0x1) == 1 else 'off'
                                #pr_mode_flag = 'old' if ((word32_int >> 13) & 0x1) == 1 else 'new'

                                word31_hex = hexDecodedData [772:776]
                                word31 = reverse_and_concatenate(word31_hex)
                                decoded_data =  Multiplexing(word31)

                                Spacecraft_id_hex = hexDecodedData[764:766]
                                Spacecraft_id=reverse_and_concatenate(Spacecraft_id_hex)
                                Navic_cmd_hex = hexDecodedData[766:768]
                                Navic_cmd = reverse_and_concatenate(Navic_cmd_hex)

                                odp_par_hex = hexDecodedData[1036:1040] #
                                odp_par = reverse_and_concatenate(odp_par_hex)

                                odp_flags = odp_parameter(odp_par)

                                # Example: Update GUI entry widgets
                                for label, value in odp_flags.items():
                                    entry = odp_entries.get(label)
                                    if entry:
                                        entry.config(state="normal")
                                        entry.delete(0, END)
                                        entry.insert(0, value)
                                        entry.config(state="readonly")
                                        set_status_colored(entry, value)

                                #Steering BIAS
                                Steering_B_hex = hexDecodedData[1068:1072]
                                Steering_B = reverse_and_concatenate(Steering_B_hex)
                                value1 = (Steering_B & 0X7FFF)/100.0
                                b_flag = (Steering_B >> 15) & 0x1

                                if b_flag == 1:
                                    Steering_Bias = -value1
                                else:
                                    Steering_Bias = value1

                                #U1 DATA

                                U1_hex =  hexDecodedData[1072:1076]
                                U1_h = reverse_and_concatenate(U1_hex)
                                value2 = (U1_h & 0X7FFF)/100.0
                                b_flag = (U1_h >> 15) & 0x1

                                if b_flag == 1:
                                    U1_data = -value2
                                else:
                                    U1_data = value2


                                #Steering DRIFT
                                Steering_Drift_hex = hexDecodedData[1076:1080]
                                Steering_D = reverse_and_concatenate(Steering_Drift_hex)
                                value3 = (Steering_D & 0X7FFF)/10.0
                                b_flag = (Steering_D >> 15) & 0x1

                                if b_flag == 1:
                                    Steering_Drift = -value3
                                else:
                                    Steering_Drift = value3


                                #U2 DATA
                                U2_hex =  hexDecodedData[1080:1084]
                                U2_h = reverse_and_concatenate(U2_hex)
                                value4 = (U2_h & 0X7FFF)/10.0
                                b_flag = (U2_h >> 15) & 0x1

                                if b_flag == 1:
                                    U2_data = -value4
                                else:
                                    U2_data = value4

                                #Steering CLOCK
                                Steering_clock_hex = hexDecodedData[1084:1092]
                                Steering_clock = reverse_and_concatenate(Steering_clock_hex,is_signed=True)/1000.0

                                '''SA10W20_hex = hexDecodedData[1112:1116]
                                SA10W20=reverse_and_concatenate(SA10W20_hex)
                                #ill_cnd_val = SA10W20
                                #ill_cnd_val = (SA10W20 & 0xFFF8) >> 3
                                #pre_cntr = SA10W20 & 0x0007

                                SA10W21_hex = hexDecodedData[1116:1120]
                                SA10W21=reverse_and_concatenate(SA10W21_hex)
                                #ill_cnd_Limit = SA10W21
                                #ill_cnd_Limit = (SA10W21 &0xFFC0) >> 6
                                #post_cntr = SA10W21 & 0x003F

                                SA10W22_hex = hexDecodedData[1120:1124]
                                SA10W22=reverse_and_concatenate(SA10W22_hex)
                                cond_pre_check = SA10W22 & 0x00FF
                                cond_post_check = (SA10W22 >> 8) & 0x00FF

                                SA10W23_hex = hexDecodedData[1124:1128]
                                SA10W23=reverse_and_concatenate(SA10W23_hex)
                                ODP_prop_used = (SA10W23 >> 0) & 1'''
                                
                                SA10W22_hex = hexDecodedData[1120:1124]
                                SA10W22=reverse_and_concatenate(SA10W22_hex)
                                Orbit_phase = (SA10W22 >> 13) & 0x1
                                
                                


                                PPS_3D_hex = hexDecodedData[1804:1808]
                                pps_3d=reverse_and_concatenate(PPS_3D_hex)

                                if pps_3d == 3:
                                    PPS_3D = "2D Fix"
                                elif pps_3d == 7:
                                    PPS_3D = "3D Fix"
                                else :
                                    PPS_3D = "No Fix"

                                PPS_NanoSec_hex = hexDecodedData[1808:1816]
                                #print(PPS_NanoSec_hex)
                                PPS_NanoSec=reverse_and_concatenate(PPS_NanoSec_hex)
                                PPS_Sec_hex = hexDecodedData[1816:1824]
                                PPS_Sec=reverse_and_concatenate(PPS_Sec_hex)
                                PPS_Week_hex = hexDecodedData[1824:1828]
                                PPS_Week=reverse_and_concatenate(PPS_Week_hex)





                                # Convert hex to decimal and scale as needed
                                '''SYN_NanoSecond=reverse_and_concatenate(SYN_NanoSecond_hex)
                                SYN_Second=reverse_and_concatenate(SYN_Second_hex)
                                SYN_Weeknumber=reverse_and_concatenate(SYN_Weeknumber_hex)'''

                                CHECKSUM=reverse_and_concatenate(CHECKSUM_hex)
                                chechsum_calulation_covert_decimal(SYN_NanoSecond_hex,SYN_Second_hex,SYN_Weeknumber_hex,CHECKSUM)

                                SYS_NanoSecond=reverse_and_concatenate(SYS_NanoSecond_hex)
                                SYS_Second=reverse_and_concatenate(SYS_Second_hex)
                                SYS_Weeknumber=reverse_and_concatenate(SYS_Weeknumber_hex)

                                EST_x = reverse_and_concatenate(SPS_x, is_signed=True)/100.0
                                EST_y = reverse_and_concatenate(SPS_y, is_signed=True)/100.0
                                EST_z = reverse_and_concatenate(SPS_z, is_signed=True)/100.0
                                EST_vx = reverse_and_concatenate(SPS_vx, is_signed=True)/1000.0
                                EST_vy = reverse_and_concatenate(SPS_vy, is_signed=True)/1000.0
                                EST_vz = reverse_and_concatenate(SPS_vz, is_signed=True)/1000.0

                                UpdateCounter=reverse_and_concatenate(UpdateCounter_hex)

                                INT_x = reverse_and_concatenate(INT_x_hex , is_signed=True)/100.0
                                INT_y = reverse_and_concatenate(INT_y_hex , is_signed=True)/100.0
                                INT_z = reverse_and_concatenate(INT_z_hex , is_signed=True)/100.0
                                INT_vx = reverse_and_concatenate(INT_vx_hex , is_signed=True)/1000.0
                                INT_vy = reverse_and_concatenate(INT_vy_hex , is_signed=True)/1000.0
                                INT_vz = reverse_and_concatenate(INT_vz_hex , is_signed=True)/1000.0

                                validation_flag=reverse_and_concatenate(validation_flag_hex)

                                CHECKSUM1=reverse_and_concatenate(CHECKSUM1_hex)
                                SA4chechsum_calulation_covert_decimal(SYS_NanoSecond_hex,SYS_Second_hex,SYS_Weeknumber_hex,SPS_x,SPS_y,SPS_z,SPS_vx,SPS_vy,SPS_vz,UpdateCounter_hex,INT_x_hex ,INT_y_hex ,INT_z_hex ,INT_vx_hex ,INT_vy_hex ,INT_vz_hex ,validation_flag_hex,CHECKSUM1)

                                CLOCKBIAS = reverse_and_concatenate(CLOCKBIAS_hex,is_signed=True)/100.0
                                PDOP = reverse_and_concatenate(PDOP_hex, is_signed=True)/100.0
                                INTER_SYSTEM_BIAS= reverse_and_concatenate(INTER_BIAS_hex,is_signed=True)/1000.0
                                SWDT_RST_COUNTER = reverse_and_concatenate(SWDT_RST_COUNTER_hex)
                                Last_cmd_excuted_byte4 = reverse_and_concatenate(Last_cmd_excuted_byte4_hex)
                                Last_cmd_excuted_byte1_2 = reverse_and_concatenate(Last_cmd_excuted_byte1_2_hex)


                                ACQ1_SVID = reverse_and_concatenate(ACQ1_SVID_hex)
                                Last_cmd_excuted_byte3 = reverse_and_concatenate(Last_cmd_excuted_byte3_hex)
                                MC = reverse_and_concatenate(MC_hex)
                                LRT = reverse_and_concatenate(LAST_RESET_TIME_hex)
                                ISD = reverse_and_concatenate(INTER_SYSTEM_Drift_hex)

                                SVID = reverse_and_concatenate(SVID_hex)
                                IODE = reverse_and_concatenate(IODE_hex)
                                CRS = reverse_and_concatenate(CRS_hex)



                                TELE_CMD_COUNTER = reverse_and_concatenate(TELE_CMD_COUNTER_hex)
                                UPSET_COUNTER = reverse_and_concatenate(UPSET_COUNTER_hex)

                                SVID1 = reverse_and_concatenate(SVID1_hex)
                                SVID2 = reverse_and_concatenate(SVID2_hex)
                                SVID3 = reverse_and_concatenate(SVID3_hex)
                                SVID4 = reverse_and_concatenate(SVID4_hex)
                                SVID5 = reverse_and_concatenate(SVID5_hex)
                                SVID6 = reverse_and_concatenate(SVID6_hex)
                                SVID7 = reverse_and_concatenate(SVID7_hex)
                                SVID8 = reverse_and_concatenate(SVID8_hex)
                                SVID9 = reverse_and_concatenate(SVID9_hex)
                                SVID10 = reverse_and_concatenate(SVID10_hex)
                                SVID11 = reverse_and_concatenate(SVID11_hex)
                                SVID12 = reverse_and_concatenate(SVID12_hex)

                                CNDR1 = reverse_and_concatenate(CNDR1_hex)
                                CNDR2 = reverse_and_concatenate(CNDR2_hex)
                                CNDR3 = reverse_and_concatenate(CNDR3_hex)
                                CNDR4 = reverse_and_concatenate(CNDR4_hex)
                                CNDR5 = reverse_and_concatenate(CNDR5_hex)
                                CNDR6 = reverse_and_concatenate(CNDR6_hex)
                                CNDR7 = reverse_and_concatenate(CNDR7_hex)
                                CNDR8 = reverse_and_concatenate(CNDR8_hex)
                                CNDR9 = reverse_and_concatenate(CNDR9_hex)
                                CNDR10 = reverse_and_concatenate(CNDR10_hex)
                                CNDR11 = reverse_and_concatenate(CNDR11_hex)
                                CNDR12 = reverse_and_concatenate(CNDR12_hex)



                                IODE1 = reverse_and_concatenate(IODE1_hex)
                                IODE2 = reverse_and_concatenate(IODE2_hex)
                                IODE3 = reverse_and_concatenate(IODE3_hex)
                                IODE4 = reverse_and_concatenate(IODE4_hex)
                                IODE5 = reverse_and_concatenate(IODE5_hex)
                                IODE6 = reverse_and_concatenate(IODE6_hex)
                                IODE7 = reverse_and_concatenate(IODE7_hex)
                                IODE8 = reverse_and_concatenate(IODE8_hex)
                                IODE9 = reverse_and_concatenate(IODE9_hex)
                                IODE10 = reverse_and_concatenate(IODE10_hex)
                                IODE11 = reverse_and_concatenate(IODE11_hex)
                                IODE12 = reverse_and_concatenate(IODE12_hex)


                                PR1 = reverse_and_concatenate(PR1_hex)
                                PR2 = reverse_and_concatenate(PR2_hex)
                                PR3 = reverse_and_concatenate(PR3_hex)
                                PR4 = reverse_and_concatenate(PR4_hex)
                                PR5 = reverse_and_concatenate(PR5_hex)
                                PR6 = reverse_and_concatenate(PR6_hex)
                                PR7 = reverse_and_concatenate(PR7_hex)
                                PR8 = reverse_and_concatenate(PR8_hex)
                                PR9 = reverse_and_concatenate(PR9_hex)
                                PR10 = reverse_and_concatenate(PR10_hex)
                                PR11 = reverse_and_concatenate(PR11_hex)
                                PR12 = reverse_and_concatenate(PR12_hex)

                                DR1 = reverse_and_concatenate(DR1_hex,is_signed=True)/1000.0
                                DR2 = reverse_and_concatenate(DR2_hex,is_signed=True)/1000.0
                                DR3 = reverse_and_concatenate(DR3_hex,is_signed=True)/1000.0
                                DR4 = reverse_and_concatenate(DR4_hex,is_signed=True)/1000.0
                                DR5 = reverse_and_concatenate(DR5_hex,is_signed=True)/1000.0
                                DR6 = reverse_and_concatenate(DR6_hex,is_signed=True)/1000.0
                                DR7 = reverse_and_concatenate(DR7_hex,is_signed=True)/1000.0
                                DR8 = reverse_and_concatenate(DR8_hex,is_signed=True)/1000.0
                                DR9 = reverse_and_concatenate(DR9_hex,is_signed=True)/1000.0
                                DR10 = reverse_and_concatenate(DR10_hex,is_signed=True)/1000.0
                                DR11 = reverse_and_concatenate(DR11_hex,is_signed=True)/1000.0
                                DR12 = reverse_and_concatenate(DR12_hex,is_signed=True)/1000.0

                                SA29_hex = hexDecodedData[1932:1992]
                                if isinstance(SA29_hex,(bytes,bytearray)):
                                    SA29_hex = SA29_hex.hex()
                                SA29_Raw = " ".join([SA29_hex[i:i+4]for i in range (0,len(SA29_hex),4)])

                                '''check_and_store_TTF(EST_x, EST_y, EST_z, SYN_Second, SYN_NanoSecond, SYN_Weeknumber, UpdateCounter)

                                if TTF is not None:
                                    ttf.config(state="normal")
                                    ttf.delete(0,END)
                                    ttf.insert(0, f"{TTF}")
                                    ttf.config(state="readonly")

                                counter_entry.config(state="normal")
                                counter_entry.delete(0,END)
                                counter_entry.insert(0, str(counter_value))
                                counter_entry.config(state="readonly")


                                time_entry.config(state="normal")
                                time_entry.delete(0,END)
                                time_entry.insert(0, str(SYN_Second))
                                time_entry.config(state="readonly")
                                set_colored_value(time_entry,SYN_Second)

                                nanotime_entry.config(state="normal")
                                nanotime_entry.delete(0,END)
                                nanotime_entry.insert(0, str(SYN_NanoSecond))
                                nanotime_entry.config(state="readonly")
                                set_colored_value(nanotime_entry,SYN_NanoSecond)

                                week_entry.config(state="normal")
                                week_entry.delete(0,END)
                                week_entry.insert(0, str(SYN_Weeknumber))
                                week_entry.config(state="readonly")
                                set_colored_value(week_entry,SYN_Weeknumber)'''

                                csm.config(state=NORMAL)
                                csm.delete(0,END)
                                csm.insert(0, f"{checksum}")
                                csm.config(state="readonly")


                                time_entry1.config(state="normal")
                                time_entry1.delete(0,END)
                                time_entry1.insert(0, str(SYS_Second))
                                time_entry1.config(state="readonly")
                                set_colored_value(time_entry1,SYS_Second)

                                nanotime_entry1.config(state="normal")
                                nanotime_entry1.delete(0,END)
                                nanotime_entry1.insert(0, str(SYS_NanoSecond))
                                nanotime_entry1.config(state="readonly")
                                set_colored_value(nanotime_entry1,SYS_NanoSecond)

                                week_entry1.config(state="normal")
                                week_entry1.delete(0,END)
                                week_entry1.insert(0, str(SYS_Weeknumber))
                                week_entry1.config(state="readonly")
                                set_colored_value(week_entry1,SYS_Weeknumber)

                                time_entry3.config(state="normal")
                                time_entry3.delete(0,END)
                                time_entry3.insert(0, str(PPS_Sec))
                                time_entry3.config(state="readonly")
                                set_colored_value(time_entry3,PPS_Sec)

                                nanotime_entry3.config(state="normal")
                                nanotime_entry3.delete(0,END)
                                nanotime_entry3.insert(0, str(PPS_NanoSec))
                                nanotime_entry3.config(state="readonly")
                                set_colored_value(nanotime_entry3,PPS_NanoSec)

                                week_entry3.config(state="normal")
                                week_entry3.delete(0,END)
                                week_entry3.insert(0, str(PPS_Week))
                                week_entry3.config(state="readonly")
                                set_colored_value(week_entry3,PPS_Week)

                                fix_status.config(state="normal")
                                fix_status.delete(0,END)
                                fix_status.insert(0, str(PPS_3D))
                                fix_status.config(state="readonly")
                                #set_colored_value(fix_status,PPS_3D)

                                position_entry.config(state="normal")
                                position_entry.delete(0,END)
                                position_entry.insert(0, str(EST_x))
                                position_entry.config(state="readonly")
                                set_colored_value(position_entry,EST_x)

                                position_entry1.config(state="normal")
                                position_entry1.delete(0,END)
                                position_entry1.insert(0, str(EST_y))
                                position_entry1.config(state="readonly")
                                set_colored_value(position_entry1,EST_y)

                                position_entry2.config(state="normal")
                                position_entry2.delete(0,END)
                                position_entry2.insert(0, str(EST_z))
                                position_entry2.config(state="readonly")
                                set_colored_value(position_entry2,EST_z)

                                velocity_entry.config(state="normal")
                                velocity_entry.delete(0,END)
                                velocity_entry.insert(0, str(EST_vx))
                                velocity_entry.config(state="readonly")
                                set_colored_value(velocity_entry,EST_vx)

                                velocity_entry1.config(state="normal")
                                velocity_entry1.delete(0,END)
                                velocity_entry1.insert(0, str(EST_vy))
                                velocity_entry1.config(state="readonly")
                                set_colored_value(velocity_entry1,EST_vy)

                                velocity_entry2.config(state="normal")
                                velocity_entry2.delete(0,END)
                                velocity_entry2.insert(0, str(EST_vz))
                                velocity_entry2.config(state="readonly")
                                set_colored_value(velocity_entry2,EST_vz)

                                update_entry.config(state=NORMAL)
                                update_entry.delete(0,END)
                                update_entry.insert(0, f"{UpdateCounter}")
                                update_entry.config(state="readonly")
                                set_colored_value(update_entry,UpdateCounter)

                                position_entry3.config(state="normal")
                                position_entry3.delete(0,END)
                                position_entry3.insert(0, str(INT_x))
                                position_entry3.config(state="readonly")
                                set_colored_value(position_entry3,INT_x)

                                position_entry4.config(state="normal")
                                position_entry4.delete(0,END)
                                position_entry4.insert(0, str(INT_y))
                                position_entry4.config(state="readonly")
                                set_colored_value(position_entry4,INT_y)

                                position_entry5.config(state="normal")
                                position_entry5.delete(0,END)
                                position_entry5.insert(0, str(INT_z))
                                position_entry5.config(state="readonly")
                                set_colored_value(position_entry5,INT_z)

                                velocity_entry3.config(state="normal")
                                velocity_entry3.delete(0,END)
                                velocity_entry3.insert(0, str(INT_vx))
                                velocity_entry3.config(state="readonly")
                                set_colored_value(velocity_entry3,INT_vx)

                                velocity_entry4.config(state="normal")
                                velocity_entry4.delete(0,END)
                                velocity_entry4.insert(0, str(INT_vy))
                                velocity_entry4.config(state="readonly")
                                set_colored_value(velocity_entry4,INT_vy)


                                velocity_entry5.config(state="normal")
                                velocity_entry5.delete(0,END)
                                velocity_entry5.insert(0, str(INT_vz))
                                velocity_entry5.config(state="readonly")
                                set_colored_value(velocity_entry5,INT_vz)


                                flag.config(state=NORMAL)
                                flag.delete(0,END)
                                flag.insert(0, f"{ODP_FLAG}")
                                flag.config(state="readonly")
                                #set_colored_value(flag,ODP_FLAG)

                                csm1.config(state=NORMAL)
                                csm1.delete(0,END)
                                csm1.insert(0, f"{checksum1}")
                                csm1.config(state="readonly")


                                cb.config(state=NORMAL)
                                cb.delete(0,END)
                                cb.insert(0, f"{CLOCKBIAS}")
                                cb.config(state="readonly")
                                set_colored_value(cb,CLOCKBIAS)

                                pdop.config(state=NORMAL)
                                pdop.delete(0,END)
                                pdop.insert(0, f"{PDOP}")
                                pdop.config(state="readonly")
                                set_colored_value(pdop,PDOP)


                                icb.config(state=NORMAL)
                                icb.delete(0,END)
                                icb.insert(0, f"{INTER_SYSTEM_BIAS}")
                                icb.config(state="readonly")
                                set_colored_value(icb,INTER_SYSTEM_BIAS)

                                st_bias.config(state=NORMAL)
                                st_bias.delete(0,END)
                                st_bias.insert(0, f"{Steering_Bias}")
                                st_bias.config(state="readonly")
                                set_colored_value(st_bias,Steering_Bias)

                                st_drift.config(state=NORMAL)
                                st_drift.delete(0,END)
                                st_drift.insert(0, f"{Steering_Drift}")
                                st_drift.config(state="readonly")
                                set_colored_value(st_drift,Steering_Drift)

                                clk_crr.config(state=NORMAL)
                                clk_crr.delete(0,END)
                                clk_crr.insert(0, f"{Steering_clock}")
                                clk_crr.config(state="readonly")
                                set_colored_value(clk_crr,Steering_clock)

                                U1.config(state=NORMAL)
                                U1.delete(0,END)
                                U1.insert(0, f"{U1_data}")
                                U1.config(state="readonly")
                                set_colored_value(U1,U1_data)

                                U2.config(state=NORMAL)
                                U2.delete(0,END)
                                U2.insert(0, f"{U1_data}")
                                U2.config(state="readonly")
                                set_colored_value(U2,U2_data)


                                swdt.config(state=NORMAL)
                                swdt.delete(0,END)
                                swdt.insert(0, f"{SWDT_RST_COUNTER}")
                                swdt.config(state="readonly")
                                set_colored_value(swdt,SWDT_RST_COUNTER)


                                last_cmd_b1_b2.config(state=NORMAL)
                                last_cmd_b1_b2.delete(0,END)
                                last_cmd_b1_b2.insert(0, f"{Last_cmd_excuted_byte1_2}")
                                last_cmd_b1_b2.config(state="readonly")
                                set_colored_value(last_cmd_b1_b2,Last_cmd_excuted_byte1_2)

                                last_cmd_b3.config(state=NORMAL)
                                last_cmd_b3.delete(0,END)
                                last_cmd_b3.insert(0, f"{Last_cmd_excuted_byte3}")
                                last_cmd_b3.config(state="readonly")
                                set_colored_value(last_cmd_b3,Last_cmd_excuted_byte3)

                                last_cmd_b4.config(state=NORMAL)
                                last_cmd_b4.delete(0,END)
                                last_cmd_b4.insert(0, f"{Last_cmd_excuted_byte4}")
                                last_cmd_b4.config(state="readonly")
                                set_colored_value(last_cmd_b4,Last_cmd_excuted_byte4)

                                acq1_svid.config(state=NORMAL)
                                acq1_svid.delete(0,END)
                                acq1_svid.insert(0, f"{ACQ1_SVID}")
                                acq1_svid.config(state="readonly")
                                set_colored_value(acq1_svid,ACQ1_SVID)


                                mc.config(state=NORMAL)
                                mc.delete(0,END)
                                mc.insert(0, f"{MC}")
                                mc.config(state="readonly")
                                set_colored_value(mc,MC)

                                lrt.config(state=NORMAL)
                                lrt.delete(0,END)
                                lrt.insert(0, F"{LRT}")
                                lrt.config(state="readonly")
                                set_colored_value(lrt,LRT)


                                isd.config(state=NORMAL)
                                isd.delete(0,END)
                                isd.insert(0, f"{ISD}")
                                isd.config(state="readonly")
                                set_colored_value(isd,ISD)

                                drift.config(state=NORMAL)
                                drift.delete(0,END)
                                drift.insert(0, f"{DRIFT}")
                                drift.config(state="readonly")
                                set_colored_value(drift,DRIFT)

                                SI.config(state=NORMAL)
                                SI.delete(0,END)
                                SI.insert(0, f"{SVID}")
                                SI.config(state="readonly")
                                set_colored_value(SI,SVID)

                                iode.config(state=NORMAL)
                                iode.delete(0,END)
                                iode.insert(0, f"{IODE}")
                                iode.config(state="readonly")
                                set_colored_value(iode,IODE)

                                crs.config(state=NORMAL)
                                crs.delete(0,END)
                                crs.insert(0, f"{CRS}")
                                crs.config(state="readonly")
                                set_colored_value(crs,CRS)

                                svid1.config(state=NORMAL)
                                svid1.delete(0,END)
                                svid1.insert(0, f"{SVID1}")
                                svid1.config(state="readonly")
                                set_colored_value(svid1,SVID1)

                                svid2.config(state=NORMAL)
                                svid2.delete(0,END)
                                svid2.insert(0, f"{SVID2}")
                                svid2.config(state="readonly")
                                set_colored_value(svid2,SVID2)

                                svid3.config(state=NORMAL)
                                svid3.delete(0,END)
                                svid3.insert(0, f"{SVID3}")
                                svid3.config(state="readonly")
                                set_colored_value(svid3,SVID3)

                                svid4.config(state=NORMAL)
                                svid4.delete(0,END)
                                svid4.insert(0, f"{SVID4}")
                                svid4.config(state="readonly")
                                set_colored_value(svid4,SVID4)

                                svid5.config(state=NORMAL)
                                svid5.delete(0,END)
                                svid5.insert(0, f"{SVID5}")
                                svid5.config(state="readonly")
                                set_colored_value(svid5,SVID5)

                                svid6.config(state=NORMAL)
                                svid6.delete(0,END)
                                svid6.insert(0, f"{SVID6}")
                                svid6.config(state="readonly")
                                set_colored_value(svid6,SVID6)

                                svid7.config(state=NORMAL)
                                svid7.delete(0,END)
                                svid7.insert(0, f"{SVID7}")
                                svid7.config(state="readonly")
                                set_colored_value(svid7,SVID7)

                                svid8.config(state=NORMAL)
                                svid8.delete(0,END)
                                svid8.insert(0, f"{SVID8}")
                                svid8.config(state="readonly")
                                set_colored_value(svid8,SVID8)

                                svid9.config(state=NORMAL)
                                svid9.delete(0,END)
                                svid9.insert(0, f"{SVID9}")
                                svid9.config(state="readonly")
                                set_colored_value(svid9,SVID9)

                                svid10.config(state=NORMAL)
                                svid10.delete(0,END)
                                svid10.insert(0, f"{SVID10}")
                                svid10.config(state="readonly")
                                set_colored_value(svid10,SVID10)

                                svid11.config(state=NORMAL)
                                svid11.delete(0,END)
                                svid11.insert(0, f"{SVID11}")
                                svid11.config(fg="green")
                                svid11.config(state="readonly")
                                set_colored_value(svid11,SVID11)

                                svid12.config(state=NORMAL)
                                svid12.delete(0,END)
                                svid12.insert(0, f"{SVID12}")
                                svid12.config(state="readonly")
                                set_colored_value(svid12,SVID12)

                                cndr1.config(state=NORMAL)
                                cndr1.delete(0,END)
                                cndr1.insert(0, f"{CNDR1}")
                                cndr1.config(state="readonly")
                                set_colored_value(cndr1, CNDR1)

                                cndr2.config(state=NORMAL)
                                cndr2.delete(0,END)
                                cndr2.insert(0, f"{CNDR2}")
                                cndr2.config(state="readonly")
                                set_colored_value(cndr2, CNDR2)

                                cndr3.config(state=NORMAL)
                                cndr3.delete(0,END)
                                cndr3.insert(0, f"{CNDR3}")
                                cndr3.config(state="readonly")
                                set_colored_value(cndr3, CNDR3)

                                cndr4.config(state=NORMAL)
                                cndr4.delete(0,END)
                                cndr4.insert(0, f"{CNDR4}")
                                cndr4.config(state="readonly")
                                set_colored_value(cndr4, CNDR4)

                                cndr5.config(state=NORMAL)
                                cndr5.delete(0,END)
                                cndr5.insert(0, f"{CNDR5}")
                                cndr5.config(state="readonly")
                                set_colored_value(cndr5, CNDR5)

                                cndr6.config(state=NORMAL)
                                cndr6.delete(0,END)
                                cndr6.insert(0, f"{CNDR6}")
                                cndr6.config(state="readonly")
                                set_colored_value(cndr6, CNDR6)

                                cndr7.config(state=NORMAL)
                                cndr7.delete(0,END)
                                cndr7.insert(0, f"{CNDR7}")
                                cndr7.config(state="readonly")
                                set_colored_value(cndr7, CNDR7)

                                cndr8.config(state=NORMAL)
                                cndr8.delete(0,END)
                                cndr8.insert(0, f"{CNDR8}")
                                cndr8.config(state="readonly")
                                set_colored_value(cndr8, CNDR8)

                                cndr9.config(state=NORMAL)
                                cndr9.delete(0,END)
                                cndr9.insert(0, f"{CNDR9}")
                                cndr9.config(state="readonly")
                                set_colored_value(cndr9, CNDR9)

                                cndr10.config(state=NORMAL)
                                cndr10.delete(0,END)
                                cndr10.insert(0, f"{CNDR10}")
                                cndr10.config(state="readonly")
                                set_colored_value(cndr10, CNDR10)

                                cndr11.config(state=NORMAL)
                                cndr11.delete(0,END)
                                cndr11.insert(0, f"{CNDR11}")
                                cndr11.config(fg="green")
                                cndr11.config(state="readonly")
                                set_colored_value(cndr11, CNDR11)

                                cndr12.config(state=NORMAL)
                                cndr12.delete(0,END)
                                cndr12.insert(0, f"{CNDR12}")
                                cndr12.config(state="readonly")
                                set_colored_value(cndr12, CNDR12)

                                refresh_cndr_plot()

                                t1.config(state=NORMAL)
                                t1.delete(0,END)
                                t1.insert(0, T_flag_display[0])
                                t1.config(state="readonly")

                                t2.config(state=NORMAL)
                                t2.delete(0,END)
                                t2.insert(0, T_flag_display[1])
                                t2.config(state="readonly")

                                t3.config(state=NORMAL)
                                t3.delete(0,END)
                                t3.insert(0, T_flag_display[2])
                                t3.config(state="readonly")

                                t4.config(state=NORMAL)
                                t4.delete(0,END)
                                t4.insert(0, T_flag_display[3])
                                t4.config(state="readonly")

                                t5.config(state=NORMAL)
                                t5.delete(0,END)
                                t5.insert(0, T_flag_display[4])
                                t5.config(state="readonly")

                                t6.config(state=NORMAL)
                                t6.delete(0,END)
                                t6.insert(0, T_flag_display[5])
                                t6.config(state="readonly")

                                t7.config(state=NORMAL)
                                t7.delete(0,END)
                                t7.insert(0, T_flag_display[6])
                                t7.config(state="readonly")

                                t8.config(state=NORMAL)
                                t8.delete(0,END)
                                t8.insert(0, T_flag_display[7])
                                t8.config(state="readonly")

                                t9.config(state=NORMAL)
                                t9.delete(0,END)
                                t9.insert(0, t9_flag )
                                t9.config(state="readonly")

                                t10.config(state=NORMAL)
                                t10.delete(0,END)
                                t10.insert(0, t10_flag )
                                t10.config(state="readonly")

                                t11.config(state=NORMAL)
                                t11.delete(0,END)
                                t11.insert(0, t11_flag )
                                t11.config(state="readonly")

                                t12.config(state=NORMAL)
                                t12.delete(0,END)
                                t12.insert(0, t12_flag )
                                t12.config(state="readonly")

                                d1.config(state=NORMAL)
                                d1.delete(0,END)
                                d1.insert(0, D_flag_display[0])
                                d1.config(state="readonly")
                                set_status_colored(d1,D_flag_display[0])

                                d2.config(state=NORMAL)
                                d2.delete(0,END)
                                d2.insert(0, D_flag_display[1])
                                d2.config(state="readonly")

                                d3.config(state=NORMAL)
                                d3.delete(0,END)
                                d3.insert(0, D_flag_display[2])
                                d3.config(state="readonly")

                                d4.config(state=NORMAL)
                                d4.delete(0,END)
                                d4.insert(0, D_flag_display[3])
                                d4.config(state="readonly")

                                d5.config(state=NORMAL)
                                d5.delete(0,END)
                                d5.insert(0, D_flag_display[4])
                                d5.config(state="readonly")

                                d6.config(state=NORMAL)
                                d6.delete(0,END)
                                d6.insert(0, D_flag_display[5])
                                d6.config(state="readonly")

                                d7.config(state=NORMAL)
                                d7.delete(0,END)
                                d7.insert(0, D_flag_display[6])
                                d7.config(state="readonly")

                                d8.config(state=NORMAL)
                                d8.delete(0,END)
                                d8.insert(0, D_flag_display[7])
                                d8.config(state="readonly")

                                d9.config(state=NORMAL)
                                d9.delete(0,END)
                                d9.insert(0, d9_flag )
                                d9.config(state="readonly")

                                d10.config(state=NORMAL)
                                d10.delete(0,END)
                                d10.insert(0, d10_flag )
                                d10.config(state="readonly")

                                d11.config(state=NORMAL)
                                d11.delete(0,END)
                                d11.insert(0, d11_flag )
                                d11.config(state="readonly")

                                d12.config(state=NORMAL)
                                d12.delete(0,END)
                                d12.insert(0, d12_flag )
                                d12.config(state="readonly")



                                e1.config(state=NORMAL)
                                e1.delete(0,END)
                                e1.insert(0, ephem_flag_display[0])
                                e1.config(state="readonly")

                                e2.config(state=NORMAL)
                                e2.delete(0,END)
                                e2.insert(0, ephem_flag_display[1])
                                e2.config(state="readonly")

                                e3.config(state=NORMAL)
                                e3.delete(0,END)
                                e3.insert(0, ephem_flag_display[2])
                                e3.config(state="readonly")

                                e4.config(state=NORMAL)
                                e4.delete(0,END)
                                e4.insert(0, ephem_flag_display[3])
                                e4.config(state="readonly")

                                e5.config(state=NORMAL)
                                e5.delete(0,END)
                                e5.insert(0, ephem_flag_display[4])
                                e5.config(state="readonly")

                                e6.config(state=NORMAL)
                                e6.delete(0,END)
                                e6.insert(0, ephem_flag_display[5])
                                e6.config(state="readonly")

                                e7.config(state=NORMAL)
                                e7.delete(0,END)
                                e7.insert(0, ephem_flag_display[6])
                                e7.config(state="readonly")

                                e8.config(state=NORMAL)
                                e8.delete(0,END)
                                e8.insert(0, ephem_flag_display[7])
                                e8.config(state="readonly")

                                e9.config(state=NORMAL)
                                e9.delete(0,END)
                                e9.insert(0, e9_flag )
                                e9.config(state="readonly")

                                e10.config(state=NORMAL)
                                e10.delete(0,END)
                                e10.insert(0, e10_flag )
                                e10.config(state="readonly")

                                e11.config(state=NORMAL)
                                e11.delete(0,END)
                                e11.insert(0, e11_flag )
                                e11.config(state="readonly")

                                e12.config(state=NORMAL)
                                e12.delete(0,END)
                                e12.insert(0, e12_flag )
                                e12.config(state="readonly")



                                p1.config(state=NORMAL)
                                p1.delete(0,END)
                                p1.insert(0, constel_flag_display[0])
                                p1.config(state="readonly")

                                p2.config(state=NORMAL)
                                p2.delete(0,END)
                                p2.insert(0, constel_flag_display[1])
                                p2.config(state="readonly")

                                p3.config(state=NORMAL)
                                p3.delete(0,END)
                                p3.insert(0, constel_flag_display[2])
                                p3.config(state="readonly")

                                p4.config(state=NORMAL)
                                p4.delete(0,END)
                                p4.insert(0, constel_flag_display[3])
                                p4.config(state="readonly")

                                p5.config(state=NORMAL)
                                p5.delete(0,END)
                                p5.insert(0, constel_flag_display[4])
                                p5.config(state="readonly")

                                p6.config(state=NORMAL)
                                p6.delete(0,END)
                                p6.insert(0, constel_flag_display[5])
                                p6.config(state="readonly")

                                p7.config(state=NORMAL)
                                p7.delete(0,END)
                                p7.insert(0, constel_flag_display[6])
                                p7.config(state="readonly")

                                p8.config(state=NORMAL)
                                p8.delete(0,END)
                                p8.insert(0, constel_flag_display[7])
                                p8.config(state="readonly")

                                p9.config(state=NORMAL)
                                p9.delete(0,END)
                                p9.insert(0, p9_flag )
                                p9.config(state="readonly")

                                p10.config(state=NORMAL)
                                p10.delete(0,END)
                                p10.insert(0, p10_flag )
                                p10.config(state="readonly")

                                p11.config(state=NORMAL)
                                p11.delete(0,END)
                                p11.insert(0, p11_flag )
                                p11.config(state="readonly")

                                p12.config(state=NORMAL)
                                p12.delete(0,END)
                                p12.insert(0, p12_flag )
                                p12.config(state="readonly")

                                h1.config(state=NORMAL)
                                h1.delete(0,END)
                                h1.insert(0, H_flag_display[0])
                                h1.config(state="readonly")

                                h2.config(state=NORMAL)
                                h2.delete(0,END)
                                h2.insert(0, H_flag_display[1])
                                h2.config(state="readonly")

                                h3.config(state=NORMAL)
                                h3.delete(0,END)
                                h3.insert(0, H_flag_display[2])
                                h3.config(state="readonly")

                                h4.config(state=NORMAL)
                                h4.delete(0,END)
                                h4.insert(0, H_flag_display[3])
                                h4.config(state="readonly")

                                h5.config(state=NORMAL)
                                h5.delete(0,END)
                                h5.insert(0, H_flag_display[4])
                                h5.config(state="readonly")

                                h6.config(state=NORMAL)
                                h6.delete(0,END)
                                h6.insert(0, H_flag_display[5])
                                h6.config(state="readonly")

                                h7.config(state=NORMAL)
                                h7.delete(0,END)
                                h7.insert(0, H_flag_display[6])
                                h7.config(state="readonly")

                                h8.config(state=NORMAL)
                                h8.delete(0,END)
                                h8.insert(0, H_flag_display[7])
                                h8.config(state="readonly")

                                h9.config(state=NORMAL)
                                h9.delete(0,END)
                                h9.insert(0, H_flag_display[8])
                                h9.config(state="readonly")

                                h10.config(state=NORMAL)
                                h10.delete(0,END)
                                h10.insert(0, H_flag_display[9])
                                h10.config(state="readonly")

                                h11.config(state=NORMAL)
                                h11.delete(0,END)
                                h11.insert(0, H_flag_display[10])
                                h11.config(state="readonly")

                                h12.config(state=NORMAL)
                                h12.delete(0,END)
                                h12.insert(0, H_flag_display[11])
                                h12.config(state="readonly")

                                i1.config(state=NORMAL)
                                i1.delete(0,END)
                                i1.insert(0, I_flag_display[0])
                                i1.config(state="readonly")

                                i2.config(state=NORMAL)
                                i2.delete(0,END)
                                i2.insert(0, I_flag_display[1])
                                i2.config(state="readonly")

                                i3.config(state=NORMAL)
                                i3.delete(0,END)
                                i3.insert(0, I_flag_display[2])
                                i3.config(state="readonly")

                                i4.config(state=NORMAL)
                                i4.delete(0,END)
                                i4.insert(0, I_flag_display[3])
                                i4.config(state="readonly")

                                i5.config(state=NORMAL)
                                i5.delete(0,END)
                                i5.insert(0, I_flag_display[4])
                                i5.config(state="readonly")

                                i6.config(state=NORMAL)
                                i6.delete(0,END)
                                i6.insert(0, I_flag_display[5])
                                i6.config(state="readonly")

                                i7.config(state=NORMAL)
                                i7.delete(0,END)
                                i7.insert(0, I_flag_display[6])
                                i7.config(state="readonly")

                                i8.config(state=NORMAL)
                                i8.delete(0,END)
                                i8.insert(0, I_flag_display[7])
                                i8.config(state="readonly")

                                i9.config(state=NORMAL)
                                i9.delete(0,END)
                                i9.insert(0, I_flag_display[8])
                                i9.config(state="readonly")

                                i10.config(state=NORMAL)
                                i10.delete(0,END)
                                i10.insert(0, I_flag_display[9])
                                i10.config(state="readonly")

                                i11.config(state=NORMAL)
                                i11.delete(0,END)
                                i11.insert(0, I_flag_display[10])
                                i11.config(state="readonly")

                                i12.config(state=NORMAL)
                                i12.delete(0,END)
                                i12.insert(0, I_flag_display[11])
                                i12.config(state="readonly")

                                a1.config(state=NORMAL)
                                a1.delete(0,END)
                                a1.insert(0, A_flag_display[0])
                                a1.config(state="readonly")

                                a2.config(state=NORMAL)
                                a2.delete(0,END)
                                a2.insert(0, A_flag_display[1])
                                a2.config(state="readonly")

                                a3.config(state=NORMAL)
                                a3.delete(0,END)
                                a3.insert(0, A_flag_display[2])
                                a3.config(state="readonly")

                                a4.config(state=NORMAL)
                                a4.delete(0,END)
                                a4.insert(0, A_flag_display[3])
                                a4.config(state="readonly")

                                a5.config(state=NORMAL)
                                a5.delete(0,END)
                                a5.insert(0, A_flag_display[4])
                                a5.config(state="readonly")

                                a6.config(state=NORMAL)
                                a6.delete(0,END)
                                a6.insert(0, A_flag_display[5])
                                a6.config(state="readonly")

                                a7.config(state=NORMAL)
                                a7.delete(0,END)
                                a7.insert(0, A_flag_display[6])
                                a7.config(state="readonly")

                                a8.config(state=NORMAL)
                                a8.delete(0,END)
                                a8.insert(0, A_flag_display[7])
                                a8.config(state="readonly")

                                a9.config(state=NORMAL)
                                a9.delete(0,END)
                                a9.insert(0, A_flag_display[8])
                                a9.config(state="readonly")

                                a10.config(state=NORMAL)
                                a10.delete(0,END)
                                a10.insert(0, A_flag_display[9])
                                a10.config(state="readonly")

                                a11.config(state=NORMAL)
                                a11.delete(0,END)
                                a11.insert(0, A_flag_display[10])
                                a11.config(state="readonly")

                                a12.config(state=NORMAL)
                                a12.delete(0,END)
                                a12.insert(0, A_flag_display[11])
                                a12.config(state="readonly")

                                r1.config(state=NORMAL)
                                r1.delete(0,END)
                                r1.insert(0, R_flag_display[0])
                                r1.config(state="readonly")

                                r2.config(state=NORMAL)
                                r2.delete(0,END)
                                r2.insert(0, R_flag_display[1])
                                r2.config(state="readonly")

                                r3.config(state=NORMAL)
                                r3.delete(0,END)
                                r3.insert(0, R_flag_display[2])
                                r3.config(state="readonly")

                                r4.config(state=NORMAL)
                                r4.delete(0,END)
                                r4.insert(0, R_flag_display[3])
                                r4.config(state="readonly")

                                r5.config(state=NORMAL)
                                r5.delete(0,END)
                                r5.insert(0, R_flag_display[4])
                                r5.config(state="readonly")

                                r6.config(state=NORMAL)
                                r6.delete(0,END)
                                r6.insert(0, R_flag_display[5])
                                r6.config(state="readonly")

                                r7.config(state=NORMAL)
                                r7.delete(0,END)
                                r7.insert(0, R_flag_display[6])
                                r7.config(state="readonly")

                                r8.config(state=NORMAL)
                                r8.delete(0,END)
                                r8.insert(0, R_flag_display[7])
                                r8.config(state="readonly")

                                r9.config(state=NORMAL)
                                r9.delete(0,END)
                                r9.insert(0, R_flag_display[8])
                                r9.config(state="readonly")

                                r10.config(state=NORMAL)
                                r10.delete(0,END)
                                r10.insert(0, R_flag_display[9])
                                r10.config(state="readonly")

                                r11.config(state=NORMAL)
                                r11.delete(0,END)
                                r11.insert(0, R_flag_display[10])
                                r11.config(state="readonly")

                                r12.config(state=NORMAL)
                                r12.delete(0,END)
                                r12.insert(0, R_flag_display[11])
                                r12.config(state="readonly")


                                iode1.config(state=NORMAL)
                                iode1.delete(0,END)
                                iode1.insert(0, f"{IODE1}")
                                iode1.config(state="readonly")
                                set_colored_value(iode1,IODE1)

                                iode2.config(state=NORMAL)
                                iode2.delete(0,END)
                                iode2.insert(0, f"{IODE2}")
                                iode2.config(state="readonly")
                                set_colored_value(iode2,IODE2)

                                iode3.config(state=NORMAL)
                                iode3.delete(0,END)
                                iode3.insert(0, f"{IODE3}")
                                iode3.config(state="readonly")
                                set_colored_value(iode3,IODE3)

                                iode4.config(state=NORMAL)
                                iode4.delete(0,END)
                                iode4.insert(0, f"{IODE4}")
                                iode4.config(state="readonly")
                                set_colored_value(iode4,IODE4)

                                iode5.config(state=NORMAL)
                                iode5.delete(0,END)
                                iode5.insert(0, f"{IODE5}")
                                iode5.config(state="readonly")
                                set_colored_value(iode5,IODE5)

                                iode6.config(state=NORMAL)
                                iode6.delete(0,END)
                                iode6.insert(0, f"{IODE6}")
                                iode6.config(state="readonly")
                                set_colored_value(iode6,IODE6)

                                iode7.config(state=NORMAL)
                                iode7.delete(0,END)
                                iode7.insert(0, f"{IODE7}")
                                iode7.config(state="readonly")
                                set_colored_value(iode7,IODE7)

                                iode8.config(state=NORMAL)
                                iode8.delete(0,END)
                                iode8.insert(0, f"{IODE8}")
                                iode8.config(state="readonly")
                                set_colored_value(iode8,IODE8)

                                iode9.config(state=NORMAL)
                                iode9.delete(0,END)
                                iode9.insert(0, f"{IODE9}")
                                iode9.config(state="readonly")
                                set_colored_value(iode9,IODE9)

                                iode10.config(state=NORMAL)
                                iode10.delete(0,END)
                                iode10.insert(0, f"{IODE10}")
                                iode10.config(state="readonly")
                                set_colored_value(iode10,IODE10)

                                iode11.config(state=NORMAL)
                                iode11.delete(0,END)
                                iode11.insert(0, f"{IODE11}")
                                iode11.config(fg="green")
                                iode11.config(state="readonly")
                                set_colored_value(iode11,IODE11)

                                iode12.config(state=NORMAL)
                                iode12.delete(0,END)
                                iode12.insert(0, f"{IODE12}")
                                iode12.config(state="readonly")
                                set_colored_value(iode12,IODE12)

                                pr1.config(state=NORMAL)
                                pr1.delete(0,END)
                                pr1.insert(0, f"{PR1}")
                                pr1.config(state="readonly")
                                set_colored_value(pr1,PR1)

                                pr2.config(state=NORMAL)
                                pr2.delete(0,END)
                                pr2.insert(0, f"{PR2}")
                                pr2.config(state="readonly")
                                set_colored_value(pr2,PR2)

                                pr3.config(state=NORMAL)
                                pr3.delete(0,END)
                                pr3.insert(0, f"{PR3}")
                                pr3.config(state="readonly")
                                set_colored_value(pr3,PR3)

                                pr4.config(state=NORMAL)
                                pr4.delete(0,END)
                                pr4.insert(0, f"{PR4}")
                                pr4.config(state="readonly")
                                set_colored_value(pr4,PR4)

                                pr5.config(state=NORMAL)
                                pr5.delete(0,END)
                                pr5.insert(0, f"{PR5}")
                                pr5.config(state="readonly")
                                set_colored_value(pr5,PR5)

                                pr6.config(state=NORMAL)
                                pr6.delete(0,END)
                                pr6.insert(0, f"{PR6}")
                                pr6.config(state="readonly")
                                set_colored_value(pr6,PR6)

                                pr7.config(state=NORMAL)
                                pr7.delete(0,END)
                                pr7.insert(0, f"{PR7}")
                                pr7.config(state="readonly")
                                set_colored_value(pr7,PR7)

                                pr8.config(state=NORMAL)
                                pr8.delete(0,END)
                                pr8.insert(0, f"{PR8}")
                                pr8.config(state="readonly")
                                set_colored_value(pr8,PR8)

                                pr9.config(state=NORMAL)
                                pr9.delete(0,END)
                                pr9.insert(0, f"{PR9}")
                                pr9.config(state="readonly")
                                set_colored_value(pr9,PR9)

                                pr10.config(state=NORMAL)
                                pr10.delete(0,END)
                                pr10.insert(0, f"{PR10}")
                                pr10.config(state="readonly")
                                set_colored_value(pr10,PR10)

                                pr11.config(state=NORMAL)
                                pr11.delete(0,END)
                                pr11.insert(0, f"{PR11}")
                                pr11.config(fg="green")
                                pr11.config(state="readonly")
                                set_colored_value(pr11,PR11)

                                pr12.config(state=NORMAL)
                                pr12.delete(0,END)
                                pr12.insert(0, f"{PR12}")
                                pr12.config(state="readonly")
                                set_colored_value(pr12,PR12)

                                dr1.config(state=NORMAL)
                                dr1.delete(0,END)
                                dr1.insert(0, f"{DR1}")
                                dr1.config(state="readonly")
                                set_colored_value(dr1,DR1)

                                dr2.config(state=NORMAL)
                                dr2.delete(0,END)
                                dr2.insert(0, f"{DR2}")
                                dr2.config(state="readonly")
                                set_colored_value(dr2,DR2)

                                dr3.config(state=NORMAL)
                                dr3.delete(0,END)
                                dr3.insert(0, f"{DR3}")
                                dr3.config(state="readonly")
                                set_colored_value(dr3,DR3)

                                dr4.config(state=NORMAL)
                                dr4.delete(0,END)
                                dr4.insert(0, f"{DR4}")
                                dr4.config(state="readonly")
                                set_colored_value(dr4,DR4)

                                dr5.config(state=NORMAL)
                                dr5.delete(0,END)
                                dr5.insert(0, f"{DR5}")
                                dr5.config(state="readonly")
                                set_colored_value(dr5,DR5)

                                dr6.config(state=NORMAL)
                                dr6.delete(0,END)
                                dr6.insert(0, f"{DR6}")
                                dr6.config(state="readonly")
                                set_colored_value(dr6,DR6)

                                dr7.config(state=NORMAL)
                                dr7.delete(0,END)
                                dr7.insert(0, f"{DR7}")
                                dr7.config(state="readonly")
                                set_colored_value(dr7,DR7)

                                dr8.config(state=NORMAL)
                                dr8.delete(0,END)
                                dr8.insert(0, f"{DR8}")
                                dr8.config(state="readonly")
                                set_colored_value(dr8,DR8)

                                dr9.config(state=NORMAL)
                                dr9.delete(0,END)
                                dr9.insert(0, f"{DR9}")
                                dr9.config(state="readonly")
                                set_colored_value(dr9,DR9)

                                dr10.config(state=NORMAL)
                                dr10.delete(0,END)
                                dr10.insert(0, f"{DR10}")
                                dr10.config(state="readonly")
                                set_colored_value(dr10,DR10)

                                dr11.config(state=NORMAL)
                                dr11.delete(0,END)
                                dr11.insert(0, f"{DR11}")
                                dr11.config(state="readonly")
                                set_colored_value(dr11,DR11)

                                dr12.config(state=NORMAL)
                                dr12.delete(0,END)
                                dr12.insert(0, f"{DR12}")
                                dr12.config(state="readonly")
                                set_colored_value(dr12,DR12)

                                tele_cmd_counter.config(state=NORMAL)
                                tele_cmd_counter.delete(0,END)
                                tele_cmd_counter.insert(0, f"{TELE_CMD_COUNTER}")
                                tele_cmd_counter.config(state="readonly")
                                set_colored_value(tele_cmd_counter,TELE_CMD_COUNTER)

                                upset_cmd_counter.config(state=NORMAL)
                                upset_cmd_counter.delete(0,END)
                                upset_cmd_counter.insert(0, f"{UPSET_COUNTER}")
                                upset_cmd_counter.config(state="readonly")
                                set_colored_value(upset_cmd_counter,UPSET_COUNTER)

                                mux_entry.config(state=NORMAL)
                                mux_entry.delete(0,END)
                                mux_entry.insert(0, f"{decoded_data}")
                                mux_entry.config(state="readonly")
                                #set_colored_value(mux_entry,decoded_data)

                                odp.config(state=NORMAL)
                                odp.delete(0,END)
                                odp.insert(0, odp_status)
                                odp.config(state="readonly")
                                set_status_colored(odp,odp_status)

                                phase_center.config(state=NORMAL)
                                phase_center.delete(0,END)
                                phase_center.insert(0, phase_corr)
                                phase_center.config(state="readonly")
                                set_status_colored(phase_center,phase_corr)

                                phase_center_sps.config(state=NORMAL)
                                phase_center_sps.delete(0,END)
                                phase_center_sps.insert(0, phase_corr_sps)
                                phase_center_sps.config(state="readonly")
                                set_status_colored(phase_center_sps,phase_corr_sps)

                                port1.config(state=NORMAL)
                                port1.delete(0,END)
                                port1.insert(0, port1_config)
                                port1.config(state="readonly")
                                #set_colored_value(port1,port1_config)

                                port2.config(state=NORMAL)
                                port2.delete(0,END)
                                port2.insert(0, port2_config)
                                port2.config(state="readonly")
                                #set_colored_value(port2,port2_config)

                                sol.config(state=NORMAL)
                                sol.delete(0,END)
                                sol.insert(0, Sol)
                                sol.config(state="readonly")
                                #set_colored_value(sol,Sol)

                                pos_e.config(state=NORMAL)
                                pos_e.delete(0,END)
                                pos_e.insert(0, Pos_E)
                                pos_e.config(state="readonly")
                                #set_colored_value(pos_e,Pos_E)

                                alm.config(state=NORMAL)
                                alm.delete(0,END)
                                alm.insert(0, ALM)
                                alm.config(state="readonly")
                                #set_colored_value(alm,ALM)

                                time.config(state=NORMAL)
                                time.delete(0,END)
                                time.insert(0, Time)
                                time.config(state="readonly")
                                #set_colored_value(time,Time)

                                d2_3d.config(state=NORMAL)
                                d2_3d.delete(0,END)
                                d2_3d.insert(0, D2_3D_config)
                                d2_3d.config(state="readonly")
                                #set_colored_value(d2_3d,D2_3D_config)

                                pos.config(state=NORMAL)
                                pos.delete(0,END)
                                pos.insert(0, Pos)
                                pos.config(state="readonly")
                                #set_colored_value(pos,Pos)

                                ccsds.config(state=NORMAL)
                                ccsds.delete(0,END)
                                ccsds.insert(0, ccsds_flag)
                                ccsds.config(state="readonly")
                                set_status_colored(ccsds,ccsds_flag)

                                rand.config(state=NORMAL)
                                rand.delete(0,END)
                                rand.insert(0, randomizer_flag)
                                rand.config(state="readonly")
                                set_status_colored(rand,randomizer_flag)

                                space_crf_id.config(state=NORMAL)
                                space_crf_id.delete(0,END)
                                space_crf_id.insert(0, Spacecraft_id)
                                space_crf_id.config(state="readonly")
                                #set_status_colored(space_crf_id,Spacecraft_id)

                                navic_cmd.config(state=NORMAL)
                                navic_cmd.delete(0,END)
                                navic_cmd.insert(0, Navic_cmd)
                                navic_cmd.config(state="readonly")
                                set_colored_value(navic_cmd,Navic_cmd)

                                tmillcond.config(state=NORMAL)
                                tmillcond.delete(0,END)
                                tmillcond.insert(0, ill_cnd_val)
                                tmillcond.config(state="readonly")

                                tmillcondlim.config(state=NORMAL)
                                tmillcondlim.delete(0,END)
                                tmillcondlim.insert(0, ill_cnd_Limit)
                                tmillcondlim.config(state="readonly")

                                pre_chk_cntr.config(state=NORMAL)
                                pre_chk_cntr.delete(0,END)
                                pre_chk_cntr.insert(0, pre_cntr)
                                pre_chk_cntr.config(state="readonly")

                                post_chk_cntr.config(state=NORMAL)
                                post_chk_cntr.delete(0,END)
                                post_chk_cntr.insert(0, post_cntr)
                                post_chk_cntr.config(state="readonly")

                                cond_pre.config(state=NORMAL)
                                cond_pre.delete(0,END)
                                cond_pre.insert(0, cond_pre_check)
                                cond_pre.config(state="readonly")

                                cond_post.config(state=NORMAL)
                                cond_post.delete(0,END)
                                cond_post.insert(0, cond_post_check)
                                cond_post.config(state="readonly")
                                
                                orbit_ph.config(state=NORMAL)
                                orbit_ph.delete(0,END)
                                orbit_ph.insert(0, Orbit_phase)
                                orbit_ph.config(state="readonly")

                                odp_prop.config(state=NORMAL)
                                odp_prop.delete(0,END)
                                odp_prop.insert(0, ODP_prop_used)
                                odp_prop.config(state="readonly")


                                raw_data.config(state=NORMAL)
                                raw_data.delete(0,END)
                                raw_data.insert(0, SA29_Raw)
                                raw_data.config(state="readonly")



                                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                                base_name = file_entry1.get()

                                '''data_row = [current_timestamp,SYN_Second,SYN_NanoSecond,SYN_Weeknumber]
                                write_to_SYN(data_row,base_name)'''

                                data_row = [Raw_data]
                                write_to_raw(data_row,base_name)

                                data_row = [current_timestamp,hexDecodedData]
                                write_to_raw_withheader1(data_row,base_name)




                                data_row = [current_timestamp,SYS_Second,SYS_NanoSecond,SYS_Weeknumber,
                                            PPS_Sec,PPS_NanoSec,PPS_Week,PPS_3D,
                                            INT_x,INT_y,INT_z,INT_vx,INT_vy,INT_vz,
                                            EST_x,EST_y,EST_z,EST_vx,EST_vy,EST_vz,
                                            UpdateCounter,MC,TELE_CMD_COUNTER,UPSET_COUNTER,
                                            checksum,checksum1,ODP_FLAG,PDOP,
                                            CLOCKBIAS,INTER_SYSTEM_BIAS,DRIFT,ISD,Steering_Bias,
                                            Steering_Drift,Steering_clock,U1_data,U2_data,
                                            Last_cmd_excuted_byte1_2,Last_cmd_excuted_byte3,Last_cmd_excuted_byte4,ACQ1_SVID,SWDT_RST_COUNTER]

                                str_Est = decoded32["Str_Est"]
                                str_En = decoded32["Str_En"]
                                reset_C = decoded32["Reset_C"]
                                init = decoded32["Init"]

                                data_row.extend([str_Est, str_En, reset_C,init]),


                                hwdt_reset_counter = decoded25["HWDT Reset Counter"]
                                swdt_reset_id = decoded25["SWDT Reset ID"]
                                pb_storage_mode = decoded25["PB Storage Mode"]

                                data_row.extend([hwdt_reset_counter, swdt_reset_id, pb_storage_mode]),

                                interupt_cmd = decoded_cmd["Interupt CMD Counter"]
                                no_of_sat = decoded_cmd["No Of Satellite"]

                                data_row.extend([interupt_cmd,no_of_sat])

                                valid_1553_cmd_counter = decoded_wdt["Valid 1553 CMD CTR"]
                                tm_selection = decoded_wdt["TM Selection"]
                                sw_line_status=decoded_wdt["SW Line/WDT Status"]
                                hw_wdt_status = decoded_wdt["HW WDT Status"]
                                mnv_status = decoded_wdt["MNV Status"]
                                sps_sw_status = decoded_wdt["SPS Software Status"]


                                data_row.extend([valid_1553_cmd_counter, tm_selection, sw_line_status,hw_wdt_status,mnv_status,sps_sw_status])


                                iono_smoothing = decoded_flags["Iono Smoothing"]
                                inono_enable = decoded_flags["INONO Enable"]
                                gp2015_lock = decoded_flags["GP2015 Lock"]
                                rffc5071_lock = decoded_flags["RFFC5071 Lock"]
                                nav_1a = decoded_flags["Nav 1A"]
                                velocity_smoothing = decoded_flags["Velocity Smoothing"]
                                gps2015_ant2_lock = decoded_flags["GPS2015 Ant2 Lock"]
                                raim = decoded_flags["RAIM"]
                                carrier_smoothing = decoded_flags["Carrier Smoothing"]
                                system_mode = decoded_flags["System Mode"]
                                time_aligned_to = decoded_flags["Time Aligned To"]
                                data_row.extend([iono_smoothing,inono_enable, gp2015_lock, rffc5071_lock, nav_1a, velocity_smoothing,
                                                 gps2015_ant2_lock, raim, carrier_smoothing, system_mode, time_aligned_to])


                                data_row.extend([LRT,SVID,IODE,CRS,decoded_data,odp_status,phase_corr,phase_corr_sps,port1_config,port2_config,
                                                 Sol,Pos_E,ALM,Time,D2_3D_config,Pos,ccsds_flag,randomizer_flag,Spacecraft_id,Navic_cmd])

                                no_of_input_sat=odp_flags["No of I/P sat to odp"]
                                no_of_sat_est=odp_flags["No of sat est"]
                                filter_init=odp_flags["Filter Init reason"]
                                filter_init_flag=odp_flags["Filter Init Flag"]
                                kf_est_flag=odp_flags["KF Est Flag"]
                                ppp_est_flag=odp_flags["PPP Est Flag Unsing"]
                                ph_center_en_flag=odp_flags["Ph_center En Flag"]
                                data_row.extend([no_of_input_sat,no_of_sat_est,filter_init,filter_init_flag,kf_est_flag,ppp_est_flag,ph_center_en_flag])
                                data_row.extend([ill_cnd_val,ill_cnd_Limit,pre_cntr,post_cntr,Orbit_phase,ODP_prop_used])
                                data_row.extend([
                                            1,SVID1,CNDR1,T_flag_display[0],constel_flag_display[0],ephem_flag_display[0],D_flag_display[0],I_flag_display[0],R_flag_display[0],H_flag_display[0],A_flag_display[0],IODE1,PR1,DR1,
                                            2,SVID2,CNDR2,T_flag_display[1],constel_flag_display[1],ephem_flag_display[1],D_flag_display[1],I_flag_display[1],R_flag_display[1],H_flag_display[1],A_flag_display[1],IODE2,PR2,DR2,
                                            3,SVID3,CNDR3,T_flag_display[2],constel_flag_display[2],ephem_flag_display[2],D_flag_display[2],I_flag_display[2],R_flag_display[2],H_flag_display[2],A_flag_display[2],IODE3,PR3,DR3,
                                            4,SVID4,CNDR4,T_flag_display[3],constel_flag_display[3],ephem_flag_display[3],D_flag_display[3],I_flag_display[3],R_flag_display[3],H_flag_display[3],A_flag_display[3],IODE4,PR4,DR4,
                                            5,SVID5,CNDR5,T_flag_display[4],constel_flag_display[4],ephem_flag_display[4],D_flag_display[4],I_flag_display[4],R_flag_display[4],H_flag_display[4],A_flag_display[4],IODE5,PR5,DR5,
                                            6,SVID6,CNDR6,T_flag_display[5],constel_flag_display[5],ephem_flag_display[5],D_flag_display[5],I_flag_display[5],R_flag_display[5],H_flag_display[5],A_flag_display[5],IODE6,PR6,DR6,
                                            7,SVID7,CNDR7,T_flag_display[6],constel_flag_display[6],ephem_flag_display[6],D_flag_display[6],I_flag_display[6],R_flag_display[6],H_flag_display[6],A_flag_display[6],IODE7,PR7,DR7,
                                            8,SVID8,CNDR8,T_flag_display[7],constel_flag_display[7],ephem_flag_display[7],D_flag_display[7],I_flag_display[7],R_flag_display[7],H_flag_display[7],A_flag_display[7],IODE8,PR8,DR8,
                                            9,SVID9,CNDR9,t9_flag,p9_flag,e9_flag,d9_flag,I_flag_display[8],R_flag_display[8],H_flag_display[8],A_flag_display[8],IODE9,PR9,DR9,
                                            10,SVID10,CNDR10,t10_flag,p10_flag,e10_flag,d10_flag,I_flag_display[9],R_flag_display[9],H_flag_display[9],A_flag_display[9],IODE10,PR10,DR10,
                                            11,SVID11,CNDR11,t11_flag,p11_flag,e11_flag,d11_flag,I_flag_display[10],R_flag_display[10],H_flag_display[10],A_flag_display[10],IODE11,PR11,DR11,
                                            12,SVID12,CNDR12,t12_flag,p12_flag,e12_flag,d12_flag,I_flag_display[11],R_flag_display[11],H_flag_display[11],A_flag_display[11],IODE12,PR12,DR12])

                                write_to_csv(data_row,base_name)

                                pass
                            elif data_type == "header2":

                                header_length = 10
                                Raw_data2 = ' '.join([hexDecodedData[i:i+2]for i in range(header_length,len(hexDecodedData),2)])

                                h2NanoSecond_hex=hexDecodedData[12:20]
                                h2Second_hex=hexDecodedData[20:28]
                                h2Weeknumber_hex=hexDecodedData[28:32]

                                # Convert hex to decimal and scale as needed
                                SYN_h2NanoSecond=reverse_and_concatenate(h2NanoSecond_hex)

                                SYN_h2Second=reverse_and_concatenate(h2Second_hex)

                                SYN_h2WeekNumber=reverse_and_concatenate(h2Weeknumber_hex)

                                time_entry.config(state="normal")
                                time_entry.delete(0,END)
                                time_entry.insert(0, str(SYN_h2Second))
                                time_entry.config(state="readonly")

                                nanotime_entry.config(state="normal")
                                nanotime_entry.delete(0,END)
                                nanotime_entry.insert(0, str(SYN_h2NanoSecond))
                                nanotime_entry.config(state="readonly")

                                week_entry.config(state="normal")
                                week_entry.delete(0,END)
                                week_entry.insert(0, str(SYN_h2WeekNumber))
                                week_entry.config(state="readonly")

                                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                                base_name = file_entry1.get()

                                data_row = [Raw_data2]
                                write_to_rawh2(data_row,base_name)

                                data_row = [current_timestamp,hexDecodedData]
                                write_to_raw_withheader2(data_row,base_name)

                                data_row = [current_timestamp,SYN_h2Second,SYN_h2NanoSecond,SYN_h2WeekNumber]
                                write_to_SYNh2(data_row,base_name)
                                pass
                            elif data_type == "header3":
                                header_length = 10
                                Raw_data3 = ' '.join([hexDecodedData[i:i+2]for i in range(header_length,len(hexDecodedData),2)])
                                base_name = file_entry1.get()

                                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                                data_row = [current_timestamp,hexDecodedData]
                                write_to_raw_withheader3(data_row,base_name)

                                data_row = [Raw_data3]
                                write_to_rawh3(data_row,base_name)

                                pass
                            elif data_type == "header4":
                                header_length = 10
                                Raw_data4 = ' '.join([hexDecodedData[i:i+2]for i in range(header_length,len(hexDecodedData),2)])
                                base_name = file_entry1.get()

                                current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                                data_row = [current_timestamp,hexDecodedData]
                                write_to_raw_withheader4(data_row,base_name)

                                data_row = [Raw_data4]
                                write_to_rawh4(data_row,base_name)



        time.sleep(1)


    except KeyboardInterrupt:
        print("Stopped")


def replay_from_file():
    global replay_running, replay_filepath
    filepath = filedialog.askopenfilename(
        title="Select Raw Data File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not filepath:
        return

    replay_filepath = filepath
    replay_running = True

    filename = os.path.basename(filepath)
    # Schedule button text update on main thread
    root.after(0, btn_replay.config, {'text': filename, 'fg': "blue"})

    threading.Thread(target=process_data, daemon=True).start()
    threading.Thread(target=process_replay_file, args=(filepath,), daemon=True).start()



def stop_replay():
    """Stop button handler."""
    global replay_running
    replay_running = False
    print("⏹ Replay stopped by user.")


def toggle_pause_resume():
    """Toggle between pause and resume."""
    global replay_paused
    if replay_paused:
        replay_paused = False
        btn_pause_resume.config(text="Pause ⏸", bg="lightyellow")
        print("▶ Replay resumed.")
    else:
        replay_paused = True
        btn_pause_resume.config(text="Resume ▶", bg="lightgreen")
        print("⏸ Replay paused.")


def jump_to_sys_sec():
    """Reads value from entry box and sets jump target."""
    global jump_target_sec, replay_running, replay_filepath, replay_paused

    if not replay_filepath:
        print("⚠️ No replay file loaded yet.")
        return

    try:
        val = int(jump_entry.get())
        jump_target_sec = val
        print(f"🔄 Jump requested to SYS_Second = {val}")

        # Always un-pause on jump
        replay_paused = False
        btn_pause_resume.config(text="Pause ⏸", bg="lightyellow")

        # Restart replay fresh
        replay_running = False
        pytime.sleep(0.5)
        replay_running = True
        threading.Thread(target=process_replay_file, args=(replay_filepath,), daemon=True).start()

    except ValueError:
        print("⚠️ Invalid SYS_Second value entered.")


def process_replay_file(filepath):
    """Feeds CSV data to process_data(), supports jump to SYS_Second (fast scan)."""
    global replay_running, replay_paused, jump_target_sec
    import csv

    with open(filepath, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header

        fast_skip_mode = jump_target_sec is not None

        for row in reader:
            if not replay_running:
                break
            if len(row) < 2:
                continue

            hexDecodedData = row[1]

            # --- Extract SYS_Second ---
            SYS_Second_hex = hexDecodedData[148:156]  # word for SYS_Second
            try:
                SYS_Second = reverse_and_concatenate(SYS_Second_hex)
            except:
                continue

            # --- Jump handling (fast skip without sleep) ---
            if jump_target_sec is not None:
                if SYS_Second < jump_target_sec:
                    continue   # skip forward until target
                elif SYS_Second > jump_target_sec:
                    continue   # still skipping
                else:
                    print(f"✅ Jumped! Now starting from SYS_Second={SYS_Second}")
                    jump_target_sec = None
                    fast_skip_mode = False  # disable fast skip
                    # (don’t break, let it fall into normal replay below)

            # --- Normal replay (only header1) ---
            if hexDecodedData.startswith("acca1f0a"):
                data_queue.put(("header1", hexDecodedData))
                print(hexDecodedData)

            # Handle pause
            while replay_paused and replay_running:
                pytime.sleep(0.2)

            # Sleep only if not skipping
            if not fast_skip_mode:
                pytime.sleep(0.5)

    print("✅ Replay finished or stopped.")







def start_thread():
    t1 = threading.Thread(target=readSerial)
    t1.deamon = True
    t1.start()

    t2 = threading.Thread(target=process_data)
    t2.deamon = True
    t2.start()



def connexion():
    global ser, serialData, drop_COM, drop_bd,status_var1

    if connect_btn["text"] == "Disconnect":
        serialData = False  #stop the thread
        connect_btn["text"] = "Connect"
        refresh_btn["state"] = "active"
        drop_bd["state"] = "active"
        drop_COM["state"] = "active"
        file_entry1.config(state="normal")#ENABLE
        project_entry.config(state="normal")#ENABLE
        if ser and ser.is_open:
            ser.close()
        print("Serial port closed")
    else:
        serialData = True
        connect_btn["text"] = "Disconnect"
        refresh_btn["state"] = "disabled"
        drop_bd["state"] = "disabled"
        drop_COM["state"] = "disabled"
        file_entry1.config(state="disabled")#DISABLE
        project_entry.config(state="disabled")#DISABLE
        port = clicked_com.get()
        baud = clicked_bd.get()
        try:
            available_ports = [p.device for p in serial.tools.list_ports.comports()]
            if port not in available_ports:
                status_var1.set(f"❌ {port} is not available. Please refresh!")
                return
            ser = serial.Serial(port, baud, timeout=1)
            start_thread()
            status_var1.set(f"✅ Connected to {port} at {baud} baud.")
        except serial.SerialException as e:
            status_var1.set(f"❌ Serial error: {e}")
        except OSError as e:
            status_var1.set(f"❌ OS error: {e}")
        except Exception as e:
            status_var1.set(f"❌ Unexpected error: {e}")





def close_window():
    global root, serialData,ser
    serialData = False
    if ser in ser.is_open:
        ser.close()
    root.destroy()

if __name__=="__main__":
    connect_menu_init()
