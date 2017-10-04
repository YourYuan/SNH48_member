import pandas as pd
import requests
import urllib


def member_crawler(team_code):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding': 'gzip, deflate',
	'Content-Type': 'application/x-www-form-urlencoded; charset= utf-8',
	'Connection':"keep-alive",
	'Referer': 'http://www.snh48.com/member_details.html?sid=10001'
	}

    url = 'http://h5.snh48.com/resource/jsonp/members.php?gid=' + team_code +'&callback=get_members_success'

    req = urllib.request.Request('http://h5.snh48.com/resource/jsonp/members.php?gid=40&callback=get_members_success',headers=headers)

    res = urllib.request.urlopen(req)

    content = res.read().decode('utf-8')

	return content

def parse_data(content,team_name):

    name_pattern = re.compile('"sname":"(.*?)"')

    nickname_pattern = re.compile('"nickname":"(.*?)"')

    tname_pattern = re.compile('"tname":"(.*?)"')

    join_day_pattern = re.compile('"join_day":"(.*?)"')

    height_pattern = re.compile('"height":"(.*?)"')

    birthday_pattern = re.compile('"birth_day":"(.*?)"')

    star_pattern = re.compile('"star_sign_12":"(.*?)"')

    birth_place_pattern = re.compile('"birth_place":"(.*?)"')

    speciality_pattern = re.compile('"speciality":"(.*?)"')

    hobby_pattern = re.compile('"hobby":"(.*?)"')

    experience_pattern = re.compile('"experience":"(.*?)"')

    catch_phrase_pattern = re.compile('"catch_phrase":"(.*?)"')

    blood_pattern = re.compile('"blood_type":"(.*?)"')

    df = pd.DataFrame()

    df['姓名'] = re.findall(name_pattern,content)

    df['昵称'] = re.findall(nickname_pattern, content)

    df['队伍'] = re.findall(tname_pattern,content)

    df['加入时间'] = re.findall(join_day_pattern, content)

    df['身高'] = re.findall(height_pattern,content)

    df['生日'] = re.findall(birthday_pattern,content)

    df['星座'] = re.findall(star_pattern,content)

    df['出生地'] = re.findall(birth_place_pattern,content)

    df['特长'] = re.findall(speciality_pattern,content)

    df['爱好'] = re.findall(hobby_pattern,content)

    df['经历'] = re.findall(experience_pattern,content)

    df['catch_phrase'] = re.findall(catch_phrase_pattern,content)

    df['血型'] = re.findall(blood_pattern,content)

    write = pd.ExcelWriter('%s.xlsx'%(team_name))

    df.to_excel(write,'Sheet1')

    write.save()

	return df

def main():

    name = ['SNH48','BEJ48','GNZ48','SHY48']

    code = ['10','20','30','40']

    df = pd.DataFrame()

    for i in range(4):

        content = member_crawler(code[i])

        df_new = parse_data(content,name[i])

        pd.concat([df,df_new],ignore_index=True)


if __name__ == '__main__':

    main()
