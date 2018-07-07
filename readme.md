
**MULTI_DOWNLOADER**

**What it does**:

Downloads a file using a http connection. A file can be downloaded in as many as 6 fragments working asynchronously and at the end merging all of the parts.
The user can select the number of fragments by selecting the number of threads which can be atmost 6.

***Capable of Downloading multiple files concurrently.***  

***Things Used***:

1.Python-tkinter(GUI)

2.Multithreading for asynchronous operations

3.***urrlib2*** for http connections

4.Multiprocessing(PROCESSES) for Downloading various file concurrently

***How to Run***:
Just clone the repo and run the command 

***python Multi_Downloader.py***

A GUI will open 

Enter the url , Select the number of threads , Enter the directory (if you dont do this no problem the file will be saved on the current 
directory) and press the download button.(HERE YOU GO)

For Downloading Multiple Files concurrently just add each url one after the other without waiting for the previous downloads to finish 

***You can also compress the downloaded file***
 
 To do so :
 
 After downloading,the downloaded file will appear under the downloads section , right click on the file and click compress.
 A gzip file of your file would be created .
 
 To unzip use the following command:
 
 gunzip <-filename->
 
 


Hope you like it.

