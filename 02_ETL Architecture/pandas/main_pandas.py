import requests
import pandas as pd

baseurl = 'http://ec2-54-174-131-205.compute-1.amazonaws.com/API/HDRO_API.php/country_code=ATG,AUS,BGD,BHS,BLZ,BRB,BRN,BWA,CAN,CMR,CYP,DMA,FJI,GBR,GHA,GMB,GRD,GUY,IND,JAM,KEN,KIR,KNA,LCA,LKA,LSO,MDV,MLT,MOZ,MUS,MWI,MYS,NAM,NGA,NRU,NZL,PAK,PNG,RWA,SGP,SLB,SLE,SWZ,SYC,TON,TTO,TUV,TZA,UGA,VCT,VUT,WSM,ZAF,ZMB/indicator_id=103706,183506,175906'

#01 get the data
req = requests.get(baseurl)
data = req.json()

#02 flatten the data inside of a dataframe
data_df_flat = pd.json_normalize(data, max_level=3)

#03 unpivot data frame
data_unpivot = pd.melt(data_df_flat)

#data_unpivot = pd.melt(pd.json_normalize(data, max_level=3))

#04 split variable column by delimiter
data_unpivot[['placeholder','iso3', 'indicator_code', 'year']] = data_unpivot['variable'].str.split('.', expand=True)

#05.a remove unnecessary columns
data_unpivot.pop('variable')
data_unpivot.pop('placeholder')
data_unpivot.pop('indicator_code')
data_unpivot.pop('year')

#05.b rename the remaining columns
data_indicators = data_unpivot.rename(columns={'value': 'indicator_name','iso3': 'indicator_code'})

#06.a get the indicators, located a x-number of rows at the tail of the dataframe
data_indicators = data_indicators.tail(3)
#06.b delete unused dataframes
del data_unpivot,data_df_flat
#07 see how the data looks like printed
#print(type(data_unpivot))
#print(data_indicators)

# Steps 02,03 can be combined: data_unpivot = pd.melt(pd.json_normalize(data, max_level=3))
# Step 07 can be removed, just a check step
