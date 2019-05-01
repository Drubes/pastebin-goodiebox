#!/usr/bin/python
# -*- coding: utf-8 -*-

'''''''''''''''''''''''''''''''' ' ' ' '''''''''''''''''''''''''''''''''''''''''

░▓▓▓▓▓▓▒▓░▒░░
░████████████▓                   ░░          ░▒▓▓█▓▒░
▒▓▓▒     ▒▓███░                  ▒▓▒       ░▒████████▓░
█▓        ░███░      ░       ░░  ░██░     ░██░     ░▒▓█░     ░▓▓░      ░▒░
█▓        ▓█▓░      █░       ▒▒   ▓█░     ▒██▒       ░▓▒  ░▓████░     ▒███░
▒█▓▒     ▓▓▓      ░██▒  ░░   ▒▓   ▒█▒      ░░█▓░       ░  ▓████░    ░█████▓░
 ▓██▓░▓███▓▒    ░▓████░ ▒▒   ▒█▒  ▒█▓        ▒████▓░     ░██▒      ░███▒ ░▓▒
 ░██▒░▓████▓▓▒ ▒███▒▒█▓ ▒█░  ░▓█▒ ░██░         ▒▒▓██▓░   ▓██       ▓█▓    ░░
  ██░   ░████  ██▒   ▓█░░█▓   ░▓█░ ▒█▓            ░▒██▒  ▒█████▒   ██░
  █▓     ▓██░░▓███▓▒▒▓█▒ ▒█░   ░█▓ ░▓█▓░            ░▓█▒  ░███▓░   ██░
  █░     ██▒ ░█████████▒ ░██░   ▒█░ ░███▓░    ░██    ░▒█   ▒██     ▒█▓       ░░
  █░    ▓██▒ ░██  ░▒███▒  ▓█▒   ░██░ ▓███▒    ▓ ▒░     ▓▓░ ░██      ▒██▓░    ▓▓
  █▓   ░███   █░    ░▓▓░░░▓█░    ░██░ ░███░  ░█        ░█▓  ██░      ▒████▓▒░██
  █▓   ██▓    ▒      ░░ ▒▓█▓      ░█▓  ▓██▒░ ▓█░       ░█▓  ███░  ▒█  ░▓███████
  █▒  ██▓     ░       ░▓██▓░       ▒█░  ▒██▓  ██▓░   ░▒█▒   ▒███████░    ░▒▓██▒
  █▓▒▓▓▒            ░▒██▓░   ░▒░   ░██░  ▓█▓  ░████████░     ░▓███▓▒
  ██▓▒              ▒█▓      ▒█▓    ░██░  ▓░    ░▒▓█▓▒░
  ░░                ▓█░      ▒██▒    ▒██░                              ░█▓ ▒▓░
                    ██▒     ▒████▓    ▓█▒     ▒▓▓███▓███████████▒▒▒░░  ▒██ ▓█▒
                    ▓██▒   ▒██▓░▓█▒ ░▓▓█▒    ░▓▓▓███████████▓███████▓▒ ░▓▒ ░▒░
                    ░██▓▓▓████▒▒▒██████▓░
                     ░▒█████░░   ░░░░░░
                       ░▒░

'''''''''''''''''''''''''''''''' ' ' ' '''''''''''''''''''''''''''''''''''''''''
# Known issues / todo:
#------------------------
# '::' is a false positves on ipv6
# 'dd.mm.yy' and 'dd.mm.yyyy' formated dates are a fasle positive on EU phonenumber.
# numbers with a shitload of '0' are a fasle positve on bitcoin addresses

################################################################################
#IMPORT.
import requests
import re
import string
import sys
from time import sleep

################################################################################
#CONFIG
do_scrape = 1                    # troggle scraping on/off
do_save = 1                      # save paste to folder
do_printself    = 1                 # show this file at start.
output_file     ="/home/m42d/pastes/goodies"           # path to save scrape results to.
save_path       = '/home/m42d/pastes/' # path to save pastes to
que_file        = '/home/m42d/pastes/que'                 # path to save que to.
scraped_file    = '/home/m42d/pastes/scraped'         # path to save scraped id's to.
        # only saves if paste expires and regex or triggerword matches
        # unless save_tw or save_rx is matched than it wil save even
        # if if the past never expires.


# trigger words..
# case insensitive.
tw = ['password','pass','user','admin','login','dox','BEGIN RSA PRIVATE KEY','Private-MAC','<RSAKeyValue>','bitcoin','#EXTINF']
save_tw = ['#EXTINF'] # trigger words to save to save even if the pastebin doen't expire.

