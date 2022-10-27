import csv
import numpy as np
import pandas as pd
import sys
import os
import glob
from pathlib import Path
import json
from pandas.errors import EmptyDataError
from py import process
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input folder containing csv files", required=True)
parser.add_argument("-o", "--output", help="Output csv file", required=True)
args = parser.parse_args()

# Collect all csv files from the training/testing folder
path_to_read = args.input
#path_to_read = "./train_files"
csv_files = glob.glob(os.path.join(path_to_read, "*.csv"))

processed_files = {}

for full_name in csv_files:
    # Get the file name from the full path
    file_name = Path(full_name).stem
    # Get the unique pcap file name
    if '.' in file_name:
        # 1659009952.170782_0_data.csv -> 1659009952 
        pcap = file_name.split(".")[0]
    elif '(' in file_name:
        # real_fb14 (1).csv -> real_fb14
        pcap = file_name.split(" ")[0]
    else:
        pcap = file_name

    if pcap not in processed_files:
        processed_files[pcap] = []    
    processed_files[pcap].append(full_name)

print(json.dumps(processed_files, indent=2))

fields = ['file', 'session_time', '%tcp_protocol', '%udp_protocol', 
          'ul_data_volume', 'max_ul_volume', 'min_ul_volume', 'avg_ul_volume', 'std_ul_volume', '%ul_volume', 
          'dl_data_volume', 'max_dl_volume', 'min_dl_volume', 'avg_dl_volume', 'std_dl_volume', '%dl_volume',
          'nb_uplink_packet', 'nb_downlink_packet', '%ul_packet', '%dl_packet', 'kB/s', 'nb_packet/s']

FILE_NAME = 0
SESSION_TIME = 1
TCP_PROTO = 2
UDP_PROTO = 3
UL_DATA_VOLUME = 4
MAX_UL_VOLUME = 5
MIN_UL_VOLUME = 6
AVG_UL_VOLUME = 7
STD_UL_VOLUME = 8
UL_VOLUME = 9
DL_DATA_VOLUME = 10
MAX_DL_VOLUME = 11
MIN_DL_VOLUME = 12
AVG_DL_VOLUME = 13
STD_DL_VOLUME = 14
DL_VOLUME = 15
NB_UL_PACKET = 16
NB_DL_PACKET = 17
UL_PACKET = 18
DL_PACKET = 19
KB_PER_S = 20
NB_PACKET_PER_S = 21

UDP_PROTO_ID = '376'
TCP_PROTO_ID = '354'

final_outputs = {}
empty_data_error_files = []
value_error_files = []

