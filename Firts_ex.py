# QUESTION #1#
#
#
#
# Open and read a fasta file
# analyse with regular expressions
# output the following:
"""
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


with open('TAMU_SNP63K_69997.fasta', 'r') as file:  # read the fasta file
    data = file.read().replace('\n', '')
# print(type(data))  # view data type

marker_name = re.findall(r'name=\S{1,50}', data)  # a.Marker name
# print("len marker name: ", len(marker_name))  # to verify that is finds all names
marker_ID = re.findall(r'63K_i\d{5}\w{2}', data)  # b.Marker ID
# print("len marker id: ", len(marker_ID))

marker_alleles_all = re.findall(r's=\w{1}\S\w{1}', data)  # both alleles
# print(len(marker_alleles_all))
# need to separate each allele from the above string
all_marker_len = len(marker_alleles_all)

print("number of different markers = ", all_marker_len)
print("typ: ", type(marker_alleles_all))

# to find  Full marker sequence we should search for :spaceX2, {A,G,C,T, and Y,M,K,R,W,S} and stop at "enter" or "<"

full_marker_seq_raw = re.findall(r'\s\s[A, G, C, T, Y, M, K, R, W, S]*', data)  # Full marker sequence with allele 1
# print(full_marker_seq_raw[0:10])
full_marker_seq_raw_len = len(full_marker_seq_raw)
# print("len: ", full_marker_seq_raw_len)

# Creating a CSV file
download_dir = "Markers_Data.csv"  # where you want the file to be downloaded to
csv = open(download_dir, "w")
columnTitleRow = "Marker_name, Marker_ID, Marker_Allele_1, Marker_Allele_2, Full_marker_sequence_Allele_1, \
 Full_marker_sequence_allele_2,Marker_length, Position_of_SNP\n"
csv.write(columnTitleRow)

flag_more_than_one_snp = [0] * len(marker_alleles_all)


def put_allele(text, allele):  # replace one of [Y, M, K, R, W, S] with the alleles
    for ch in ['Y', 'M', 'K', 'R', 'W', 'S']:
        if ch in text:
            text = text.replace(ch, allele) # replace with one of the alleles
    return text


def find_snp_ind(text):  # return the index of the snp in the marker
    for ch in ['Y', 'M', 'K', 'R', 'W', 'S']:
        snp_ind = text.find(ch)
        if snp_ind != -1:
            break  # check if one of the 'ch' above is inside the string
    return snp_ind
# HAVEN'T FOUND A MARKER WITH MORE THAN ONE WILDCARD CHARACTER


# print(all_marker_len)
for index in range(0, all_marker_len):  # finding the items
    marker_name_current_raw = marker_name[index]
    marker_name_current = marker_name_current_raw[4:]
    marker_ID_current_raw = marker_ID[index]
    marker_ID_current = marker_ID_current_raw[4:]
    Allele = marker_alleles_all[index]
    Allele_1 = Allele[2:3]   # c. Marker allele 1
    Allele_2 = Allele[4:5]   # c. Marker allele 2
    full_marker_seq_single_marker = full_marker_seq_raw[index]
    full_marker_seq = full_marker_seq_single_marker[2:]
    full_marker_seq_allele_1 = put_allele(full_marker_seq, Allele_1)  # e. Full marker sequence with allele 1
    full_marker_seq_allele_2 = put_allele(full_marker_seq, Allele_2)  # f. Full marker sequence with allele 2
    marker_length = len(full_marker_seq_allele_2)  # g. Marker length
    ind_snp = find_snp_ind(full_marker_seq)  # h. Position of SNP in the marker (0-based index)
    # flag the seq with more than one snp:
    ''' if len(str(ind_snp)) > 1:
        flag_more_than_one_snp[index] = 1
    else:
        flag_more_than_one_snp[index] = 0 '''
    row = marker_name_current + "," + marker_ID_current + "," + Allele_1 + "," + Allele_2 + "," + full_marker_seq_allele_1 \
          + "," + full_marker_seq_allele_2 + "," + str(marker_length) + "," + str( ind_snp) + "," + "\n"
    csv.write(row)

# print(flag_more_than_one_snp)

# QUESTION #2#
#
#
''' Use the output of the above script to simplify the fasta - write a script that will read
the output and print two fasta files with full marker sequences, one file for allele 1 and the
other for allele 2. The fasta headers should only include the marker name#
'''
