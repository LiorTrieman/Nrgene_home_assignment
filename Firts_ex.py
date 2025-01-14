# PART 1 - ARRAY DESIGN #
# --------------------- #
"""
# Open and read a fasta file
# analyse with regular expressions
# output the following:

a. Marker name - e.g. USDA_SNP0012
b. Marker ID - e.g. i00001Gh
c. Marker allele 1 - e.g. C
d. Marker allele 2 - e.g. T
e. Full marker sequence with allele 1 - e.g. TGCAGAACACAGA...C...AAGTAAAA
f. Full marker sequence with allele 2 - e.g. TGCAGAACACAGA...T...AAGTAAAA
g. Marker length - e.g. 63
h. Position of SNP in the marker (0-based index) - e.g. 54
"""
import re  # in order to use regular expressions
import numpy as np  # arrange data
import matplotlib.pyplot as plt  # create plots and graphs
from collections import Counter

"""
with open('TAMU_SNP63K_69997.fasta', 'r') as file:  # read the fasta file
    data = file.read().replace('\n', '')
# print(type(data))  # view data type
"""


def read_fasta(fasta_file):
    with open(fasta_file, 'r') as file:  # read the fasta file
        data = file.read().replace('\n', '')
    return data
    # print(type(data))  # view data type


def put_allele(text, allele):  # replace one of [Y, M, K, R, W, S] with the alleles
    for ch in ['Y', 'M', 'K', 'R', 'W', 'S']:
        if ch in text:
            text = text.replace(ch, allele)  # replace with one of the alleles
    return text


def find_snp_ind(text):  # return the index of the snp in the marker
    for ch in ['Y', 'M', 'K', 'R', 'W', 'S']:
        snp_ind = text.find(ch)
        if snp_ind != -1:
            break  # check if one of the 'ch' above is inside the string
    return snp_ind


def cut_head_of_snp_string(raw_SNP):  # get only the snp from the raw string
    snp = raw_SNP[2:]
    return snp


def auto_label(rects):  # Attach a text label above each bar
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def cut_head_of_marker_seq_string(raw_str):  # get list of lengths from raw string
    length = raw_str[2:]
    return length

#   QUESTIONS 1 - CREATE A CSV FILE FROM EXTRACTED DATA  #
# ------------------------------------------------------ #


