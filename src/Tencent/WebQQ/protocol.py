# -*- coding: utf-8 -*-
"""
webqq3的各种协议
"""
import os,os.path
import urllib, urllib2, cookielib
from urllib2 import BaseHandler
import webqq3config
import tempfile
from StringIO import StringIO
import json,random,time

COOKIEFILE='cookies.jwp'
TXHEADERS={'User-agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

###################################################################
###################################################################
#http头相关
###################################################################
from gzip import GzipFile
from StringIO import StringIO
class ContentEncodingProcessor(urllib2.BaseHandler):
    """
    zip处理
    """
 
    # add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip, deflate")
        return req
    
    # decode
    def http_response(self, req, resp):
        old_resp = resp
        # gzip
        if resp.headers.get("content-encoding") == "gzip":
            gz = GzipFile(
                        fileobj=StringIO(resp.read()),
                        mode="r"
                      )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
        # deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO( deflate(resp.read()) )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp
 
# deflate support
import zlib
def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
    try:               # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)

###################################################################
class SimpleCookieHandler(urllib2.BaseHandler):
    """
    自定义得cookieHandler，方便随意插入修改cookie
    """
    cookies={}
    
    
    def __init__(self):
        pass
    
    def http_request(self, request):
        
        request.add_unredirected_header('Cookie', self.getCookies())
        print 'cookies ->:',self.getCookies()
        return request

    def http_response(self, request, response):
        headers=response.info()
        cookies=headers.getheaders("Set-Cookie")
        for cookie in cookies:
            k=cookie.split('=')[0]
            v=cookie.split('=')[1].split(';')[0]
            self.cookies[k]=v
        print 'cookies ->:',self.getCookies()
        return response
    
    def getCookies(self):
        return "; ".join(["%s=%s" % (k, v) for k, v in self.cookies.items()])
    
###################################################################



###################################################################
###################################################################
#webqq协议
###################################################################   

#开启调试信息 
debugHandler=urllib2.HTTPHandler(debuglevel=1)
#增加调试处理与cookie处理
opener=urllib2.build_opener(SimpleCookieHandler(),debugHandler,ContentEncodingProcessor())
#装载处理器
urllib2.install_opener(opener)

################################################################### 
class Login:
    """
    登录
    """
    
    
    def __init__(self):
        self.cookies=SimpleCookieHandler.cookies
        pass
    
    def getCheckImg(self,uin,code):
        """
        获取图片验证码
        """
        
        url=webqq3config.getURL('check_code_p')
        txdata=urllib.urlencode({"aid":"1003903","uin":uin,"vc_type":code})
        try:
            req=urllib2.Request( url % txdata)
            req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
            req.add_header('Connection', 'Keep-Alive')
            req.add_header('Referer',webqq3config.getHeader('refer_ui_ptlogin2_qq_com_login') )
            
            handle=urllib2.urlopen(req)
            
            result=handle.read()
            Login.imgfile=tempfile.NamedTemporaryFile()
            Login.imgfile.write(result)
            Login.imgfile.seek(0)
            return Login.imgfile.name
        except IOError, e:
            print e
    
    def login(self,uin,passwd,code):
        """
        登录
        """
        passwd,code=str(passwd),str(code)
        
        
        from md5 import MD5
        qmd5=MD5()
        passwd=qmd5.md5(qmd5.md5_3(passwd)+code.upper())
        
        
        
        url=webqq3config.getURL('login')
        txdata=urllib.urlencode({"u":uin,
                                "p":passwd,
                                "verifycode":code,
                                "webqq_type":"10",
                                "remember_uin":"1",
                                "login2qq":"1",
                                "aid":"1003903",
                                "u1":"http://web3.qq.com/loginproxy.html?login2qq=1&webqq_type=10",
                                "h":"1",
                                "ptredirect":"0",
                                "ptlang":"2052",
                                "from_ui":"1",
                                "pttype":"1",
                                "dumy":"",
                                "fp":"loginerroralert",
                                "mibao_css":"m_webqq",
                                "action":"2-22-10926"
                                 })
        try:
            req=urllib2.Request( url % txdata)
            req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
            req.add_header('Connection', 'Keep-Alive')
            #req.add_header('Referer',webqq3config.getHeader('refer_d_web2_qq_com_proxy') )
            req.add_header('Referer','http://ui.ptlogin2.qq.com/cgi-bin/login?target=self&mibao_css=m_webqq&appid=1003903&s_url=http%3A%2F%2Fweb3.qq.com%2Floginproxy.html&f_url=loginerroralert&strong_login=1&login_state=10' )
            
            
            self.cookies['chkuin']=uin
            self.cookies['confirmuin']=uin
            
            handle=urllib2.urlopen(req)
            
            result=handle.read()
            codes=result.split("""'""")
            return codes[1],codes[9]
        except IOError, e:
            print e
            
    
    def loginChannel(self,uin,status):
        """
        正式登录
        """
        
        #首先添加cookie
        clientid=str(int(random.uniform(0,99)))+str(int(time.time())%1000000)
        
        SimpleCookieHandler.cookies['o_cookie']=uin
        SimpleCookieHandler.cookies['ptui_loginuin']=uin
        SimpleCookieHandler.cookies['clientid']=clientid
        
        
        
        #然后构造json
        import json
        pyobj={"status":"online",
               "ptwebqq":SimpleCookieHandler.cookies.get("ptwebqq"),
               "clientid":clientid}
        
        jsonstr=json.dumps(pyobj,separators=(',',':'))
        
        
        params=urllib.urlencode({"r":jsonstr,"clientid":clientid})
        
        
        url=webqq3config.getURL('channel_login')
        try:
            req=urllib2.Request( url,params)
            req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
            req.add_header('Connection', 'Keep-Alive')
            req.add_header('Referer',webqq3config.getHeader('refer_d_web2_qq_com_proxy') )
            
            handle=urllib2.urlopen(req)
            result=handle.read()
            
            jresult=json.loads(result)
            SimpleCookieHandler.cookies['psessionid']=jresult.get('result').get('psessionid')
            SimpleCookieHandler.cookies['vfwebqq']=jresult.get('result').get('vfwebqq')
    
            return jresult
        except IOError, e:
            print e
            
        
            
    def getCheckCode(self,uin):
        """
        获取文字验证码
        """
        url=webqq3config.getURL('check_code')
        txdata=urllib.urlencode({"appid":"1003903","uin":uin})
        try:
            req=urllib2.Request( url % txdata)
            req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
            req.add_header('Connection', 'Keep-Alive')
            req.add_header('Referer',webqq3config.getHeader('refer_ui_ptlogin2_qq_com_login') )
            
            handle=urllib2.urlopen(req)
            result=handle.read()
            rcode=result[14:15]
            if rcode=='1':  #需要图片验证码
                handle.needImg=True
                code=result[18:55]
                return '1', code
            else:
                code=result[18:22]
                return '0',code
        except IOError, e:
            print e
            
        
        
###################################################################
#好友相关协议
def getFriendInfo(uin):
    """
    获取好友信息
    """
    url=webqq3config.getURL('friend_information')
    txdata=urllib.urlencode({"verifysession":"",
                             "code":"",
                             "tuin":uin,
                             "vfwebqq":SimpleCookieHandler.cookies.get("vfwebqq"),
                             "t":int(time.time())})
    try:
        req=urllib2.Request( url % txdata)
        req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
        req.add_header('Connection', 'Keep-Alive')
        req.add_header('Referer',webqq3config.getHeader('refer_s_web2_qq_com_proxy') )
        
        handle=urllib2.urlopen(req)
        result=handle.read()
            
        jresult=json.loads(result)
        return jresult
    except IOError, e:
        print e
        

###################################################################
def getFriendList():
    """
    获取好友列表
    """
    url=webqq3config.getURL('friend_list')
    txdata=urllib.urlencode({"h": "hello",
                             "vfwebqq":SimpleCookieHandler.cookies.get("vfwebqq")})
    try:
        req=urllib2.Request( url, txdata)
        req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
        req.add_header('Connection', 'Keep-Alive')
        req.add_header('Referer',webqq3config.getHeader('refer_d_web2_qq_com_proxy') )
        
        handle=urllib2.urlopen(req)
        
        result=handle.read()
            
        jresult=json.loads(result)
        return jresult
    except IOError, e:
        print e

###################################################################
def getOnlineFriends():
    """
    获取在线好友
    """
    url=webqq3config.getURL('oline_friends')
    txdata=urllib.urlencode({"clientid":SimpleCookieHandler.cookies.get("clientid"),
                             "psessionid":SimpleCookieHandler.cookies.get("psessionid"),
                             "t":int(time.time())
                        })
    try:
        req=urllib2.Request( url%txdata)
        req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
        req.add_header('Connection', 'Keep-Alive')
        req.add_header('Referer',webqq3config.getHeader('refer_d_web2_qq_com_proxy') )
        
        handle=urllib2.urlopen(req)
        
        result=handle.read()
            
        jresult=json.loads(result)
        return jresult
    except IOError, e:
        print e
###################################################################
def getQunList():
    """
    获取群列表
    """
    url=webqq3config.getURL('group_list')
    
    
    import json
    pyobj={"vfwebqq":SimpleCookieHandler.cookies.get("vfwebqq"),
           }
    
    jsonstr=json.dumps(pyobj,separators=(',',':'))
        
        
    
    txdata=urllib.urlencode({"r":jsonstr,})
    try:
        req=urllib2.Request( url, txdata)
        req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
        req.add_header('Connection', 'Keep-Alive')
        req.add_header('Referer',webqq3config.getHeader('refer_d_web2_qq_com_proxy') )
        
        handle=urllib2.urlopen(req)
        
        result=handle.read()
            
        jresult=json.loads(result)
        return jresult
    except IOError, e:
        print e
        
###################################################################
def getSingleLongNick(uin):
    """
    获取好友签名
    """
    url=webqq3config.getURL('friend_long_nick')
    txdata=urllib.urlencode({"tuin":uin,
                             "vfwebqq":SimpleCookieHandler.cookies.get("vfwebqq"),
                             "t":int(time.time())})
    
    def doit():
        try:
            req=urllib2.Request( url%txdata)
            req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
            req.add_header('Connection', 'Keep-Alive')
            req.add_header('Referer',webqq3config.getHeader('refer_s_web2_qq_com_proxy') )
            
            handle=urllib2.urlopen(req)
            
            result=handle.read()
            jresult=json.loads(result)
            
            #while jresult.get("retcode")!=0:
            #    doit()
            return jresult
        except IOError, e:
            print e
            doit()
    
    return doit()

###################################################################
def getQunMemo(gcodes):
    """
    获取群公告
    """
    url=webqq3config.getURL('group_info')
    
    import json
    jsonstr=json.dumps(gcodes,separators=(',',':'))
    
    txdata=urllib.urlencode({"gcode":jsonstr,
                             "retainKey":"memo,gcode",
                             "vfwebqq":SimpleCookieHandler.cookies.get("vfwebqq")})
    
    def doit():
        try:
            req=urllib2.Request( url%txdata)
            req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
            req.add_header('Connection', 'Keep-Alive')
            req.add_header('Referer',webqq3config.getHeader('refer_s_web2_qq_com_proxy') )
            
            handle=urllib2.urlopen(req)
            
            result=handle.read()
            jresult=json.loads(result)
            
            #while jresult.get("retcode")!=0:
            #    doit()
            return jresult
        except IOError, e:
            print e
            doit()
    
    return doit()
###################################################################
import tempfile,random
tempPath=tempfile.gettempdir()+"/"
def getFace(uin,faceType):
    """
    获取头像
    """
    url=webqq3config.getURL('get_face_url')
    txdata=urllib.urlencode({"cache":"0",
                             "fid":"0",
                             "type":faceType,
                             "uin":uin,
                             "vfwebqq":SimpleCookieHandler.cookies.get("vfwebqq")})
    try:
        num=random.randint(1,10)
        req=urllib2.Request( url%(num,txdata))
        req.add_header('User-Agent', webqq3config.getHeader('user-agent'))
        req.add_header('Connection', 'Keep-Alive')
        req.add_header('Referer',webqq3config.getHeader('refer_web3_qq_com') )
        
        handle=urllib2.urlopen(req)
        itype=handle.info().getheader('Content-Type')
        if itype.find("image") ==-1:
            return False
        else:
            fpath=tempPath+str(uin)
            tempFile = file(fpath,'w')
            tempFile.write(handle.read())
            tempFile.close()
            return fpath
        
    except IOError, e:
        print e       
 
###################################################################

       
###################################################################
if __name__=="__main__":
     
    class Parser:
        def handleCheckCode(self, handle):
            if handle is not None:
                print handle.read()
            else:
                print "handle is None"
    
    a=Login()
    a.loginChannel('232', "份额份额")
