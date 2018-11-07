import json
text = "{'name': 'text','value': ['今晚，随着 EA Access、Origin Access、Origin Access Premier 以及预购玩家已经可以提前体验《战地V》Beta 版本测试，DICE 顺势再次放出了一则官方介绍短片，详细展示了《战地V》中玩家可以体验到的单机/线上内容：']}".replace('\'','\"')
print(json.loads(text))