if __name__ == "__main__":
    data = read_fasta('TAMU_SNP63K_69997.fasta')
    marker_name = re.findall(r'name=\S{1,50}', data)  # a.Marker name
    # print("len marker name: ", len(marker_name))  # to verify that is finds all names
    marker_ID = re.findall(r'63K_i\d{5}\w{2}', data)  # b.Marker ID
    # print("len marker id: ", len(marker_ID))

    marker_alleles_all = re.findall(r's=\w{1}\S\w{1}', data)  # both alleles
    # print(len(marker_alleles_all))
    # need to separate each allele from the above string
    all_marker_len = len(marker_alleles_all)
    # to find  Full marker sequence we should search for :spaceX2, {A,G,C,T, and Y,M,K,R,W,S} and stop at "enter" or "<"

    full_marker_seq_raw = re.findall(r'\s\s[A, G, C, T, Y, M, K, R, W, S]*', data)  # Full marker sequence with allele 1
    # print(full_marker_seq_raw[0:10])
    full_marker_seq_raw_len = len(full_marker_seq_raw)

    # Creating a CSV file
    download_dir = "Markers_Data.csv"  # where you want the file to be downloaded to
    csv = open(download_dir, "w")
    columnTitleRow = "Marker_name, Marker_ID, Marker_Allele_1, Marker_Allele_2, Full_marker_sequence_Allele_1, \
     Full_marker_sequence_allele_2,Marker_length, Position_of_SNP\n"
    csv.write(columnTitleRow)

    # HAVEN'T FOUND A MARKER WITH MORE THAN ONE WILDCARD CHARACTER

    for index in range(0, all_marker_len):  # finding the items
        marker_name_current_raw = marker_name[index]
        marker_name_current = marker_name_current_raw[5:]  # cut relevant part of the string
        marker_ID_current_raw = marker_ID[index]
        marker_ID_current = marker_ID_current_raw[4:]  # cut relevant part of the string
        Allele = marker_alleles_all[index]
        Allele_1 = Allele[2:3]   # c. Marker allele 1
        Allele_2 = Allele[4:5]   # d. Marker allele 2
        full_marker_seq_single_marker = full_marker_seq_raw[index]
        full_marker_seq = full_marker_seq_single_marker[2:]  # cut relevant part of the string
        full_marker_seq_allele_1 = put_allele(full_marker_seq, Allele_1)  # e. Full marker sequence with allele 1
        full_marker_seq_allele_2 = put_allele(full_marker_seq, Allele_2)  # f. Full marker sequence with allele 2
        marker_length = len(full_marker_seq_allele_2)  # g. Marker length
        ind_snp = find_snp_ind(full_marker_seq)  # h. Position of SNP in the marker (0-based index)
        row = marker_name_current + "," + marker_ID_current + "," + Allele_1 + "," + Allele_2 + "," +\
            full_marker_seq_allele_1 + "," + full_marker_seq_allele_2 + "," + str(marker_length) + "," \
            + str(ind_snp) + "," + "\n"
        csv.write(row)  # adding a raw to file each 'for' iteration

    #  QUESTIONS 2 - CREATE 2 FASTA FILE ONE FOR EACH ALLELES  #
    # -------------------------------------------------------- #

    """ Use the output of the above script to simplify the fasta - write a script that will read
    the output and print two fasta files with full marker sequences, one file for allele 1 and the
    other for allele 2. The fasta headers should only include the marker name#
    # first create a list of marker_names and a list of marker_seq for each allele
    # create a dict from these two lists
    # write then into fasta file """
    list_name = []

    for index in range(0, all_marker_len):  # finding the items
        marker_name_current_raw = marker_name[index]
        marker_name_current = marker_name_current_raw[5:]
        list_name.append(marker_name_current)

    o_file = open("fasta_allele_1.fasta", "w")
    o_file.write(">")  # write a title of names
    for index in range(len(list_name)):
        o_file.write(list_name[index] + " ")

    for index in range(len(list_name)):
        Allele = marker_alleles_all[index]
        Allele_1 = Allele[2:3]  # c. Marker allele 1
        full_marker_seq_single_marker = full_marker_seq_raw[index]
        full_marker_seq = full_marker_seq_single_marker[2:]
        full_marker_seq_allele_1 = put_allele(full_marker_seq, Allele_1)  # e. Full marker sequence with allele 1
        o_file.write(">" + full_marker_seq_allele_1 + "\n")
    o_file.close()
    o_file = open("fasta_allele_2.fasta", "w")
    # write a title of names:
    o_file.write(">")
    for index in range(len(list_name)):
        o_file.write(list_name[index] + " ")

    for index in range(len(list_name)):
        Allele = marker_alleles_all[index]
        Allele_2 = Allele[4:5]  # d. Marker allele 2
        full_marker_seq_single_marker = full_marker_seq_raw[index]
        full_marker_seq = full_marker_seq_single_marker[2:]
        full_marker_seq_allele_2 = put_allele(full_marker_seq, Allele_2)  # f. Full marker sequence with allele 2
        o_file.write(">" + full_marker_seq_allele_2 + "\n")
    o_file.close()

    # QUESTIONS 3 - PLOTTING THE DATA #
    # -------------------------------- #

    # Bar Chart for Frequencies of SNP types (C/T, C/G. C/A, A/T, A/G, G/T)
    # marker_alleles_all -raw list of all SNP types, need to extract freqs
    num_total_snp = len(marker_alleles_all)
    list_of_snp = []

    for index in range(0, num_total_snp):  # get the list of all snp
        snp_type = cut_head_of_snp_string(marker_alleles_all[index])
        list_of_snp.append(snp_type)

    snp_freqs = []
    snp_objects = Counter(list_of_snp).keys()  # equals to list(set(words))
    snp_counts = Counter(list_of_snp).values()  # counts the elements' appearances
    print(snp_objects)
    print(snp_counts)
    for index in snp_counts:
        freq = index/num_total_snp
        snp_freqs.append(freq)
    y_pos = np.arange(len(snp_objects))
    plt.figure(1)  # new figure
    plt.bar(y_pos, snp_freqs, align='center', alpha=0.5)
    plt.xticks(y_pos, snp_objects)
    plt.ylabel('Frequencies')
    plt.title('Frequencies of SNP types')
    x = np.arange(len(snp_objects))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, snp_counts, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Count of SNP')
    ax.set_title('Total count of SNP types')
    ax.set_xticks(x)
    ax.set_xticklabels(snp_objects)
    auto_label(rects1)
    fig.tight_layout()
    plt.show()

    # Marker length - Histogram
    list_of_marker_length = []

    for index in range(0, num_total_snp):
        marker_str = cut_head_of_marker_seq_string(full_marker_seq_raw[index])
        marker_len = len(marker_str)
        list_of_marker_length.append(marker_len)

    ind_snp_list = []
    norm_snp_list = []
    max_len = 0  # finding the max len of the all markers
    count_zero = 0
    for index in range(0, all_marker_len):  # finding the items
        full_marker_seq_single_marker = full_marker_seq_raw[index]
        full_marker_seq = full_marker_seq_single_marker[2:]  # cut relevant part of the string
        ind_snp = find_snp_ind(full_marker_seq)  # h. Position of SNP in the marker (0-based index)
        ind_snp_list.append(ind_snp)
        if len(full_marker_seq) > max_len:
            max_len = len(full_marker_seq)  # update the maximum
        if len(full_marker_seq) > 0:
            norm_snp_list.append(ind_snp/int(len(full_marker_seq)))
        if len(full_marker_seq) == 0:
            count_zero += 1  # FOUND 8 GENE WITH SEQ LEN == ZERO - SHOULD BE CHECKED
    plt.figure(2)
    plt.hist(list_of_marker_length, range=(0, max_len), density=False, histtype='bar', align='mid', orientation='vertical')
    plt.ylabel('Marker Lengths counts')
    plt.xlabel('Marker Lengths (number of Nucleotide)')
    plt.title('Marker Lengths Histogram')
    plt.show()
    ''' bins=None, , density=None, weights=None, cumulative=False,\
                           bottom=None, , rwidth=None, log=False, color=None, label=None,\
                           stacked=False, normed=None, *, data=None, **kwargs)'''
    fig, axs = plt.subplots(2)
    axs[0].hist(ind_snp_list, bins=20, range=[0, max_len])  # xmax should be longest marker seq
    axs[0].set_title('SNP location Histogram')
    axs[1].hist(norm_snp_list, bins=20, range=[0, 1])
    axs[1].set_title('NP normalized location Histogram')
    plt.show()



