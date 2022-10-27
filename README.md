# User Network Activities Classification and XAI
## Description
This project aims to characterise user network activities using supervised machine learning techniques (KMeans, Keras Neural Network),
while traditional approaches based on Deep Packet Inspection (DPI) may have difficulties for distinguishing different online user activities.
Currently, we consider the most 3 common user activities:

- Activity 1: Web browsing / File downloading
- Activity 2: Interactive (such as video call, chatting app)
- Activity 3: Video playback (Youtube)

The model use CSV reports created from MMT-Probe as input data and after being trained, it can predict which category a new activity belongs to. 
Before that step, the MMT-Probe takes pcap files as input to produce reports.

Some slides of T5.4 of SPATIAL project: https://docs.google.com/presentation/d/13SsfhJyGGETRJsiydxo4U3QKMa1hMYrUWmpWSaXJALY/edit?usp=sharing

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
3. Create a csv file containing all data and the features (there are 21 features):
    ```sh
    $ python3 parse_csv.py -i train_files -o output_train.csv
    $ python3 parse_csv.py -i test_files -o output_test.csv
    ```
Then, we need to label the training/testing data by adding a column 'output', for example 1, 2 or 3.

4. Run the code for neural network and see the result (I used Spyder IDE in this step).

## Some important notes:
- In mmt-probe.conf found normally in /opt/mmt/probe/mmt-probe.conf, for the parameter "input", the "mode" should be change to "OFFLINE" and "source" should be your path to the pcap file. More instructions on the input and output configuration can be found in the above install link.
- The folder "real_pcap" contains some examples of used pcap files as input for MMT-Probe.
- I use sklearn and keras library for the Kmeans and Neural Network class. For more information:
[Your First Deep Learning Project in Python with Keras Step-by-Step](https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/)
[K-Means Clustering in Python: A Practical Guide – Real Python](https://realpython.com/k-means-clustering-python/)


## [MD] TO TRY
- Fix create_features_csv.py to convert pcap files into csv files
- Add more features / real-time control parameters (currently 24 features and 3 features are useless - without data)
- Try different AI models: XGBoost, LightGBM, ...
- Integrate XAI methods, such as SHAP, LIME
- Reproduce and add more datasets? more activities ?
- Use the 5G testbed for 5G mobile user activities classification ???