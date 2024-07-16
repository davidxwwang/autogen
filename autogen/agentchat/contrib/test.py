import re
s = '{\n    \'keyword\': \'SIDCfgList\',\n    \'reason\': \'Contains "SID" and closely related in meaning to the problem\',\n    \'similarity\': \'80%\'\n}'
# 使用正则表达式提取 keyword
match = re.search(r"'keyword': '([^']+)'", s)
if match:
    keyword = match.group(1)
    print(keyword)
else:
    print("No keyword found")