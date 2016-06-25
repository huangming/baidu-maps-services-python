# -*- coding: utf-8 -*-
import sys
PY2 = sys.version[0] == '2'
from baidumaps import Client
import re

bdmaps = Client(ak='cQlzSOBQEZGTbhHTbeUMcTU62vakzrvF')
def findbus(from_place,to_place,city='深圳',mode = 'transit'):
    # result = bdmaps.geoconv('114.21892734521,29.575429778924')
    if city=='':city='深圳' 
    try:
        result = bdmaps.direct(from_place,to_place,mode,region=city)
    except:
        return ''
    mymsg = ''
    content = ''
    for i in range(len(result['routes'])):
        scheme = result['routes'][i]
        content += '[方案%d]: 从%s'%(i+1,from_place)
        timeout = 0
        for steplist in scheme['steps']:
            step = steplist[0]
            if step['type']==5:
                content += ' '
                if PY2:
                    content += step['stepInstruction'].encode('utf-8')
                else:
                    content += step['stepInstruction']
                content += ' '
            elif step['type']==3:
                pattern = '''<font[.\n]*?color=.*?>'''
                stepinfo = re.sub(pattern,'',step['stepInstruction'])
                pattern = '''</font>'''
                stepinfo = re.sub(pattern,'',stepinfo)
                pattern = '''<font color=.*?>'''
                stepinfo = re.sub(pattern,'',stepinfo)
                if PY2:
                    content += stepinfo.encode('utf-8')
                else:
                    content += stepinfo
            timeout += step['duration']
        content += ' 到达%s 用时%d分钟\n'%(to_place,timeout/60)
    return content if len(content)>0 else False
print(findbus('机场','坪洲'))