# name of the keys of the regexp to save even if the pastebin doen't expire.
save_rx = ['Bitcoin private key']
#Regex magic.,
rx = {'uri':'^(?i)([a-z]{1,6}:\/\/)[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,5}(:[0-9]{1,5})?(\/.*)?',\
      'email':'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',\
      'EU phonenr':'(((\+[0-9]{2,3})|(00[0-9]{2,3}))\s)?(((((\(0\))|0){1})?[0-9]{1,3}\/)|([0-9]{1,2}\.[0-9]{2}\.))?[0-9]{2}\.[0-9]{2}\.[0-9]{2}(\.[0-9]{2})?',\
      'ipv4 addr':'(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))',\
      'ipv6 addr':'(?:[a-f0-9]{1,4}:){6}(?::[a-f0-9]{1,4})|(?:[a-f0-9]{1,4}:){5}(?::[a-f0-9]{1,4}){1,2}|(?:[a-f0-9]{1,4}:){4}(?::[a-f0-9]{1,4}){1,3}|(?:[a-f0-9]{1,4}:){3}(?::[a-f0-9]{1,4}){1,4}|(?:[a-f0-9]{1,4}:){2}(?::[a-f0-9]{1,4}){1,5}|(?:[a-f0-9]{1,4}:)(?::[a-f0-9]{1,4}){1,6}|(?:[a-f0-9]{1,4}:){1,6}:|:(?::[a-f0-9]{1,4}){1,6}|[a-f0-9]{0,4}::|(?:[a-f0-9]{1,4}:){7}[a-f0-9]{1,4}',\
      'md5 hash':'^[a-fA-F0-9]{32}$',\
      'SHA1 hash':'^[a-fA-F0-9]{40}$',\
      'SHA224 hash':'^[a-fA-F0-9]{56}$',\
      'SHA256 hash':'^[a-fA-F0-9]{64}$',\
      'SHA384 hash':'^[a-fA-F0-9]{96}$',\
      'SHA512 hash':'^[a-fA-F0-9]{128}$',\
      'Bitcoin private key':'^5[HJKL][1-9A-HJ-NP-Za-km-z]{49,51}',\
      'Bitcoin addr':'([13][a-km-zA-HJ-NP-Z0-9]{26,33})',\
      'bcrypt hash':'\$2a\$\d\d\$[\s\S]{53}',\
      'CC Amex Card':'^3[47][0-9]{13}$',\
      'CC BCGlobal':'^(6541|6556)[0-9]{12}$',\
      'CC Carte Blanche Card':'^389[0-9]{11}$',\
      'CC Diners Club Card':'^3(?:0[0-5]|[68][0-9])[0-9]{11}$',\
      'CC Discover Card':'^65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})$',\
      'CC Insta Payment Card':'^63[7-9][0-9]{13}$',\
      'CC JCB Card':'^(?:2131|1800|35\d{3})\d{11}$',\
      'CC KoreanLocalCard':'^9[0-9]{15}$',\
      'CC Laser Card':'^(6304|6706|6709|6771)[0-9]{12,15}$',\
      'CC Maestro Card':'^(5018|5020|5038|6304|6759|6761|6763)[0-9]{8,15}$',\
      'CC Mastercard':'^(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))$',\
      'CC Solo Card':'^(6334|6767)[0-9]{12}|(6334|6767)[0-9]{14}|(6334|6767)[0-9]{15}$',\
      'CC Switch Card':'^(4903|4905|4911|4936|6333|6759)[0-9]{12}|(4903|4905|4911|4936|6333|6759)[0-9]{14}|(4903|4905|4911|4936|6333|6759)[0-9]{15}|564182[0-9]{10}|564182[0-9]{12}|564182[0-9]{13}|633110[0-9]{10}|633110[0-9]{12}|633110[0-9]{13}$',\
      'CC Union Pay Card':'^(62[0-9]{14,17})$',\
      'CC Visa Card':'^4[0-9]{12}(?:[0-9]{3})?$',\
      'CC Visa Master Card':'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$'}


################################################################################
#You dont want to do any double work now, do you?
scraped = ['scraping']
try:
    scraped += open(scraped_file,"r").read().split('\n')
except: pass
scraped  = list(dict.fromkeys(scraped)) # dont need doubles.


################################################################################
# Fetch archive()
# fetches and parshes archive page,
# returns list of pastbin ids or 0 if fails
def fetch_archive():
    url = 'https://pastebin.com/archive'
    try:
        pb = requests.get(url).text
        x = re.findall(r'<a href=\"/[0-9a-zA-Z]{8}">', pb)
        r = []
        for l in x:
            r.append(l[10:-2])
    except:
        r = 0
    return r

################################################################################
# get_paste(str pastebinid)
# content from pastbin id
# returns :
# [str content, bool expires, str pastid]
def get_paste(x):
    if x != 'scraping':
        url = 'https://pastebin.com/'+x
        bad = 'This page has been removed!'
        start = '<textarea id="paste_code" class="paste_code" name="paste_code" onkeydown="return catchTab(this,event)">'
        end = '</textarea>'
        start_exp = 'When this paste gets automatically deleted'
        good_exp = 'Never'
        try:
            pb = requests.get(url).text
            if bad not in pb:
                paste = pb[pb.index(start)+len(start):]
                paste = paste[:paste.index(end)]
                if good_exp in pb[pb.index(start_exp)+len(start_exp):pb.index(start_exp)+len(start_exp)+20]:
                    expire = 0
                else:
                    expire = 1
                r = [paste,expire,x]
        except:
            pass
    try:
        r
    except NameError:
        r = [open(__file__).read(),0,'scraping'] # if shit is fucked just return yourself.
    return r                                     # set the id to 'scraping' to avoid scraping :P

