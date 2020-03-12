import sqlite3
import http.cookiejar
import requests
import scrapy.http.cookies

def get_then_set_cookies(scjar, ff_cookies):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies where baseDomain='coursera.org'")
    for item in cur.fetchall():
        c = http.cookiejar.Cookie(0, item[4], item[5], # 4 and 5 are name and value
                                  None, False,
                                  item[0], item[0].startswith('.'), item[0].startswith('.'),
                                  item[1], False,
                                  item[2],
                                  item[3], item[3] == "",
                                  None, None, {})

        print(c)
        scjar.set_cookie(c)  # same structure, should be able to use ... it is the same...



''' 
for scrapy the cookie is like this

we will need 
.domain
.path
.name
and cookie it self ( should with value)

def set_cookie(self, cookie):
    """Set a cookie, without checking whether or not it should be set."""
    c = self._cookies
    self._cookies_lock.acquire()
    try:
        if cookie.domain not in c: c[cookie.domain] = {}
        c2 = c[cookie.domain]
        if cookie.path not in c2: c2[cookie.path] = {}
        c3 = c2[cookie.path]
        c3[cookie.name] = cookie
    finally:
        self._cookies_lock.release()

....
and we see this... so..., is almost the same
                c = Cookie(0, name, value,
                           None, False,
                           domain, domain_specified, initial_dot,
                           path, False,
                           secure,
                           expires,
                           discard,
                           None,
                           None,
                           {})
'''
scjar = scrapy.http.cookies.CookieJar()

ff_cookie = '/Users/v/Library/Application Support/Firefox/Profiles/3nqq0lq0.default-1493908674951/cookies.sqlite'
get_then_set_cookies(scjar, ff_cookie) # read from firefox

# need to convert the cookie to the ones for scrapy, so no need complicated fields?
#s = requests.Session()
#s.cookies = cj

#response = s.get('https://www.coursera.org/?skipBrowseRedirect=true&skipRecommendationsRedirect=true&tab=current')
#print(response.text)
