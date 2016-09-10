import urllib.request
import urllib.parse
import re
import datetime
import sys

def cleanhtml(raw_html):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext.strip()


def get_tnum(tid):

    base_url = "https://twitter.com/" + tid
    request = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(request)

    flag = False
    for line in response:
        line = line.decode("utf-8")
        if flag:
            line = cleanhtml(line)
            t_num = int(line.replace(",", ""))
            return t_num
        if '<span class="ProfileNav-label">트윗</span>' in line:
            flag = True
    return -1


def update_csv(f_name, new_line):
    f = open(f_name, "a")
    f.write(new_line+"\n")
    f.close()

"""

t_upate.sh >
cd /home/(directory)
python3 tw_crawl.py @K @T
git add data.csv
git commit -m "updata data $(date +%Y%m%d)"
git push
echo "----------------------------"

crontab >
59 23 * * * /home/(directory)/t_update.sh >> /home/(directory)/crontab.log 2>&1

"""

if __name__ == "__main__":

    tid_list = sys.argv[1:]

    k_tnum = get_tnum(tid_list[0])
    t_tnum = get_tnum(tid_list[1])

    tday = datetime.date.today()

    k_line = ",".join([str(tday), str(k_tnum), "k"])
    t_line = ",".join([str(tday), str(t_tnum), "t"])

    update_csv("data.csv", k_line)
    update_csv("data.csv", t_line)
    print("update successfully completed: " + str(tday))
