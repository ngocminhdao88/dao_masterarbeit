import os

if os.path.isdir('tmp'):
    print('folder is there')
else:
    print('folder not there, create it')
    os.mkdir('tmp')
