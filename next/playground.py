import cookielib
import requests
from lxml import html

__author__ = 'Scity'


# sample 1
def Sample1():
    jar = cookielib.CookieJar()
    login_url = 'http://www.fitbit.com/login'

    r = requests.get(login_url, cookies=jar)
    print "Status Code", r.status_code

    from lxml import etree
    p = etree.HTML(r.text)

# sample 2
def Sample2():
    payload ={
        "login":"window6132003@yahoo.com.hk",
        "password":"Window12337!",
        "authenticity_token":""
    }

    # get the authenticity_token
    session_requests = requests.session()
    login_url = "https://github.com/login"
    result = session_requests.get(login_url)

    tree = html.fromstring(result.text)
    payload["authenticity_token"] = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

    print "Action:Get"
    print "Result", result.ok
    print "Result Status", result.status_code
    print "Token", payload["authenticity_token"]
    print payload

    # return

    result = session_requests.post(
        login_url,
        data = payload,
        headers = dict(referer=login_url)
    )

    print "Action:Login"
    print "Result", result.ok
    print "Result Status", result.status_code

    # scrap link
    url = 'https://github.com/JackieWSC/'
    result = session_requests.get(
        url,
        headers = dict(referer=url)
    )

    print "Action:Access scrap link"
    print "Result", result.ok
    print "Result Status", result.status_code

    tree = html.fromstring(result.content)
    bucket_elems = tree.xpath("//span [@class='repo']")
    # print bucket_elems()

    bucket_names = [bucket.text for bucket in bucket_elems]
    print bucket_names


def Sample3():
    payload ={
        "login":"window6132003@yahoo.com.hk",
        "password":"Window12337!",
        "authenticity_token":""
    }

    # get the authenticity_token
    session_requests = requests.session()
    login_url = "https://github.com/login"
    result = session_requests.get(login_url)

    tree = html.fromstring(result.text)
    payload["authenticity_token"] = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

    print "Action:Get"
    print "Result", result.ok
    print "Result Status", result.status_code
    print "Token", payload["authenticity_token"]
    print payload

    # return
    result = session_requests.post(
        login_url,
        data = payload,
        headers = dict(referer=login_url)
    )

    print "Action:Login"
    print "Result", result.ok
    print "Result Status", result.status_code

    # scrap link
    url = 'https://github.com/settings/emails'
    result = session_requests.get(
        url,
        headers = dict(referer=url)
    )

    print "Action:Access scrap link"
    print "Result", result.ok
    print "Result Status", result.status_code

    tree = html.fromstring(result.content)
    bucket_elems = tree.xpath("//span [@class='css-truncate-target']/@title")
    pageTitle = tree.xpath("//title")

    print "Page Title:",pageTitle[0].text
    if len(bucket_elems) != 0 :
        print bucket_elems[0]

def Sample4():
    payload ={
        "login":"window6132003@yahoo.com.hk",
        "password":"Window12337!",
        "authenticity_token":"",
        "utf8":b'\x27\x13',
        "commit":"Sign+in"
    }

    # get the authenticity_token
    session_requests = requests.session()
    login_url = "https://github.com/login"
    jar = cookielib.CookieJar()
    result = session_requests.get(login_url, cookies=jar)

    # print result.text

    tree = html.fromstring(result.text)
    payload["authenticity_token"] = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

    print "Action:Get"
    print "Result", result.ok
    print "Result Status", result.status_code
    print "Token", payload["authenticity_token"]
    print payload

    # result = session_requests.post(
    #     "http://httpbin.org/post",
    #     cookies = jar,
    #     data = payload,
    #     headers = dict(referer=login_url))
    # print result.url
    # print result.text
    # print result.content

    result = session_requests.post(
        login_url,
        data = payload)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print "And you get an HTTPError:", e.message

    print result.url
    # tree = html.fromstring(result.content)
    # print tree

    # result.raise_for_status()
    print "Action:Login"
    print "Result", result.ok
    print "Result Status", result.status_code

    # scrap link
    url = 'https://github.com/settings/emails'
    result = session_requests.get(
        url,
        headers = dict(referer=url)
    )

    print "Action:Access scrap link"
    print "Result", result.ok
    print "Result Status", result.status_code

    tree = html.fromstring(result.content)
    bucket_elems = tree.xpath("//span [@class='css-truncate-target']/@title")
    pageTitle = tree.xpath("//title")

    print "Page Title:",pageTitle[0].text
    if len(bucket_elems) != 0 :
        print bucket_elems[0]

