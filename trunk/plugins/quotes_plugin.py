#===istalismanplugin===
# -*- coding: utf-8 -*-

import urllib2,re,urllib,socket

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

ALIAS_URL_FILE = 'dynamic/alias_url.txt'

db_file(ALIAS_URL_FILE, dict)

try: ALIAS_URL = eval(read_file(ALIAS_URL_FILE))
except: ALIAS_URL = {}

def hnd_alias_url(t, s, p):
        if not s[1] in GROUPCHATS: return
        if not p:
                if not s[1] in ALIAS_URL.keys():
                        reply(t, s, u'Нет алиасов')
                        return
                reply(t, s, '\n'.join([str(ALIAS_URL[s[1]].keys().index(x)+1)+') '+x+' - '+ALIAS_URL[s[1]][x] for x in ALIAS_URL[s[1]].keys()]))
                return
        if p.isdigit():
                for x in ALIAS_URL[s[1]]:
                        if str(ALIAS_URL[s[1]].keys().index(x)+1) == p:
                                del ALIAS_URL[s[1]][x]
                                write_file(ALIAS_URL_FILE, str(ALIAS_URL))
                                reply(t, s, u'Удалил!')
                                return
                reply(t, s, u'Алиаса с таким номером нет в списке!')
                return
        if not p.count(' '):
                reply(t, s, u'Синтаксис - <команда> <url>')
                return
        ss = p.split()
        if ss[0].lower() in COMMANDS.keys():
                reply(t, s, u'Недопустимое имя алиаса!')
                return
        
        if not s[1] in ALIAS_URL.keys():
                ALIAS_URL[s[1]]={}
                
        ALIAS_URL[s[1]][ss[0].lower()]=ss[1]
        reply(t, s, u'Добавил!')
        write_file(ALIAS_URL_FILE, str(ALIAS_URL))

register_command_handler(hnd_alias_url, 'alias_url', ['все'], 20, 'Просмотр сайтов и цитатников с помощью алиасов. Без параметров покажет список алиасов. Чтобы удалить алиас используем номер алиаса в списке. В строке url есть следующие переменные - $p -текст, $qot - параметры в виде %D0%BF%D0%B8%D0%B2%D0%BE, $n1 - рандомное число 0-10, $n2 число от 10-100 ну и $n3 до 1000', 'alias_url <command> <url>', ['poem'])                                        

def hnd_msg_alias_url(r, t, s, p):
        if not s[1] in ALIAS_URL.keys(): return
        pr = p.lower()
        pt = ''
        qot = ''
        if p.count(' '):
                ss = p.split()
                pr = ss[0].lower()
                try: pt = ss[1]
                except: pass
        if pr in ALIAS_URL[s[1]]:
                exc = ALIAS_URL[s[1]][pr].encode('utf8')
                if not pt.isdigit():
                        pt = pt.encode('utf8','replace')
                if pt:
                        qot = urllib.quote(pt)
                        
                exc = exc.replace('$p', pt)
                exc = exc.replace('$qot', qot)
                exc = exc.replace('$n1',str(random.randrange(0,10))).replace('$n2',str(random.randrange(10,100))).replace('$n3',str(random.randrange(100,1000)))
                reply(t, s, send_urlopen_q(exc,1))

register_message_handler(hnd_msg_alias_url)

def send_urlopen_q(url, i=0):
        req = urllib2.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
	try:
                req = urllib2.urlopen(req, timeout = 3)
                enc = req.headers.getparam('charset')
                rep = req.read().decode(enc, 'replace')
                if i: return universal_html_parser(rep)
                return rep
	except urllib2.URLError, e:
                if isinstance(e.reason, socket.timeout): return u'Время ожидания вышло'
                else: return u'Сайт упал'
        except Exception as err: return err.message
        return str()

def gogii(t, s, p):
        reply(t, s, send_urlopen_q(p))

register_command_handler(gogii, 'qqq', ['все'], 0, 'random poem', 'poem', ['poem'])                                        
        

def remove_trash(body):
        body = re.compile(r'<style[^<>]*?>.*?</style>',re.DOTALL | re.IGNORECASE).sub('', body)
        body = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', body)
        body = re.compile(r'<!--.*?-->',re.DOTALL | re.IGNORECASE).sub('', body)
        body = re.compile(r'&#.*?;',re.DOTALL | re.IGNORECASE).sub('', body)
        return body


