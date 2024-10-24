import os

def get_info(fp):
    "Get 1st # from file , skip #!"
    def fix_line(s):
        return s.split('\n')[0]

    with open(fp,'r') as f:
        head=f.read(1000)
    head = head.split('#')
    if len(head)<1:
        return ''
    if head[1][0]=='!':#skip
        return fix_line(head[2])
    else:
        return fix_line(head[1])

def list_dict(ds,detailed=False,ext='.py'):
    """Get list of all files without extensions(with py)
    If detailed get 1st line of header too"""
    ext=ext.lower()
    l=[]
    for file in os.listdir(ds):
        file_name,file_ext = os.path.splitext(os.path.split(file)[-1])
        if file_ext.lower() == ext:
            fp = os.path.join(os.path.abspath(ds), file)
            l.append([file_name, fp])
    return l

def get_main(fp,module_name ='loadedex'):
    import importlib.util
    spec = importlib.util.spec_from_file_location(module_name, fp)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main