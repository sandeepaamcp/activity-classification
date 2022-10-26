# Internship project
## Description
This project is for the goal of trying to distinguish different types of online user activities by using machine learning (here, k-means and neural network). For now, the model is still simple; it works for a couple of a source IP address and a destination IP address, and can only separate online activities into 3 categories: the web browsing/file downloading, online video watching, and online communication (such as video call).
The project is written in Python 3.9 and it is recommended to use an IDE that can visualize graphs. The model use CSV reports created from MMT-Probe as input data and after being trained, it can predict which category a new activity belongs to. Before that step, the MMT-Probe takes pcap files as input to produce reports.
Please note that at the time when this project is realized, MMT-Probe and MMT-Operator are recommended to run on Ubuntu. If you do not have a Linux machine, it is recommended to use a virtual Linux machine. More detailed instructions for Ubuntu machine are written below.

## Prerequisites

You need to install Wireshark application, MMT-Probe and MMT-Operator following the links below:

- [Wireshark](https://www.wireshark.org/download.html).
- [MMT-Probe](https://github.com/Montimage/mmt-probe): follow the instruction to install and run in this link.
- [MMT-Operator](https://github.com/Montimage/mmt-operator) (optional): follow the instruction to install and run in this link. Note that it MMT-Operator should be install after MMT-Probe.

## Installation

In order to install and run the project, the following steps should be followed:
1. Cloning the project
2. Preparing the data: 
    - Capture your online activities into pcap files using Wireshark or tcpdump command.
    - Filter the pcaps file using Wireshark, so that there is 1 source IP and 1 destination IP for each pcap file.
    - Use MMT-Probe to produce CSV reports from those pcap files.
    - Save all files for training the model in folder "all_files", while those for testing the model in folder "test_files".
3. Create a csv file containing all data and the features (there are 21 features) (supposing we are in the folder containing all the files):

    ```sh
    python3 ./create_features_csv.py ./all_files/ ./train_file.csv
    python3 ./create_features_csv.py ./test_files/ ./test_file.csv
    ```
4. Run the code for neural network and see the result (I used Spyder IDE in this step).

## Some important notes:
- In mmt-probe.conf found normally in /opt/mmt/probe/mmt-probe.conf, for the parameter "input", the "mode" should be change to "OFFLINE" and "source" should be your path to the pcap file. More instructions on the input and output configuration can be found in the above install link.
- The folder "real_pcap" contains some examples of used pcap files as input for MMT-Probe.
- I use sklearn and keras library for the Kmeans and Neural Network class. For more information:
[Your First Deep Learning Project in Python with Keras Step-by-Step](https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/)
[K-Means Clustering in Python: A Practical Guide – Real Python](https://realpython.com/k-means-clustering-python/)


## Work to do
The model is very simple, and it only works in this specific said model, so there are many ways to improve it to fit your need. Some of the ways are adding more revelent features, adding some real-time control parameters,...