#Load from csv
import csv
import os

def get_professors():
    with open(os.path.join(os.path.dirname(__file__),'csv.csv')) as csvfile:
        creader = csv.reader(csvfile)
        profs=[]
        for row in creader:
            info={}
            info['university']=row[2]
            info['name']=row[0]
            info['email']=row[1]
            profs.append(info)
        return profs[1:]

def main(config):
    return get_professors()