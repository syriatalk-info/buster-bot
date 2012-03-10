#===istalismanplugin===
# -*- coding: utf-8 -*-

#TR_EN = {u'sch':u'щ', u'yu':u'ю', u'yi':u'ы', u'ch':u'ч', u'zh':u'ж', u'ya':u'я', u'sh':u'ш', u'c':u'ц', u'a':u'а', u'b':u'б', u'v':u'в', u'g':u'г', u'd':u'д', u'e':u'е', u'z':u'з', u'i':u'и', u'j':u'й', u'k':'к', u'l':u'л', u'm':u'м', u'n':u'н', u'o':u'о', u'p':u'п', u'r':u'р', u's':u'с', u't':u'т', u'u':u'у', u'f':u'ф', u'h':u'х', u'\'':u'ь'}

TR_EN = ((u'sch',u'щ'),
         (u'yu',u'ю'),
         (u'yi',u'ы'),
         (u'ch',u'ч'),
         (u'zh',u'ж'),
         (u'ya',u'я'),
         (u'sh',u'ш'),
         (u'c',u'ц'),
         (u'a',u'а'),
         (u'b',u'б'),
         (u'v',u'в'),
         (u'g',u'г'),
         (u'd',u'д'),
         (u'e',u'е'),
         (u'z',u'з'),
         (u'i',u'и'),
         (u'j',u'й'),
         (u'k',u'к'),
         (u'l',u'л'),
         (u'm',u'м'),
         (u'n',u'н'),
         (u'o',u'о'),
         (u'p',u'п'),
         (u'r',u'р'),
         (u's',u'с'),
         (u't',u'т'),
         (u'u',u'у'),
         (u'f',u'ф'),
         (u'h',u'х'),
         (u'\'',u'ь'))

def translit_msg(raw, type, source, parameters):
    ru=0
    rep=''
    if not type in ['groupchat','public'] or parameters.count('http://') or parameters.count('@con') or len(parameters)<4:
        return
    if source[2]==get_bot_nick(source[1]):
        return
    if parameters.split()>0:
        s=parameters.split()[0]
        z=s.replace(',','').replace(':','')
        if source[1] in GROUPCHATS and z in GROUPCHATS[source[1]]:
            parameters=parameters.replace(s,'')
            parameters=parameters.strip()
    if parameters[0] in ['*',':','@']:
        return
    if parameters[0]==parameters[1] and parameters[1]==parameters[2]:
        return
    parameters=parameters.lower()
    if parameters in [u'katapul\'tu',u'rr',u'harakiri']:
        return
    for x in parameters:
        if ord(x)>127:
            ru=1
            break
    if ru: return
    for c,b in TR_EN:
        try:
            parameters=parameters.replace(c, b)
        except: pass
    cmd=parameters.lower()
    pr=''
    if parameters.split()>0:
        args=parameters.split()
        cmd=parameters.split()[0]
        cmd=parameters.lower()
        pr=' '.join(args[1:])
    if COMMAND_HANDLERS.has_key(cmd):
        call_command_handlers(cmd, type, source, parameters, None)
    else:
        msg(source[1], parameters)

register_message_handler(translit_msg)