def remove_space(body):
        if body.count('\n'):
                body = '\n'.join([x for x in body.split('\n') if not x.isspace() and len((x if not x.count(' ') else ''.join(x.split(' '))))>1])
        if body.count(chr(9)):
                body = body.replace(chr(9),'')
        last = 0
        try: body = ' '.join([x for x in body.split(' ') if x!=''])
        except: pass
        return body

def remove_link(body):
        body = re.compile(r'<a href=\".*?>.*?</a>',re.DOTALL | re.IGNORECASE).sub('', body)
        return body

def universal_html_parser(body):
        if not isinstance(body, basestring):
                return 'Object has not atrr string'
        return remove_space(decode_s(remove_link(remove_trash(body))))

def handler_bashorgru_get(type, source, parameters):
	if parameters.strip()=='':
		req = urllib2.Request('http://bash.im/random')
	else:
		req = urllib2.Request('http://bash.im/quote/'+parameters.strip())
	req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
	try:
		r = urllib2.urlopen(req)
		target = r.read()
		target = re.compile(r'<script.*?>.*?</script>',re.DOTALL | re.IGNORECASE).sub('', target)
		"""link to the quote"""
		try: id = re.findall('<a href=\"/quote/(.*?)\" class=\"id\">#(.*?)</a>', target)[0][0]
		except: id = ''
		msg = re.findall('<div class=\"text\">(.*?)</div>', target)[0]
		msg = msg.replace('<br />','\n').replace('&quot;','\"').replace('&gt;',':').replace('<br>','\n')
		reply(type,source,unicode(('#'+id+':\n' if id else '')+msg,'windows-1251'))
	except:
		reply(type,source,u'очевидно, они опять сменили разметку')
            

