import requests
from bs4 import BeautifulSoup
import re

login_url = "http://rs.xidian.edu.cn/member.php?mod=logging&action=login&loginsubmit=yes&" \
            "handlekey=login&loginhash=LO0ND&inajax=1"
url_init = "http://rs.xidian.edu.cn/home.php?mod=spacecp&ac=plugin&id=bt:history&page="

# pretend to be a browser
header = {
    "User-Agent": "Mozilla/5.0"
}

# your username and password
payload = {
    "username": "*****",           # your username
    "password": "*********"        # your password        
}

# set a session the post to login
session_requests = requests.session()
response = session_requests.post(login_url, data=payload)

# init len_res to get into the loop;when it comes to the last page
# after scrapy the len_res will become 0,then break the loop
len_res = 1
result = {}
time = {}
user = ""

# the first url is page=1
j = 1

while len_res:
    url = url_init + str(j)
    response = session_requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")

    #get user
    strong_tmp = str(soup.find(re.compile('strong')))
    user_tmp = re.findall(r'>[A-Za-z]*[\u4e00-\u9fa5]*[A-Za-z]*[\u4e00-\u9fa5]*</a', strong_tmp)
    user = user_tmp[0].split('>')[1].split('<')[0]
    
    # get the <tbody>
    t_body = str(soup.tbody)
    # print(t_body)

    # get kind of the resource you download
    res_tmp = re.findall(r'\"_blank\">\[[\u4e00-\u9fa5]*\]', t_body)
    res = []
    for i in res_tmp:
        res.append(i.split('[')[1].split(']')[0])
    # print(res)

    # get the time
    time_tmp = re.findall(r'<td>\d{4}-\d{1,2}', t_body)
    # print(time_tmp)
    ti = []
    for i in time_tmp:
        ti.append(i.split('>')[-1])
    # print(ti)

    # put it into the result dic;if exists,let the value +1
    for i in res:
        if result.get(i):
            result[i] += 1
        else:
            result[i] = 1

    # put it into the result dic;if exists,let the value +1
    for i in ti:
        if time.get(i):
            time[i] += 1
        else:
            time[i] = 1

    # reset parameter len_res and j
    len_res = len(res)
    j += 1

# print the results
print("user: "+user)

# sorted the downloaded
results = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
for i in results.keys():
    print(str(i)+": "+str(results[i]))

print("************************")

for i in time.keys():
    print(str(i)+": "+str(time[i]))

