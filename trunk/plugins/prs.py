# -*- coding: utf-8 -*-

def hnd_prs(prs):
    try: typ = prs['type']
    except: typ = 'available'
    if typ!='available': return
    try:
        fromjid = prs['from'].split('/')
    except: return
    groupchat = fromjid[0]
    nick = prs['from'][len(groupchat)+1:]
    jid = get_true_jid(groupchat+'/'+nick)
    _item = None
    if groupchat in GROUPCHATS:
        if jid in GLOBACCESS:
            return
        else:
            if groupchat in ACCBYCONFFILE and jid in ACCBYCONFFILE[groupchat]:
                pass
	    else:
                if groupchat in GROUPCHATS and nick in GROUPCHATS[groupchat]:
                    try:
                        _x = [i for i in prs.children if (i.name=='x') and (i.uri=='http://jabber.org/protocol/muc#user')][0]
                        _item = [i for i in _x.children if i.name=='item'][0]
                    except:
                        pass
                    if jid != None and _item != None:
                        role = _item['role']
			aff = _item['affiliation']
			if role in ROLES:
                            accr = ROLES[role]
			    if role=='moderator' or user_level(jid,groupchat)>=15:
                                GROUPCHATS[groupchat][nick]['ismoder'] = 1
			    else:
                                GROUPCHATS[groupchat][nick]['ismoder'] = 0
			else:
                            accr = 0
			if aff in AFFILIATIONS:
                            acca = AFFILIATIONS[aff]
			else:
                            acca = 0
			access = accr+acca
			change_access_temp(groupchat, jid, access)

def check_s2s():
    time.sleep(20)
    for gch in GROUPCHATS.keys():
        packet = IQ(JAB, 'get')
        packet.addElement('query', 'jabber:iq:version')
        packet.addCallback(s2s_result_handler, gch)
        reactor.callFromThread(packet.send, gch+'/'+get_bot_nick(gch))
    threading.Timer(280, check_s2s).start()

def s2s_result_handler(gch, x):
    if x['type'] == 'error':
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: code = []
        if not ' '.join(code) in ['405']:
            threading.Timer(60, join(gch, get_bot_nick(gch)))

register_stage0_init(check_s2s)
register_presence_handler(hnd_prs)
