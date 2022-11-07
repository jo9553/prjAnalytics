import boto3
import urllib3
from datetime import date
import pandas as pd
from pandas import DataFrame
import awswrangler as wr

today = date.today().strftime("%y%m%d")

s3Client = boto3.client('s3')
s3Resource = boto3.resource('s3')

inputDate = today
# inputDate = '221104'
cat = 'hsio'
zipfilename = '{0}/{1}{2}.zip'.format(cat,cat,inputDate)
csvfilename = '{0}/{1}{2}.csv'.format(cat,cat,inputDate)
s3Bucket = "<change it to your own bucket name"

http = urllib3.PoolManager()
url = 'https://www.hkex.com.hk/eng/stat/dmstat/dayrpt/{0}{1}.zip'.format(cat, inputDate)

def getURL(purl):
    response = pd.read_csv(url, compression='zip', sep="\t", engine='python', header=0, error_bad_lines=False)
    return response

def lambda_handler(event, context):
    response = getURL(url) #DataFrame'
    startfrom = response.index[response['HANG SENG INDEX OPTIONS DAILY MARKET REPORT (Final)']==',,,"After-Hours Trading Session",,,,,,,,"Day Trading Session",,,,,,"Combined"'].tolist()
    response.drop(response.index[:startfrom[0]],inplace=True)
    response.drop(response.tail(14).index, inplace=True)
    response2 = response['HANG SENG INDEX OPTIONS DAILY MARKET REPORT (Final)'].str.split(",", expand=True)
    response2.columns = ['contract_month','strike_price','call/put','1opening_price','1daily_high','1daily_low',
                '1close_price','1volume','2opening_price','2daily_high','2daily_low','2oqp_close','2oqp_change','2iv','2volume','contract_high','contract_low','combined_volume','open_interest','change_in_OI']
    response2.drop(response2[response2['contract_month'] == ''].index)
    response2.dropna(how='all')
    
    d = {'dataDate':inputDate} #convert inputDate to dictionary
    df = pd.DataFrame(data=d, index=['dataDate']) #convert dictionary to DataFrame
    response2["dataDate"] = df['dataDate'].dataDate #add DataFrame to response2
    
    wr.s3.to_csv(
        df=pd.DataFrame(response2),
        path='s3://'+s3Bucket+'/'+csvfilename,
    )
