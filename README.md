# ROGJ-project
Računalna obrada govora i jezika

Before running the upload script make sure you:
1) Pasted the file with your private key and stored the path to it into an environment variable GOOGLE_APPLICATION_CREDENTIALS
export GOOGLE_APPLICATION_CREDENTIALS="ROGJ.json"
2) Have a folder with your wav and txt files and you set the path to them and to the output directory inside the script.
3) Chose the right sampling frequency for your files.


After running te upload script please run the analyse script to get WER, MER and WIL calculated and stored to statistics.csv.

In the end run the final statistics script. 

