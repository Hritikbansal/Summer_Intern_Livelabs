import pandas as pd
import matplotlib.pyplot as plt 
import operator
import numpy as np

def bus_seq(df_tmp):
	row,column=df_tmp.shape
	if(row==1):
		df_tmp['busSeq']="nextbus"
	elif(row==2):
		idx=column
		df_tmp.insert(loc=idx,column='busSeq',value=["nextbus","subseqbus"])
	else:
		idx=column
		df_tmp=df_tmp.iloc[0:3]
		df_tmp.insert(loc=idx,column='busSeq',value=["nextbus","subseqbus","nextsubseqbus"])

	return df_tmp

def download_id(df_new):
	tmp_nparr=df_new.timestamp.unique()

	for k in range(tmp_nparr.size):
		if(k==0):
			cond1=df_new['timestamp']==tmp_nparr[0]
			df_tmp=df_new[cond1]
			df_tmp2=df_tmp
			df_tmp2['downloadId']=0
		else:
			cond1=df_new['timestamp']==tmp_nparr[k]
			df_tmp=df_new[cond1]
			df_tmp3=df_tmp
			df_tmp3['downloadId']=k
			df_tmp2=df_tmp2.append(df_tmp3)

	return(df_tmp2)

def req_format(df_tmp):
	df_tmp2=df_tmp.sort_values(by='timeToStation')
	#numpy array which contains all the unique values of the 
	arr=df_tmp2.naptanId.unique()
	#print(df2.naptanId.unique())
	#print(arr.size)
	for i in range(arr.size):
		if(i==0):
			cond4=df_tmp2['naptanId']==arr[0]
			df_tmp3=df_tmp2[cond4]
			df_tmp3=bus_seq(df_tmp3)
		else:
			cond4=df_tmp2['naptanId']==arr[i]
			df_tmp4=df_tmp2[cond4]
			df_tmp4=bus_seq(df_tmp4)
			df_tmp3=df_tmp3.append(df_tmp4)

	return df_tmp3	

#load csv with filename
#filename contains the data for each route 
filename="new"
df=pd.read_csv(filename+".csv")#---------------------------------------->Change the filename as per requirement

df2=df[["timestamp","lineName","naptanId","vehicleId","direction","timeToStation"]]
#direction--> the vehicle is inbound or outbound
#using inbound for this analysis
cond=df2['direction']=="inbound"
df3=df2[cond]

#adding a new column of download_id to the data
df4=download_id(df3)
#print(df4)

li=df4.downloadId.unique()

for j in range(li.size):
	if(j==0):
		cond2=df4["downloadId"]==li[0]
		df_tmp=df4[cond2]
		df5=req_format(df_tmp)	
	else:
		cond3=df4["downloadId"]==li[j]
		df_tmp=df4[cond3]
		df6=req_format(df_tmp)
		df5=df5.append(df6)

#df5.to_csv("final.csv")
#print(df5)

cond=df2['direction']=="outbound"
df3=df2[cond]

#adding a new column of download_id to the data
df4=download_id(df3)
#print(df4)

li=df4.downloadId.unique()

for j in range(li.size):
	if(j==0):
		cond2=df4["downloadId"]==li[0]
		df_tmp=df4[cond2]
		df6=req_format(df_tmp)	
	else:
		cond3=df4["downloadId"]==li[j]
		df_tmp=df4[cond3]
		df7=req_format(df_tmp)
		df6=df6.append(df7)

df_final=df5.append(df6)

df_final.to_csv("final.csv")