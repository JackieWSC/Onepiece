import requests
import hashlib

nike_link = "https://www.nike.com.hk/product/fair/bBV9a4pf.htm?pdpRecommend=false&preSkuCode="

res = requests.get(nike_link)
# res.text
# res.content

if "Air Jordan 6 Retro" in res.text:
    print("Found")


filename = "aj6_3.html"

with open(filename, 'wb') as fd:
    for chunk in res.iter_content(1024):
        fd.write(chunk)


nike_sha1 = hashlib.sha1(res.content)
print(nike_sha1.hexdigest())
