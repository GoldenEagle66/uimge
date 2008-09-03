#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Разработчик: apkawa@gmail.com
Сайт проекта: http://code.google.com/p/uimge/
'''
import optparse
from sys import argv,exit,stderr,stdout
from os import stat
from re import sub,search
from libuimge import imagehost,lang
import inspect
VERSION = '0.06.0.2'

opt_help,error_mes,messages=lang.check()
IMAGEHOSTS = {}
for (name,value) in inspect.getmembers(imagehost):
    if name.startswith('host_'):
        IMAGEHOSTS[name[len('host_'):]]= value

OUTPRINT={
            'default': lambda url, eva: stdout.write('%s\n'%url[0]),
            'bt_bb-thumb':  lambda url, eva: stdout.write('[url=%s][img]%s[/img][/url] ' %(url[0], url[1])),
            'bo_bb-orig':  lambda url, eva: stdout.write('[img]%s[/img]\n' %(url[0])),
            'usr_user-output': lambda url, eva: stdout.write(sub('\\\\n','\n',sub('#TMB#',url[1],sub('#URL#',url[0], eva))))
          }

class input():
    '''Usage:
    > i = input(opt,filename)
    > i.upload()
    '''
    def __init__(self,opt,filenames):
        '''__init__(self,opt, filenames)
        Начальная иницилизация'''
        if opt.filelist:
            self.read_list(opt.filelist)
        else:
            self.filenames = filenames
        self.count= 0
        self.mode = False
        self.name = None
        self.host = opt.check
        self.out = opt.out
        self.out_eval = None
        if not OUTPRINT.has_key(self.out):
            self.out_eval=self.out
            self.out = 'usr_user-output'
    def upload(self):
        '''функция заливки изображений или урлов с изображениями'''
        for file in self.filenames:
            if not self.check(file):
                continue
            send = [file,self.name,self.mode]
            url = IMAGEHOSTS[self.host](send)
            OUTPRINT[self.out](url,self.out_eval)
        stdout.write('\n')
    def read_list(self,filelist):
        self.filenames = []
        f = open(filelist,'r')
        files = f.readlines()
        f.close()
        for file in files: self.filenames.append(sub('\n','',file))
    def check(self,filename):
        if search('^http\:\/\/',filename): self.mode = True
        else: self.mode = False
        if not self.mode:
            try:
                test=stat(filename)
            except OSError:
                stderr.write('Not file\n')
                return False
        return True

def parseopt(arg):
    '''Функциия парсинга опций и вывод справки'''
    usage = opt_help['usage']
    version = 'uimgepy-'+VERSION
    parser = optparse.OptionParser(usage=usage, version=version)
    # Major options
    group_1 = optparse.OptionGroup(parser, opt_help['Major options'])
    for host in IMAGEHOSTS.keys():
        sp = host.split('_')
        group_1.add_option('-'+sp[0],'--'+sp[1],action='store_const', const=host, dest='check', \
                       help=opt_help['--'+sp[1]])
    parser.add_option_group(group_1)
    # Additional options
    group_2 = optparse.OptionGroup(parser, opt_help['Additional options'])
    group_2.add_option('-f','--file', action='store', default=None, dest='filelist', \
                       help=opt_help['--file'])
    parser.add_option_group(group_2)
    group_3 = optparse.OptionGroup(parser, opt_help['Output options'])
    for key in OUTPRINT.keys():
        if key != 'default':
            sp = key.split('_')
            if key != 'usr_user-output':
                group_3.add_option('--'+sp[0],'--'+sp[1], const=key, action='store_const', \
                        default='default', dest='out', help=opt_help['--'+sp[1]])
            else: 
                group_3.add_option('--'+sp[0],'--'+sp[1], action='store_true', \
                        default='default', dest='out', help=opt_help['--'+sp[1]])
    parser.add_option_group(group_3)
    opt, arguments = parser.parse_args(args=arg,)
    if opt.check == None:
        print error_mes['Enter option']
        parser.print_help()
        exit()
    return opt, arguments

if __name__ == '__main__':
    opt, filenames = parseopt(argv[1:])
    inp=input(opt, filenames)
    inp.upload()