for pcap,list_files in processed_files.items():
    rows = {}
    
    for file_name in list_files:
        if pcap not in rows:
            rows[pcap] = pd.DataFrame()
        first_row = pd.read_csv(file_name, nrows=0)
        len_first_row = len(list(first_row)) 
        # Check the first row of each csv file, remove if it doesn't contain any data
        if (len_first_row < 30):
            #print("Remove the first row that doesn't contain any data!")
            try:
                # Only get some important data from the csv file
                df = pd.read_csv(file_name, index_col=None, header = None, skiprows=[0], usecols=[0,3,5,6,12,14,15,17,27,28,29], sep=",")
            except EmptyDataError:
                print(f"No columns to parse from file {file_name}")
                empty_data_error_files.append(file_name)
        else:
            #print("Keep the original file!")
            try:
                # Only get some important data from the csv file
                df = pd.read_csv(file_name, index_col=None, header = None, usecols=[0,3,5,6,12,14,15,17,27,28,29], sep=",") 
            except ValueError:
                print(f"Value error from file {file_name}")
                value_error_files.append(file_name)
        rows[pcap] = pd.concat([df, rows[pcap]])

    #print(rows[pcap])
    data = [0] * len(fields) 
    # Should add dtype='int64' to avoid some warnings
    ul_col = pd.Series(dtype='int64')    # uplink data
    dl_col = pd.Series(dtype='int64')    # downlink data
    proto_col = pd.Series(dtype='int64') # protocol data

    data[FILE_NAME] = pcap
    # Add data of session time
    data[SESSION_TIME] += float(df.iloc[-1,1]) - float(df.iloc[0,1])
    
    # Should use concat() instead of append() to avoid future warnings
    proto_col = pd.concat([proto_col, df.iloc[:,3]], ignore_index=True)
    nb_tcp = 0
    nb_udp = 0
    for i, val in proto_col.items():
        if (val.find(UDP_PROTO_ID) != -1):
            nb_udp += 1
        elif (val.find(TCP_PROTO_ID) != -1):
            nb_tcp += 1    
    # Add data of percentage of TCP/UDP protocol
    data[TCP_PROTO] = nb_tcp * 100 / len(proto_col)
    data[UDP_PROTO] = nb_udp * 100 / len(proto_col)

    # Add data of uplink
    ul_col = pd.concat([ul_col, df.iloc[:,4]], ignore_index=True)
    # Add data of downlink
    dl_col = pd.concat([dl_col, df.iloc[:,6]], ignore_index=True)

    data[NB_UL_PACKET] += df.iloc[:,5].sum()
    data[NB_DL_PACKET] += df.iloc[:,7].sum()

    # Add uplink data
    data[UL_DATA_VOLUME] = ul_col.sum()
    data[MAX_UL_VOLUME] = ul_col.max()
    data[MIN_UL_VOLUME] = ul_col[ul_col != 0].min()
    data[AVG_UL_VOLUME] = ul_col[ul_col != 0].mean()
    data[STD_UL_VOLUME] = ul_col[ul_col != 0].std()
    
    # Add downlink data
    data[DL_DATA_VOLUME] = dl_col.sum()
    data[MAX_DL_VOLUME] = dl_col.max()
    data[MIN_DL_VOLUME] = dl_col[dl_col != 0].min()
    data[AVG_DL_VOLUME] = dl_col[dl_col != 0].mean()
    data[STD_DL_VOLUME] = dl_col[dl_col != 0].std()
    
    # Add data of %ul_volume and %dl_volume
    data[UL_VOLUME] = data[UL_DATA_VOLUME] * 100 / (data[UL_DATA_VOLUME] + data[DL_DATA_VOLUME])
    data[DL_VOLUME] = data[DL_DATA_VOLUME] * 100 / (data[UL_DATA_VOLUME] + data[DL_DATA_VOLUME])
    
    # Add data of %ul_packet and %dl_packet
    data[UL_PACKET] = data[NB_UL_PACKET] * 100 / (data[NB_UL_PACKET] + data[NB_DL_PACKET])
    data[DL_PACKET] = data[NB_DL_PACKET] * 100 / (data[NB_UL_PACKET] + data[NB_DL_PACKET])

    # Add data of kB/s and number_of_packets/s
    if (data[SESSION_TIME] != 0):
        data[KB_PER_S] = (data[UL_DATA_VOLUME] + data[DL_DATA_VOLUME]) / (data[SESSION_TIME] * 1000)
        data[NB_PACKET_PER_S] = (data[NB_UL_PACKET] + data[NB_DL_PACKET]) / data[SESSION_TIME]
    else: # why 0 ?
        print("Session time data is 0 in file " + file_name)

    final_outputs[pcap] = data

print("Empty data error files: " + str(empty_data_error_files))
print("Value error files: " + str(value_error_files))

output_csv = args.output 

# Write all data to the output csv file
with open(output_csv, 'w', encoding='UTF8') as csvfile:
    csvwriter = csv.writer(csvfile ,lineterminator='\n')
    # Write the fields to the 1st row
    csvwriter.writerow(fields)
    # Write all data
    for root,row in final_outputs.items(): 
        csvwriter.writerow(row)
