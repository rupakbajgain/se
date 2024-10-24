import os
#from ..page import start_browser
import json
from multiprocessing import Pool
import time
from ..automail import automail

def do_work(p):
    s=time.time()
    id=p[0]
    prof=p[1]
    print('Starting : ', prof['name'])
    #start_browser()#i dont know how process works to be sure here
    if not automail(prof):
        print(prof['name'], "No info found to send mail")
    with open('./persist/counter','a') as f:
        f.write(f"{id}\n")
    e=time.time()
    print('Done : ', prof['name'], "(%.2f) s"%(e-s))

def main(config):
    print('Current user : ', config['basic']['user'])
    if not os.path.isfile('./persist/current') or not os.path.isfile('./persist/current'):
        print("Select uni first")
        return
    with open('./persist/current','r') as f:
        uni_code = f.read()
    print('Selected Uni : ', uni_code)
    #config.write(sys.stdout)
    with open('./persist/counter','r') as f:
        done_counter = []
        for i in f.readlines():
            done_counter.append(int(i))
    #print(done_counter)
    with open(f'./persist/profs({uni_code})','r') as f:
        all_profs = json.load(f)
    todo_ids = []
    for i in range(len(all_profs)):
        if not i in done_counter:
            todo_ids.append([i, all_profs[i]])
    pool_size = 4
    print('Pool size : ', pool_size)
    p = Pool(pool_size)
    p.map(do_work, todo_ids)
    #do_work(todo_ids[0])