################################################################################
# save_paste(str id, str paste)
# save paste to file in save_path
# returns 1 on sucsess 0 if fails.
def save_paste(id, paste):
    try:
        f = open(save_path+id, "w+")
        f.write(paste)
        f.close()
        r = 1
    except:
        r = 0
    return r

################################################################################
# write_to_log(list stuff)
# writes to log file.
def write_to_log(stuff,url):
    f = open(output_file, "a+")
    f.write('\n'+'-'*80+'\n'+url+'\n')
    for z in stuff:
        try:
            f.write(z+'\n')
        except:
            f.write('CONTAINS SOME FUCKED UP CHARCTER')
    f.close()

################################################################################
# scrape(str pastebinid, str pastecontent, bool expire)
# checks for regex matches.
# checks for trigger-words.
def scrape(id, paste, save):
    if id not in scraped:
        url = 'https://pastebin.com/'+id
        stuff = []
        split_paste = re.split('\s|\n', paste)
        for paste_string in split_paste:
            #print paste_string
            for k,patern in rx.items():
                if re.match(patern,paste_string):
                    stuff.append(k.rjust(15)+': '+paste_string)
        for x in tw:
            if x.lower() in paste.lower():
                stuff.append('trigger-word'.rjust(15)+': '+x)
        for x in save_tw:
            if x.lower() in paste.lower():
                stuff.append('save-trigger-word'.rjust(15)+': '+x)
                save = 1
        if (len(stuff) > 0):
            if do_save and save:
                if save_paste(id,paste):
                    stuff=['paste is saved to :'+save_path+id]+stuff
            write_to_log(stuff,url)
        scraped.append(id)
        save_scraped(scraped)
        return 1
    else:
        return 0

################################################################################
# silent()
# same as screensaver but without output.
# nice for debuging or just running the scraper.
def silent():
    while 1:
        data = next_in_que(fetch_que())
        scrape(data[2], data[0],data[1])
        sleep(20)

################################################################################
# screensaver()
# is not realy a screen saver it just spams your console with
# the latest pastes from pastebin.
# oh, yeah and also scrapes for interesting data.
def screensaver():
    from pygments import highlight
    from pygments import lexers
    from pygments.formatters import TerminalFormatter
    max = 1024 # max lines to display
    delay = 0.05
    formatter = TerminalFormatter()
    c = 0
    if do_printself:
        for y in open(__file__).readlines():
            if (c < 31):
                print y[:-1]
            else:
                print highlight(y, lexers.PythonLexer(), formatter)[:-1]
            sleep(delay)
            c +=1
    while 1:
        s = next_in_que(fetch_que())
        x = s[2] # update id incase it returns it self.
        if do_scrape == 1:
            scrape(x, s[0],s[1])
        relax = lexers.guess_lexer(s[0])
        counter=0
        for c in s[0].split('\n'):
            if counter > max:
                break
            print highlight(c, relax, formatter)[:-1]
            sleep(delay)
            counter+=1

def save_que(que):
    try:
        f = open(que_file,"w+")
        f.write('\n'.join(que))
        f.close()
        r = 1
    except:
        r = 0
    return r

def fetch_que():
    try:
        f = open(que_file, "r")
        que = f.read().split('\n')
        f.close()
    except:
        que = fetch_archive()
    if len(que) < 5:    #update que if it's small
        que += fetch_archive()
    for x in scraped:
        list(filter(lambda a: a != x, que))
    que = list(dict.fromkeys(que))
    #print que
    return que

def fetch_scaped():
    f = open(scraped_file, "r")
    scraped += f.read().split('\n')
    f.close()
    scraped = list(dict.fromkeys(scraped))
    return scraped

def next_in_que(que):
    s=get_paste(que[0])
    que = que[1:]
    x = s[2] # update id incase it returns it self.
    if do_scrape == 1:
        scrape(x, s[0],s[1])
    save_que(que)
    return s

def save_scraped(srka):
    try:
        f = open(scraped_file,"w+")
        f.write('\n'.join(srka))
        f.close()
        r = 1
    except:
        r = 0
    return r

def just_one():
    s = next_in_que(fetch_que())
    x = s[2] # update id incase it returns it self.
    if do_scrape == 1:
        scrape(x, s[0],s[1])
    print s[0]

################################################################################
# nu is het main-us
try :
    if sys.argv[1] == "o":
        just_one()
    if sys.argv[1] == "s":
        silent()
except:
    screensaver()
