# -*- coding: utf-8 -*-

from hashlib import md5

class MD5:
    def init__(self):
        pass
    def md5(self,str):
        """
        整个加密
        """
        return md5(str).hexdigest().upper()

    def md5_3(self,str):
        """
        三遍md5
        """
        return md5(md5(md5(str).digest()).digest()).hexdigest().upper()
    
if __name__=='__main__':
    md51=MD5()
    p='4568525153hangxin'
    v='hang'
    print p,v
    print 'md5  ',md51.md5(p)
    print 'md5_3',md51.md5_3(p)
    print 'f:   ',md51.md5(md51.md5_3(p)+v.upper())