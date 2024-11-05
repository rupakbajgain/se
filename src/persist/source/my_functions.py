import os
import json
import logging
import configparser

config = configparser.ConfigParser()
config.read('assets/configs/config.ini')

def _args_to_filepath(name, *args, **kwargs):
    if len(args):
        argss=''
        for i in args:
            argss+=str(i)+','
        argss=argss[:-1]
        name+='('+argss+')'
    if len(kwargs):
        kwargss = ''
        for i in kwargs:
            kwargss+=str(i)+'-'+str(kwargs[i])+','
        kwargss=kwargss[:-1]
        name+='{'+kwargss+'}'
    file_path = os.path.join(config['directories']['PERSIST_PATH'], f"{name}")
    return file_path

def persist_helper(name, func, *args, **kwargs):
    file_path = _args_to_filepath(name, *args, **kwargs)
    logging.debug(f"Variable requested: {name}")
    if os.path.exists(file_path):
        logging.debug(f"Found on file: {file_path}")
        dbfile = open(file_path, 'r')
        db = json.load(dbfile)
        dbfile.close()
        return db
    else:
        logging.debug(f"Cache to new file: {file_path}")
        db=func(*args, **kwargs)
        dbfile = open(file_path, 'w')
        json.dump(db, dbfile, indent=2)
        dbfile.close()
        return db

def persist(p):
    def inner(func):
        def actual_function(*args, **kwargs):
            return persist_helper(p, func, *args, **kwargs)
        return actual_function
    return inner

def clear_persist(name):
    def c(*args, **kwargs):
        file_path = _args_to_filepath(name, *args, **kwargs)
        os.remove(file_path)
        return True
    return c