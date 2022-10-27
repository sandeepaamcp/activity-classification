# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 17:22:28 2022

@author: PQV
"""

# importing the csv module
import csv
import pandas as pd
import sys
import os
import glob

# csv file name
if (len(sys.argv) <3):
    path_to_read = "./train_files"    #Insert your path here
    path_to_write = "./"            #Insert your path here
else:
    path_to_read = sys.argv[1]
    file_to_write = sys.argv[2]

csv_files = glob.glob(os.path.join(path_to_read, "*.csv"))
# field names
'''
fields = ['file', 'session_time', 'ul_data_volume', 'nb_uplink_packet', 'dl_data_volume',
          'nb_downlink_packet', 'byte/s', 'nb_packet/s', 'handshake_time', 'app_response_time', 'data_transfer_time' ]
'''
fields = ['file', 'session_time', '%tcp_protocol', '%udp_protocol', 
          'ul_data_volume', 'max_ul_volume', 'min_ul_volume', 'avg_ul_volume', 'std_ul_volume', '%ul_volume', 
          'dl_data_volume', 'max_dl_volume', 'min_dl_volume', 'avg_dl_volume', 'std_dl_volume', '%dl_volume',
          'nb_uplink_packet', 'nb_downlink_packet', '%ul_packet', '%dl_packet', 'kB/s', 'nb_packet/s'] 
          #,'avg_handshake_time', 'avg_app_response_time', 'avg_data_transfer_time' ] 

# data rows of csv file
rows = []

# variables
data_to_add = [0]*len(fields)
data_to_add[0] = '0'
ul_col = pd.Series()    #upload_related date column
dl_col = pd.Series()    #download_related data column
proto_col = pd.Series() #protocol column
add_row = False
rm_1st_row = True


for file_to_read in csv_files:
    '''
    Here, since for each pcap files, the MMT-Probe may produces more than 1 corresponding report, so you have to 
    rename the report so that the code considers them 1 file. For example in this code, facebook (1).csv and 
    facebook(2).csv are considered to be in a same file "facebook", and facebook.1.csv and facebook.2.csv are 
    considered to be in a same file "facebook".
    '''
    
    print(file_to_read, '\n')
    pos_start = file_to_read.rfind('/')
    pos_end = file_to_read.find(' (', pos_start)
    if (pos_end == -1):
        pos_end = file_to_read.find('.', pos_start)
    s = (file_to_read[(pos_start+1): pos_end])

    last_file = (data_to_add[0])

    #When file name contains letters
    if((not s.isnumeric() or not last_file.isnumeric())):
        if (s != last_file and last_file != '0'):
            add_row = True

    #When file name contains only numbers
    else:
        if(int(s) >= int(last_file)+3 and int(last_file) != 0):
            add_row = True
    
    if (add_row):
        
        # %udp, %tcp
        nb_tcp = 0
        nb_udp = 0
        for i, val in proto_col.items():
            if (val.find('376') != -1):
                nb_udp +=1
            elif (val.find('354') != -1):
                nb_tcp +=1
                
        data_to_add[2] = nb_tcp*100/len(proto_col)
        data_to_add[3] = nb_udp*100/len(proto_col)
        
        #uplink data
        data_to_add[4] = ul_col.sum()
        data_to_add[5] = ul_col.max()
        data_to_add[6] = ul_col[ul_col != 0].min()
        data_to_add[7] = ul_col[ul_col != 0].mean()
        data_to_add[8] = ul_col[ul_col != 0].std()
        
        #downlink data
        data_to_add[10] = dl_col.sum()
        data_to_add[11] = dl_col.max()
        data_to_add[12] = dl_col[dl_col != 0].min()
        data_to_add[13] = dl_col[dl_col != 0].mean()
        data_to_add[14] = dl_col[dl_col != 0].std()
        
        #kB/s, nb_packet/s
        data_to_add[20] = (data_to_add[4]+data_to_add[10])/(data_to_add[1]*1000)
        data_to_add[21] = (data_to_add[16]+data_to_add[17])/data_to_add[1]
        
        # %ul volume, %dl volume
        data_to_add[9] = data_to_add[4]*100/(data_to_add[4]+data_to_add[10])
        data_to_add[15] = data_to_add[10]*100/(data_to_add[4]+data_to_add[10])
        
        # %ul packet, %dl packet
        data_to_add[18] = data_to_add[16]*100/(data_to_add[16]+data_to_add[17])
        data_to_add[19] = data_to_add[17]*100/(data_to_add[16]+data_to_add[17])
        
        data_to_add[20] = (data_to_add[4]+data_to_add[10])/(data_to_add[1]*1000)
        data_to_add[21] = (data_to_add[16]+data_to_add[17])/data_to_add[1]
        
        
        rows.append(data_to_add)
        data_to_add = [0]*len(fields)
        ul_col = pd.Series()
        dl_col = pd.Series()
        proto_col = pd.Series()
        
        add_row = False
        rm_1st_row = True
        
    
    #usecols = [timestamp, protocol/appID, Protocol_Path_uplink, UL data volume, UL packet count, DL data volume, DL packet count, handshake_time, app_response_time, data_transfer_time]
    if (rm_1st_row):
        df = pd.read_csv(file_to_read, index_col=None, header = None, skiprows=[0], usecols=[0,3,5,6,12,14,15,17,27,28,29], sep=",")
        rm_1st_row = False
    else:
        df = pd.read_csv(file_to_read, index_col=None, header = None, usecols=[0,3,5,6,12,14,15,17,27,28,29], sep=",")
    df.dropna(axis = 0, inplace = True)
    
    
    data_to_add[0] = s
    #session time
    data_to_add[1] += float(df.iloc[-1,1]) - float(df.iloc[0,1])
    
    #protocol
    proto_col = proto_col.append(df.iloc[:,3])
    
    #upload data
    ul_col = ul_col.append(df.iloc[:,4])  
    
    #download data  
    dl_col = dl_col.append(df.iloc[:,6])    

    data_to_add[16] += df.iloc[:,5].sum()
    data_to_add[17] += df.iloc[:,7].sum()
    
    
    '''
    for i in range(22,25):
        column = df.iloc[:,i-15]
        if column[column != 0].count() != 0:
            data_to_add[i] += column[column != 0].mean()
    '''

##Add last file
# %udp, %tcp
nb_tcp = 0
nb_udp = 0
for i, val in proto_col.items():
    if (val.find('376') != -1):
        nb_udp +=1
    elif (val.find('354') != -1):
        nb_tcp +=1
        
data_to_add[2] = nb_tcp*100/len(proto_col)
data_to_add[3] = nb_udp*100/len(proto_col)

#uplink data
data_to_add[4] = ul_col.sum()
data_to_add[5] = ul_col.max()
data_to_add[6] = ul_col[ul_col != 0].min()
data_to_add[7] = ul_col[ul_col != 0].mean()
data_to_add[8] = ul_col[ul_col != 0].std()

#downlink data
data_to_add[10] = dl_col.sum()
data_to_add[11] = dl_col.max()
data_to_add[12] = dl_col[dl_col != 0].min()
data_to_add[13] = dl_col[dl_col != 0].mean()
data_to_add[14] = dl_col[dl_col != 0].std()

#kB/s, nb_packet/s
data_to_add[20] = (data_to_add[4]+data_to_add[10])/(data_to_add[1]*1000)
data_to_add[21] = (data_to_add[16]+data_to_add[17])/data_to_add[1]

# %ul volume, %dl volume
data_to_add[9] = data_to_add[4]*100/(data_to_add[4]+data_to_add[10])
data_to_add[15] = data_to_add[10]*100/(data_to_add[4]+data_to_add[10])

# %ul packet, %dl packet
data_to_add[18] = data_to_add[16]*100/(data_to_add[16]+data_to_add[17])
data_to_add[19] = data_to_add[17]*100/(data_to_add[16]+data_to_add[17])

#kB/s and nb_Packet/s
data_to_add[20] = (data_to_add[4]+data_to_add[10])/(data_to_add[1]*1000)
data_to_add[21] = (data_to_add[16]+data_to_add[17])/data_to_add[1]

rows.append(data_to_add)        

print ("Number of lines:", len(rows))


 
# writing to csv file
with open(file_to_write, 'w', encoding='UTF8') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile ,lineterminator='\n')
     
    # writing the fields
    csvwriter.writerow(fields)
     
    # writing the data rows
    csvwriter.writerows(rows)