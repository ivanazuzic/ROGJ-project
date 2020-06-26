import pandas as pd
import operator

# Read the dataframe
df = pd.read_csv('statistics.csv')  
# Same values, excluding the values for unrecognised files
df_filtered = df.loc[df['Predicted sentence'] != "unknownvalueerror"]

# WER calculation
#~~~~~~~~~~~~~~~~~~~
print("\n" + "~" * 30) 
print("WER calculation")
print("~" * 30)

#mean cijelog stupca
WER_mean = df["WER from jiwer"].mean()
print("Mean WER:", WER_mean)

# Get rows with maximum WER
print("Maximum WER")
max_WER_rows = df.loc[df['WER from jiwer'].idxmax()]
print("Correct: ", max_WER_rows["Corrected sentence"], " Predicted: ", max_WER_rows["Predicted sentence"])

# Get rows with minimum WER
print("Minimum WER")
min_WER_rows = df.loc[df['WER from jiwer'].idxmin()]
print("Correct: ", min_WER_rows["Corrected sentence"], " Predicted: ", min_WER_rows["Predicted sentence"])

# WER calculation without the unrecognised files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n" + "~" * 30) 
print("WER calculation without the unrecognised files")
print("~" * 30) 
WER_mean = df_filtered["WER from jiwer"].mean()
print("Mean WER:", WER_mean)

# Get rows with maximum WER
print("Maximum WER")
max_WER_rows = df_filtered.loc[df_filtered['WER from jiwer'].idxmax()]
print("Correct: ", max_WER_rows["Corrected sentence"], " Predicted: ", max_WER_rows["Predicted sentence"])

# Get rows with minimum WER
print("Minimum WER")
min_WER_rows = df_filtered.loc[df_filtered['WER from jiwer'].idxmin()]
print("Correct: ", min_WER_rows["Corrected sentence"], " Predicted: ", min_WER_rows["Predicted sentence"])

print("~" * 30) #end of section


# MER calculation
#~~~~~~~~~~~~~~~~~~~
print("\n" + "~" * 30) 
print("MER calculation")
print("~" * 30) 

MER_mean = df["MER from jiwer"].mean()
print("Mean MER:", MER_mean)

# Get rows with maximum WER
print("Maximum MER")
max_MER_rows = df.loc[df["MER from jiwer"].idxmax()]
print("Correct: ", max_MER_rows["Corrected sentence"], " Predicted: ", max_MER_rows["Predicted sentence"])

# Get rows with minimum WER
print("Minimum MER")
min_MER_rows = df.loc[df["MER from jiwer"].idxmin()]
print("Correct: ", min_MER_rows["Corrected sentence"], " Predicted: ", min_MER_rows["Predicted sentence"])


# MER calculation without the unrecognised files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n" + "~" * 30) 
print("MER calculation without the unrecognised files")
print("~" * 30) 
MER_mean = df_filtered["MER from jiwer"].mean()
print("MeanMER:", MER_mean)

# Get rows with maximum WER
print("Maximum MER")
max_MER_rows = df_filtered.loc[df_filtered['MER from jiwer'].idxmax()]
print("Correct: ", max_MER_rows["Corrected sentence"], " Predicted: ", max_MER_rows["Predicted sentence"])

# Get rows with minimum WER
print("Minimum WER")
min_MER_rows = df_filtered.loc[df_filtered['MER from jiwer'].idxmin()]
print("Correct: ", min_MER_rows["Corrected sentence"], " Predicted: ", min_MER_rows["Predicted sentence"])
# TODO: find rows with maximum and minimum MER

print("~" * 30) #end of section


# WIL calculation
#~~~~~~~~~~~~~~~~~~~
print("\n" + "~" * 30) 
print("WIL calculation")
print("~" * 30) 

WIL_mean = df["WIL from jiwer"].mean()
print("Mean WIL:", WIL_mean)


# Get rows with maximum WILL
print("Maximum WIL")
max_WIL_rows = df.loc[df["WIL from jiwer"].idxmax()]
print("Correct: ", max_WIL_rows["Corrected sentence"], " Predicted: ", max_WIL_rows["Predicted sentence"])

# Get rows with minimum WILL
print("Minimum WIL")
min_WIL_rows = df.loc[df["WIL from jiwer"].idxmin()]
print("Correct: ", min_WIL_rows["Corrected sentence"], " Predicted: ", min_WIL_rows["Predicted sentence"])

# WILL calculation without the unrecognised files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("\n" + "~" * 30) 
print("WILL calculation without the unrecognised files")
print("~" * 30) 
WIL_mean = df_filtered["WIL from jiwer"].mean()
print("MeanWIL:", WIL_mean)

# Get rows with maximum WILL
print("Maximum WIL")
max_WIL_rows = df_filtered.loc[df_filtered['WIL from jiwer'].idxmax()]
print("Correct: ", max_WIL_rows["Corrected sentence"], " Predicted: ", max_WIL_rows["Predicted sentence"])

# Get rows with minimum WILL
print("Minimum WIL")
min_WIL_rows = df_filtered.loc[df_filtered['WIL from jiwer'].idxmin()]
print("Correct: ", min_WIL_rows["Corrected sentence"], " Predicted: ", min_WIL_rows["Predicted sentence"])
# TODO: find rows with maximum and minimum WIL

print("~" * 30) #end of section


# Words statistics
#~~~~~~~~~~~~~~~~~~~
with open("affected_words.txt") as f:
    content = f.readlines()

good_words = dict()
swapped_words = dict()
swapped_with = dict()
deleted_words = dict()
inserted_words = dict()
for row in content:
    row_splitted = row.split()
    state = row_splitted[0]
    word = row_splitted[1]
    if state == "good":
        if word not in good_words:
            good_words[word] = 1
        else:
            good_words[word] += 1
    if state == "swap":
        word2 = row_splitted[2]
        if word not in swapped_words:
            swapped_words[word] = 1
            swapped_with[word] = [word2]
        else:
            swapped_words[word] += 1
            swapped_with[word].append(word2)
    if state == "delete":
        if word not in deleted_words:
            deleted_words[word] = 1
        else:
            deleted_words[word] += 1
    if state == "insert":
        if word not in inserted_words:
            inserted_words[word] = 1
        else:
            inserted_words[word] += 1

print("\n" + "~" * 30) 
print("Good")
print("~" * 30)
print("Most common good word:", max(good_words.items(), key=operator.itemgetter(1)))
print("Least common good word:", min(good_words.items(), key=operator.itemgetter(1)))

print("\n" + "~" * 30) 
print("Swapped")
print("~" * 30) 
most_common_swapped = max(swapped_words.items(), key=operator.itemgetter(1))
print("Most common swapped word:", most_common_swapped)
print("Was swapped with", swapped_with[most_common_swapped[0]])
least_common_swapped = min(swapped_words.items(), key=operator.itemgetter(1))
print("Least common swapped word:", least_common_swapped)
print("Was swapped with", swapped_with[least_common_swapped[0]])

print("\n" + "~" * 30) 
print("Deleted")
print("~" * 30) 
print("Most common deleted word:", max(deleted_words.items(), key=operator.itemgetter(1)))
print("Least common deleted word:", min(deleted_words.items(), key=operator.itemgetter(1)))

print("\n" + "~" * 30)
print("Inserted")
print("~" * 30) 
print("Most common inserted word:", max(inserted_words.items(), key=operator.itemgetter(1)))
print("Least common inserted word:", min(inserted_words.items(), key=operator.itemgetter(1)))
