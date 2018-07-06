import pandas as pd
import operator

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


def add_location(df1,df2):

	li=df1.naptanId.unique()

	for k in range(li.size):
		if(k==0):
			tmp=li[k]
			cond=df2["Naptan_Atco"]==tmp
			df_tmp=df2[cond]
			lat_stop=df_tmp['Location_Northing'].values
			long_stop=df_tmp['Location_Easting'].values

			cond2=df1['naptanId']==tmp
			dff=df1[cond2]
			dff['Latitude']=lat_stop[0]
			dff['Longitude']=long_stop[0]

		else:
			tmp=li[k]
			cond=df2["Naptan_Atco"]==tmp
			df_tmp=df2[cond]
			lat_stop=df_tmp['Location_Northing'].values
			long_stop=df_tmp['Location_Easting'].values

			cond2=df1['naptanId']==tmp
			dff_1=df1[cond2]
			dff_1['Latitude']=lat_stop[0]
			dff_1['Longitude']=long_stop[0]
			dff=dff.append(dff_1)

	return dff



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



def final_format(df):

	li=df.naptanId.unique()	

	for k in li:
		cond=df['naptanId']==k
		df1=df[cond]
		df_new=pd.DataFrame()
		li_2=df1.downloadId.unique()
		for j in li_2:
			dict1={}
			dict2={}
			dict3={}
			cond2=df1['downloadId']==j
			df2=df1[cond2]
			tmstp=str(df2['timestamp'].values).strip('[]')
			lname=str(df2['lineName'].values).strip('[]')
			direc=str(df2['direction'].values).strip('[]')
			row,column=df2.shape
			
			if(row==1):
				li_tmp1=df2[["vehicleId","timeToStation"]].values
				dict1['VehicleId']=li_tmp1[0][0]
				dict1['ETA']=li_tmp1[0][1]
				col=["timestamp","BusStopID","downloadId","ServiceNo","direction","NextBus","NexttoNextBus","NexttoNexttoNextBus"]  ##name of the columns can be changed from here
				df_tmp=pd.DataFrame(columns=col,data=[[tmstp,k,j,lname,direc,dict1,np.nan,np.nan]])
				df_new=df_new.append(df_tmp)

			elif(row==2):
				li_tmp1=df2[["vehicleId","timeToStation"]].values
				dict1['VehicleId']=li_tmp1[0][0]
				dict1['ETA']=li_tmp1[0][1]
				dict2['VehicleId']=li_tmp1[1][0]
				dict2['ETA']=li_tmp1[1][1]
				col=["timestamp","BusStopID","downloadId","ServiceNo","direction","NextBus","NexttoNextBus","NexttoNexttoNextBus"]  ##name of the columns can be changed from here
				df_tmp=pd.DataFrame(columns=col,data=[[tmstp,k,j,lname,direc,dict1,dict2,np.nan]])
				df_new=df_new.append(df_tmp)
			else:
				li_tmp1=df2[["vehicleId","timeToStation"]].values
				dict1['VehicleId']=li_tmp1[0][0]
				dict1['ETA']=li_tmp1[0][1]
				dict2['VehicleId']=li_tmp1[1][0]
				dict2['ETA']=li_tmp1[1][1]
				dict3['VehicleId']=li_tmp1[2][0]
				dict3['ETA']=li_tmp1[2][1]
				col=["timestamp","BusStopID","downloadId","ServiceNo","direction","NextBus","NexttoNextBus","NexttoNexttoNextBus"]  ##name of the columns can be changed from here
				df_tmp=pd.DataFrame(columns=col,data=[[tmstp,k,j,lname,direc,dict1,dict2,dict3]])
				df_new=df_new.append(df_tmp)
	return df_new



filename="new"
df=pd.read_csv(filename+".csv")

df_stops=pd.read_csv("bus-stops.csv")#file which contains the location data of each bus stop

df_1=df[["timestamp","lineName","naptanId","vehicleId","direction","timeToStation"]]

df_new=download_id(df_1)

df2=add_location(df_new,df_stops) #long and lat of each bus stop will be added against each bus stop

cond=df2['direction']=="inbound"
df4=df2[cond]

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
df4=df2[cond]

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

df_int=df5.append(df6)
#intermediate dataframe
#df_int.to_csv("final.csv")

#timestamp,naptanId,downloadId,Latitude,Longitude,Direction
#nextbus-->timeToStation,VehicleId
cond=df_int['direction']=="inbound"
df_11=final_format(df_int[cond])

cond5=df_int['direction']=="outbound"
df_12=final_format(df_int[cond5])

df_final=df_11.append(df_12)

df_new.to_csv("final2.csv")

