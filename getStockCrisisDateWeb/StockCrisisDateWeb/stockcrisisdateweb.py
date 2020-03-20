#!/usr/bin/python
# -*- coding: utf-8 -*-
#import cgi
#import cgitb; cgitb.enable()

#form = cgi.FieldStorage()

import pandas as pd
import html5lib
import lxml
#import h5py
#import tables
from pandas import HDFStore, DataFrame
#from dynamodb import putItems
#import boto3
#import botocore
#import click
#import pytz
#import tables

#utc = pytz.utc

myl = None
Data1 = None


def readHTML():
    """Read the list of stock market crashes information"""
    global Data1, myl

    lsmc = pd.read_html('https://en.wikipedia.org/wiki/List_of_stock_market_crashes_and_bear_markets')
    Data1 = lsmc[0]

    #type(Data1)
    #Data1.columns

    # convert columns to type string
    for i in Data1.columns:
        Data1[i] = Data1[i].astype(str)
    print(Data1)

    Data1['Year'] = pd.to_datetime(Data1['Date'], errors='coerce').dt.year
    Data1 = Data1.fillna(0)
    Data1['Year'] = Data1['Year'].astype('int32')
    print(Data1.columns)
    print(Data1)

    myl = Data1.T.to_dict().values()


def writeHD5():
    """Write to local store.h5"""
    global Data1

    store = HDFStore('.\store.h5')
    store['listCrisis'] = Data1
    store.close()


if __name__ == '__main__':
    readHTML()
    writeHD5()
#    cli()