def decode_s(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('&middot;','').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

def decode(text):
    return strip_tags.sub('', text.replace('<br />','\n').replace('&middot;','').replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('\t','').replace('||||:]','').replace('>[:\n','')

def handler_celebration(type, source, parameters):
    try:
        req = urllib2.Request('http://wap.n-urengoy.ru/cgi-bin/wappr.pl')
        req.add_header = ('User-agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<div class="title">',target)
        message = target[od.end():]
        message = message[:re.search('назад',message).start()]
        message = '\n' + message.strip()
        message = message.replace('<','').replace('.','').replace('>','').replace('/','\n').replace('_','').replace('a','').replace('s','').replace('d','').replace(':','').replace('f','').replace('g','').replace('h','').replace('=','').replace('-','').replace('j','').replace('k','').replace('l','').replace('q','').replace('%','').replace('w','').replace('e','').replace('r','').replace('t','').replace('y','').replace('u','').replace('i','').replace('"','').replace('o','').replace('p','').replace('z','').replace('x','').replace('c','').replace('v','').replace('#','').replace('b','').replace('n','').replace('m','').replace('A','').replace('S','').replace('D','').replace('F','').replace('G','').replace('H','').replace('K',' ').replace('L',' ').replace('Q',' ').replace('W',' ').replace('E','')
        message = message.replace('Y','').replace('<br/>','\n').replace('I','').replace('O','').replace('P','').replace('Z','').replace('X','').replace('C','').replace('V','').replace('B','').replace('N','').replace('M','').replace(';','').replace('[','').replace(']','')
        if message.isspace():
                reply(type,source,u'наверно разметку сменили')
                return
        reply(type, source, unicode(remove_space(message),'UTF-8'))
    except: reply(type, source, u'Что-то сломалось!')

def handler_jc_show(type, source, parameters):
        if not parameters: return
        try:
                req = urllib2.Request('http://jc.jabber.ru/search.html?search='+parameters.encode('utf-8'))
                req.add_header('User-Agent','Mozilla/5.0 (Linux; U; Android 2.2.1; sv-se; HTC Wildfire Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1')
                req = urllib2.urlopen(req).read()
                rep = re.findall('<div>(.*?)</div>', req, re.DOTALL | re.IGNORECASE)[0]
                rep = remove_space(decode_s(rep))
                reply(type, source, rep)
        except: reply(type, source, send_urlopen_q('http://jc.jabber.ru/search.html?search='+parameters.encode('utf-8'), 1))


def handler_lurk(type, source, parameters):
        try:
                if parameters:
                        req = urllib2.Request('http://lurkmore.to/'+parameters.encode('utf-8'))
                        req.add_header = ('User-agent', 'Opera')
                        i = urllib2.urlopen(req)
                        page = i.read()
                        target=''
                        t = re.findall('<p>.*.',page,re.DOTALL | re.IGNORECASE)
                        for x in t:
                                x=x.replace('</p>','\n')
                                if not x.count('.') and not x.isspace():
                                        if x!='':
                                                x+'.'
                                target+=x
                        target = target.replace('if (window.showTocToggle) { var tocShowText = "показать"; var tocHideText = "убрать"; showTocToggle(); }','').replace('<br /','')
                        target = decode_s(target)
                        if target.isspace():
                                reply(type, source, u'аблом!')
                                return
                        reply(type,source,target.replace('\n\n','\n'))
                else:
                        reply(type, source, u'лурк - это тема,только слово еще напиши!')
                        return
        except:
                reply(type, source, u'Ничего не найдено!')

def handler_anek_s(type,source,parameters):
        reklama = [u'']
        try:
                u = urllib.urlopen('http://anekdot.odessa.ua/rand-anekdot.php')
                target = u.read()
                od = re.search('>',target)
                h1 = target[od.end():]
                h1 = h1[:re.search('<a href=',h1).start()]
                message = decode_s(h1)
                reply(type ,source, u'Анекдот: \n'+unicode(message,'windows-1251'))
        except:
                reply(type ,source, u'Упс.. Сайт упал..')

def clck_quest(type,source,parameters):
        if parameters:
                try:
                        fetcher = urllib2.urlopen('http://clck.ru/--?url='+parameters.encode('utf-8'))
                        rep=fetcher.read()
                        reply(type,source,rep)
                except:
                        reply(type,source,'что-то сломалось!')
                        pass

def hnd_fun_k(type,source,parameters):
        ALL=[]
        if type in ['private','icq','chat']:
                return
        NO=[u'дал па галаве веником',u'нехватило',u'не насыпал',u'плюнул в миску']
        if source[1] in GROUPCHATS:
                n=0
                for x in GROUPCHATS[source[1]]:
                        if GROUPCHATS[source[1]][x]['ishere']==1 and x!=get_bot_nick(source[1]):
                                n+=1
                                ALL.append(x)
                if n<3:
                        reply(type,source,u'зови народ,тогда и зохаваем!')
                        return
                no=random.choice(ALL)
                yes=''
                for x in ALL:
                        if x!=no:
                                yes+=u'насыпал '+x+'\n'
                msg(source[3], source[1], yes)
                time.sleep(1.5)
                msg(source[3], source[1],u' a '+no+' '+random.choice(NO))

def hnd_lust_ru(type,source,parameters):
        try:
                rep = send_urlopen_q('http://www.notproud.ru/random.html', 1)
                rep = rep.replace(u'читать дальше >','').replace(u'наткнуться случайно>','')
                reply(type, source, rep)
        except: reply(type,source,u'Что-то сломалось!')

def hnd_drem_talk(type,source,parameters):
        try:
                if not parameters: return

                if parameters.count(' '): parameters=parameters.replace(' ','+')
                
                rep = send_urlopen_q('http://2yxa.ru/pics/sonnik.php?poisk='+urllib.quote(parameters.encode('utf8')),1)
        
                reply(type, source, rep)
        except:
                reply(type, source, u'Что-то сломалось!')

def hnd_darvin_p(type,source,parameters):
        try:
                num = str(random.randrange(1,700))
                rep = send_urlopen_q('http://2yxa.ru/darwin/?st='+num.encode('utf-8'), 1)
                reply(type,source,rep)
        except: reply(type, source, u'Что-то сломалось!')

def kill_me_quotes(type, source, parameters):
        try:
                num = str(random.randrange(1, 7400))
                if parameters and parameters.isdigit():
                        num = parameters
                rep = send_urlopen_q('http://killmepls.ru/story/'+num, 1)
                rep = rep.replace(u'•  • Пишите нам:  • 18+','')
                reply(type, source, rep)
        except:
                reply(type, source, u'Что-то сломалось!')

def hnd_poem(type, source, parameters):
        a=[u"Я помню",u"Не помню",u"Забыть бы",u"Купите",u"Очкуеш",u"Какое",u"Угробил",u"Хреново",u"Открою",u"Ты чуешь?"]
        b=[u"чудное",u"странное",u"некое",u"вкусное",u"пьяное",u"свинское",u"чоткое",u"сраное",u"нужное",u"конское"]
        c=[u"мнгновенье",u"затменье",u"хотенье",u"варенье",u"творенье",u"везенье",u"рожденье",u"смущенье",u"печенье",u"ученье"]
        d=[u"передомной",u"под косячком",u"на кладбище",u"в моих мечтах",u"под скальпилем",u"в моих штанах",u"из-за угла",u"в моих ушах",u"в ночном горшке",u"из головы"]
        e=[u"явилась ты",u"добилась ты",u"торчат кресты",u"стихов листы",u"забилась ты",u"мои трусы",u"поют дрозды",u"из темноты",u"помылась ты",u"дают пизды"]
        f=u'как'
        g=[u"мимолётное",u"детородное",u"психотропное",u"кайфоломное",u"очевидное",u"у воробушков",u"эдакое вот",u"нам не чуждое",u"благородное",u"ябывдульское"]
        j=[u"виденье",u"сиденье",u"паренье",u"сужденье",u"вращенье",u"сношенье",u"смятенье",u"теченье",u"паденье",u"сплетенье"]
        h=[u"как гений",u"как сторож",u"как символ",u"как спарта",u"как правда",u"как ангел",u"как водка",u"как пиво","как ахтунг",u"как жопа"]
        i=[u"чистой",u"вечной",u"тухлой",u"просит",u"грязной",u"липкой",u"на хрен",u"в пене",u"женской",u"жаждет"]
        k=[u"красоты",u"мерзлоты",u"суеты",u"наркоты",u"срамоты",u"школоты",u"типа ты",u"простоты",u"хуиты",u"наготы"]
        reply(type, source, random.choice(a)+'\n'+random.choice(b)+'\n'+random.choice(c)+'\n'+random.choice(d)+'\n'+random.choice(e)+'\n'+f+' '+random.choice(g)+'\n'+random.choice(j)+'\n'+random.choice(h)+'\n'+random.choice(i)+'\n'+random.choice(k))

register_command_handler(hnd_poem, 'poem', ['все'], 0, 'random poem', 'poem', ['poem'])                                        
register_command_handler(kill_me_quotes, 'killme', ['все'], 0, 'Кажется, что жизнь повернулась спиной? Поверьте, бывает и хуже... http://killmepls.ru/', 'killme', ['killme'])                                        
register_command_handler(hnd_darvin_p, 'дарвин', ['все'], 0, 'премия дарвина', 'дарвин', ['дарвин'])                                        
register_command_handler(hnd_drem_talk, 'сон', ['все'], 0, 'толкование сна по ключевому слову', 'сон <слово>', ['сон деньги'])                                
register_command_handler(hnd_lust_ru, 'признание', ['фан','все'], 0, 'признание с http://www.notproud.ru/lust/', 'признание', ['признание'])                
register_command_handler(hnd_fun_k, 'каша', ['фан','все'], 0, 'раздача каши', 'каша', ['каша'])                
register_command_handler(clck_quest, 'clck', ['все'], 0, 'Выдает короткую ссылку взамен введенного URL', 'clck <url>', ['clck http://40tman.ucoz.ru'])
register_command_handler(handler_anek_s, 'анекдот', ['фан','все'], 0, 'Случайный анекдот из http://wap.obas.ru/', 'анекдот', ['анекдот'])
register_command_handler(handler_lurk, 'лурк', ['инфо','фан','все'], 0, 'Показывает статью из http://lurkmore.ru/','лурк <слово>', ['лурк херка'])
register_command_handler(handler_jc_show, 'jc', ['все','mod','инфо'], 0, 'Поиск конференций в рейтинге jc.jabber.ru', 'jc <конфа>', ['jc goth'])
register_command_handler(handler_jc_show, 'рейтинг', ['все','mod','инфо'], 0, 'Поиск конференций в рейтинге jc.jabber.ru', 'рейтинг <конфа>', ['рейтинг goth'])
register_command_handler(handler_celebration, 'праздники', ['все','mod','инфо'], 0, 'Показывает праздники сегодня/завтра', 'праздники', ['праздники'])
register_command_handler(handler_bashorgru_get, 'бор', ['фан','инфо','все'], 0, 'Показывает случайную цитату из бора (bash.org.ru). Также может по заданному номеру вывести.', 'бор', ['бор 223344','бор'])
