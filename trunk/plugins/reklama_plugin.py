# -*- coding: utf-8 -*-

REKLAMA_FILE ='dynamic/reklama.txt'

initialize_file(REKLAMA_FILE, '{}')

REKLAMA_LAST = 0

REKLAMA_N = 0

try:
    REKLAMA=eval(read_file(REKLAMA_FILE))
except:
    REKLAMA={}

def reklama_join(g, n, r, afl):
    if time.time() - INFO['start']<60: return
    if MAFIA_SES['start']: return
    
    global REKLAMA
    global REKLAMA_LAST
    global REKLAMA_FILE
    global REKLAMA_N

    k = 0
    
    if time.time()-REKLAMA_LAST<60: return
    jid=get_true_jid(g+'/'+n)
    if n==get_bot_nick(g): return
    if not jid in REKLAMA.keys():
        REKLAMA[jid]=time.time()
        write_file(REKLAMA_FILE, str(REKLAMA))
        k=1
    else:
        if time.time() - REKLAMA[jid]>172800:
            REKLAMA[jid]=time.time()
            write_file(REKLAMA_FILE, str(REKLAMA))
            k=1
    if k:
        REKLAMA_N+=1
        time.sleep(5)
        REKLAMA_LAST=time.time()
        msg(g+'/'+n, u'А вы не желаете сыграть в мафию? (команда !мафия в приват)')

register_join_handler(reklama_join)