def Sample5():
    header = { 'User-Agent': 'Mozilla/5.0'
    }
    payload ={
        "username":"window6132003@yahoo.com.hk",
        "password":"Window12337!!!",
        "rememberMe":"false",
        "login":'Sign+in',
        #"hpts":'1460129667356',
        #"hptsh":'sT2vxqHm0up937dNAvHM0jQ3zh0=',
        "showSwitchService":'true',
        "targetUrl":'/Home.action',
        "_sourcePage":'b634QPyAP3biMUD9T65RG_YvRLZ-1eYO3fqfqRu0fynRL_1nukNa4gH1t86pc1SP',
        "__fp":'TbRYKNsgUZA3yWPvuidLz-TPR6I9Jhx8'
    }

    # get the authenticity_token
    session = requests.session()
    login_url = "https://www.evernote.com/Login.action?targetUrl=%2FHome.action"
    result = session.get(login_url)
    # did this for first to get the cookies from the page, stored them with next line:
    # cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    cookies = session.cookies

    print "Action:Get"
    print "Result", result.ok
    print "Result Status", result.status_code
    tree = html.fromstring(result.text)
    print "Page Title:", tree.xpath("//title")[0].text
    print cookies

    # found the value used in POST action
    payload["_sourcePage"] = list(set(tree.xpath("//input[@name='_sourcePage']/@value")))[0]
    payload["__fp"] = list(set(tree.xpath("//input[@name='__fp']/@value")))[0]
    script = list(set(tree.xpath("//script[@type]")))

    for i in script:
        text = str(i.text)
        startpos = text.find("hpts")
        if startpos != -1:
            # find hpts script
            for j in text.splitlines():
                if j.find("hptsh") != -1 :
                    hptsh = j.strip(";").split()[-1]
                    print hptsh
                    payload["hptsh"] = hptsh
                    continue
                elif j.find("hpts") != -1 :
                    hpts = j.strip(";").split()[-1]
                    print hpts
                    payload["hpts"] = hpts
                    continue


    print payload

    result = session.post(
        login_url,
        headers = dict(referer=login_url),
        data = payload,
        cookies = cookies)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print "And you get an HTTPError:", e.message

    print "Action:Login"
    print "Result", result.ok
    print "Result Status", result.status_code
    print "Result URL", result.url
    # print "Result Text", result.text
    tree = html.fromstring(result.content)
    print "Page Title:", tree.xpath("//title")[0].text


    # scrap link
    url = 'https://www.evernote.com/Settings.action'
    result = session.get(url, headers = dict(referer=url), cookies = cookies)

    print "Action: Access scrap link"
    print "Result", result.ok
    print "Result Status", result.status_code
    print "Result URL", result.url
    # print "Result Text", result.text
    tree = html.fromstring(result.content)
    print "Page Title:", tree.xpath("//title")[0].text

    bucket_elems = tree.xpath("//span [@class='qa-quota-remaining monthly-usage-value']")
    print bucket_elems

def PrintSessionResult(result):
    print "Action:Get"
    print "Result", result.ok
    print "Result Status", result.status_code
    # tree = html.fromstring(result.text)
    # print "Page Title:", tree.xpath("//title")[0].text


def Next():
    headers = {
        u'Host': u'hk.nextdirect.com',
        u'User-Agent': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0',
        u'Accept': u'application/json, text/javascript, */*; q=0.01',
        u'Accept-Language': u'en-US,en;q=0.5',
        u'Accept-Encoding': u'gzip, deflate',
        u'X-Requested-With': u'XMLHttpRequest',
        u'SynchronizerToken':u'3457aac837e5cd227a0eb0596dee81acf4016a5664441a87885a91889797face_nDSL/eBqi7dMJEB/J6XkuQ==',
        u'Referer': u'http://hk.nextdirect.com/zh/g57196s3',
        u'Connection': u'Keep-Alive'
    }

    print headers

    session = requests.session()
    login_url = "http://hk.nextdirect.com/zh/g57196s3"
    stock = "http://hk.nextdirect.com/zh/StockEnquiry?productIDs[]=109108&productIDs[]=126504&productIDs[]=384266"
    #result = session.get(stock,headers=headers)
    result = session.get(stock)

    PrintSessionResult(result)
    tree = html.fromstring(result.text)
    print result.text
    # bucket_elems = tree.xpath("//select[@id='PPRitemSize109108']/option[@id]/@rel")

# script = list(set(tree.xpath("//script[@type]")))
#     for i in bucket_elems:
#         print i,"end"



print "Playground"
Next()


# <ul class="dk_options_inner" role="main" aria-hidden="true">
#    <li class="">
#       <a data-dk-dropdown-value="">
#    </li>
#    <li class="10910810">
#    </li>
#    <li class="10910812">
#    </li>
#    <li class="10910814">
#    </li>
# </ul>
