#!./env/bin/python3
import os,sys
import shutil
import click
from click_default_group import DefaultGroup
import json
from src.persist import persist
from src.config import getConfig
import time

def exec_program(user=None):
    s=time.time()
    from src.se.main import main
    config = getConfig()
    if not user:#extend with user info
        user=config['basic']['DEFAULT_USER']
    config.set('basic','USER',user)
    config.read(f'assets/configs/{user}.ini')
    main(config)
    e=time.time()
    print("Total : %.2f s"%(e-s))

@click.group(cls=DefaultGroup,
             default='run',
             default_if_no_args=True,
             help="Program to send automated mail.")
def cli():
    pass

@cli.command(help='Run the main program(default)')
@click.option('--user', required=False, help='which ini to use')
def run(user):
    exec_program(user)

@cli.command(help='Server')
@click.option('--debug', '-d', is_flag=True, help="Is debug")
def web(debug=False):
    from src.flask import main
    if hasattr(main,'main'):
        main.main(debug)

@cli.command(help='Cleanup and init')
def clean():
    config = getConfig()

    if os.path.exists(config['directories']['DOWNLOAD_PATH']):
        shutil.rmtree(config['directories']['DOWNLOAD_PATH'])
    os.mkdir(config['directories']['DOWNLOAD_PATH'])

    if os.path.exists(config['directories']['PERSIST_PATH']):
        shutil.rmtree(config['directories']['PERSIST_PATH'])
    os.mkdir(config['directories']['PERSIST_PATH'])

@cli.command(help='Run the tests')
@click.argument('lib', default=None,required=False)
def test(lib):
    p = './src'
    if lib:
        p+='/'+lib
    os.system('pytest '+p)

@cli.command(help='Create empty lib')
@click.argument('name',required=True,type=str)
def createlib(name):
    if name:
        shutil.copytree('./assets/emptylib', './src/'+name)

@cli.command(help='List universities')
def listuni():
    from src.lsdict import list_dict,get_info
    from tabulate import tabulate
    nl=[]
    for i in list_dict('./scripts/uni'):
        nl.append([i[0], get_info(i[1])])
    print(tabulate(nl,headers=["Code","Name"]))

def load_uni(name):
    config = getConfig()
    from src.lsdict import get_main
    modmain = get_main(f"./scripts/uni/{name}.py")
    return modmain(config)

@persist('profs')
def load_uni_cached(name):
    return load_uni(name)

@cli.command(help='List professors from uni')
@click.argument('name',required=True,type=str)
@click.option('--nosave', '-ns', is_flag=True, help="No Cache result")
def listprofs(name,nosave):
    if nosave:
        r=load_uni(name)
    else:
        r=load_uni_cached(name)
    with open('./persist/counter','w') as f:
        pass#create empty file
    with open('./persist/current','w') as f:
        f.write(name)#create empty file
    for i in r:
        print(json.dumps(i))

@cli.command(help='Search for prof in scholar')
def scholar():
    config = getConfig()
    from src.scholar import get_prof_datas
    prof = json.load(sys.stdin)
    r = get_prof_datas(prof)
    for i in r:
        print(json.dumps(i))

@cli.command(help='Crawl link page for prof')
def crawl():
    config = getConfig()
    from src.crawler import crawl_info
    prof = json.load(sys.stdin)
    r = crawl_info(prof)
    for i in r:
        print(json.dumps(i))

@cli.command(help='Both crawl and scholar')
def crawlscholar():
    config = getConfig()
    from src.crawler import crawl_info
    prof = json.load(sys.stdin)
    r = crawl_info(prof)
    for i in r:
        print(json.dumps(i))
    from src.scholar import get_prof_datas
    r = get_prof_datas(prof)
    for i in r:
        print(json.dumps(i))

@cli.command(help='Links to doc string')
def todocs():
    config = getConfig()
    from src.loaddocs import get_documents, docs_to_text
    #prof = json.load(sys.stdin) , missing
    l=[]
    for line in sys.stdin:
        d=json.loads(line)
        l.append(d)
    d = get_documents(l)
    t = docs_to_text(d)
    print(t)

@cli.command(help='Automacally does all steps up to email from prof_info')
def automail():
    config = getConfig()
    from src.automail import automail
    prof = json.load(sys.stdin)
    r = automail(prof)
    if r:
        print("Email done sucessfully")

if __name__=='__main__':
    cli()
