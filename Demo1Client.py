import os

folderName1 = "/home/aditya/Desktop/BE_Project/datafolder/digits/data/ClientImages1"
folderName2 = "/home/aditya/Desktop/BE_Project/datafolder/digits/data/ClientImages2"

scp_var1 = "admin1@192.168.0.13:Desktop/BE_Project/FinalDemo/Demo1Person1"
scp_var2 = "admin1@192.168.0.13:Desktop/BE_Project/FinalDemo/Demo1Person2"

cmd1 = "scp -r " + folderName1 + " " + scp_var1
print "\nCmd1: ",cmd1
os.system(cmd1)

cmd2 = "scp -r " + folderName2 + " " + scp_var2
print "\nCmd2: ",cmd2
os.system(cmd2)
