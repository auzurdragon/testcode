import pycurl
from io import StringIO

url = 'localhost:8020/test'

userinfo = {
    
}

c = pycurl.Curl()
b = StringIO()
c.setopt(pycurl.URL, url)
c.setopt(pycurl.WRITEFUNCTION, b.write)

c.perform()
