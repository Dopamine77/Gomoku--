
#import urllib.request
#f = urllib.request.urlopen("http://202.207.12.156:9017/step_04")
#print(f.read())
'''小学期第二节
import requests as re
prama = {
	'name' : 'yangrui',
	'student_number' : '0201121533'

}
url = 'http://202.207.12.156:9017/step_02'
getHml = re.get(url , params = prama)

print(getHml.text)

任务四：
import requests as re
import time
def fastModular(x): #快速幂的实现
	"""x[0] = base """
	"""x[1] = power"""
	"""x[2] = modulus"""
	result = 1
	while(x[1] > 0):
		if(x[1] & 1): # 位运算加快判断奇偶
			result = result * x[0] % x[2]
		x[1] = int(x[1]/2)
		x[0] = x[0] * x[0] % x[2]
	return result

answer = ''
getHtml = re.get("http://202.207.12.156:9017/step_04")

start = time.process_time()					# 运算时间戳
for i in eval(getHtml.json()['questions']): # 将带有'[]'符号的字符串转换成列表
	answer += str(fastModular(i)) + ','
end = time.process_time()					# 运算时间戳

param = {'ans':answer[:-1]}
print(f"Runing time is { end- start} sec")
getHtml = re.get("http://202.207.12.156:9017/step_04",params=param)
print(getHtml.text)
任务5：
import requests as re


def fastModular(x):  # 快速幂模实现 也就是加解密算法
	"""x[0] = base """
	"""x[1] = power"""
	"""x[2] = modulus"""
	result = 1
	while (x[1] > 0):
		if (x[1] & 1):
			result = result * x[0] % x[2]
		x[1] = int(x[1] / 2)  # 可用 x[1] >>= 2 位运算代替 更快
		x[0] = x[0] * x[0] % x[2]
	return result


def str_to_num(strings):
	"""将字符看作数字，以256进制的进位做加法"""
	"""返回一个十进制数字"""
	sum = 0
	lens = len(strings)
	for i in range(0, lens):
		sum += ord(strings[i]) * 256 ** (lens - i - 1)
	return sum


def num_to_str(num):
	messageList = []
	while num != 0:
		messageList.append(num % 256)
		num = num // 256  # 整数除符号 不能用 int(num // 256)
	messageList.reverse()  # 返回None　同时列表本身被倒置修改
	decodeString = ''
	for i in messageList:
		decodeString += chr(i)
	return decodeString


# 公钥
power = 65537
modulus = 135261828916791946705313569652794581721330948863485438876915508683244111694485850733278569559191167660149469895899348939039437830613284874764820878002628686548956779897196112828969255650312573935871059275664474562666268163936821302832645284397530568872432109324825205567091066297960733513602409443790146687029
password = '20060824yy,'
myHex = hex(fastModular([str_to_num(password), power, modulus]))  # 加密后的密码
print(f"My encryption code is {myHex}")

param = {
	'user': '20_YR_3',
	'password': myHex
}

getHtml = re.get('http://202.207.12.156:9017/step_05', params=param)

prefix = '0x'  # 16进制前缀 后面int()用到
# 服务器返回的16进制字符串没有前缀，加上前缀，将他转化为数字，这个数字是经过加密的
# 将得到的数字用公钥解密，得到字符串变为的数字，用逆方法解出
print(getHtml.json())
num = fastModular([int(prefix + getHtml.json()['message'], 16), power, modulus])
print(num_to_str(num))

#任务6：
import requests as re
def getIndex(coords):
	"""coords y x"""
	# 0行 [0]='.'		--- [14]='.'		[15]='\n'
	# 1行 [16]='.'		--- [30]='.'		[31]='\n'
	# 2行 [32]='.'		--- [46]='.'		[47]='\n'
	# 15行 [240]='.'	--- [254]='.'		[255]='\n'
	return int((ord(coords[0]) - ord('a'))*16 + (ord(coords[1]) - ord('a')))

getHtml = re.get("http://202.207.12.156:9017/step_06")

testOrder = getHtml.json()['questions']

board = ''              # 棋板
for i in range(0,15):
	board += '...............' + '\n'
step = 0 # 步数 用于判断黑白 黑方先走
answer = ''

for i in range(0, len(testOrder), 2): # i = 0 2 4 6 8 注意Python的左闭右开规则

	index = getIndex(testOrder[i:i+2])

	# Python不允许直接修改字符串 只能用拼接的方法
	if (step % 2) == 0:
		board = board[0: index] + 'x' + board[index + 1:]
	else:
		board = board[0: index] + 'o' + board[index + 1:]
	step += 1
	answer += board + ','

param = {
        'ans' : answer[:-1]
        }

getHtml = re.get('http://202.207.12.156:9017/step_06', params=param)
print(getHtml.text)

#任务7
import requests as re


def getIndex(coords):
	""" 将字符下标转换为数字下标"""
	"""coords y x"""
	# 0行 [0]='.'--- [14]='.'[15]='\n'
	# 1行 [16]='.'--- [30]='.'[31]='\n'
	# 2行 [32]='.'--- [46]='.'[47]='\n'
	# 15行 [240]='.'--- [254]='.'[255]='\n'
	return (ord(coords[0]) - ord('a')) * 16 + ord(coords[1]) - ord('a')


def getLine(coord, board):
	"""
    获得中心点的四周点情况 返回一个字符串列表
    coord[0] y 纵坐标 coord[1] x 控制横坐标
    board  棋局
    """
	line = ['', '', '', '']
	i = 0
	""" 核心思想就是 将周围点两个坐标x，y的限制 转化为一个位置index的限制 """
	while (i != 9):
		if ord(coord[1]) - ord('a') - 4 + i in range(0, 15):  # line[0]是横线 只需保证 横坐标在棋盘里就好
			line[0] += board[(ord(coord[0]) - ord('a')) * 16 + ord(coord[1]) - ord('a') - 4 + i]
		else:
			line[0] += ' '
		if ord(coord[0]) - ord('a') - 4 + i in range(0, 15):  # line[2]是竖线 只需保证 纵坐标在棋盘里就好
			line[2] += board[(ord(coord[0]) - ord('a') - 4 + i) * 16 + ord(coord[1]) - ord('a')]
		else:
			line[2] += ' '
		# - 4 + i 是从最小值上升判断  + 4 - i 是从最大值下降判断 两者没有什么不同 根据index的求法而定
		if ord(coord[1]) - ord('a') - 4 + i in range(0, 15) and ord(coord[0]) - ord('a') - 4 + i in range(0,
																										  15):  # line[1]是\线 保证 横纵坐标都在棋盘里就好
			line[1] += board[(ord(coord[0]) - ord('a') - 4 + i) * 16 + ord(coord[1]) - ord('a') - 4 + i]
		else:
			line[1] += ' '
		if ord(coord[1]) - ord('a') + 4 - i in range(0, 15) and ord(coord[0]) - ord('a') - 4 + i in range(0,
																										  15):  # line[3]是/线 保证 横纵坐标都在棋盘里就好
			line[3] += board[(ord(coord[0]) - ord('a') - 4 + i) * 16 + ord(coord[1]) - ord('a') + 4 - i]
		else:
			line[3] += ' '

		i += 1
	return line


getHtml = re.get("http://202.207.12.156:9017/step_07")

testOrder = getHtml.json()['board']  # 命令序列
coords = getHtml.json()['coord']  # 待计算四条线的点坐标集

board = ''  # 初始化棋板
for i in range(0, 15):
	board += '...............' + '\n'

step = 0  # 步数 用于判断黑白 黑方先走

answer = ''

for i in range(0, len(testOrder), 2):  # i = 0 2 4 6 8

	index = getIndex(testOrder[i:i + 2])

	# Python不允许直接修改字符串 只能用拼接的方法
	if (step % 2) == 0:
		board = board[0: index] + 'x' + board[index + 1:]
	else:
		board = board[0: index] + 'o' + board[index + 1:]
	step += 1
print(board)  # 展示根据命令序列生成的棋板

for coord in coords:  # 开始计算
	print(coord)
	print(getLine(coord, board))
	answer += ','.join(getLine(coord, board)) + ','

param = {
	'ans': answer[:-1]
}

getHtml = re.get('http://202.207.12.156:9017/step_07', params=param)
print(getHtml.text)

#任务8
import requests as re


def getIndexNum(coords):
    """ 将字符下标转换为数字下标"""
    """coords y x"""
    # 0行 [0]='.'--- [14]='.'[15]='\n'
    # 1行 [16]='.'--- [30]='.'[31]='\n'
    # 2行 [32]='.'--- [46]='.'[47]='\n'
    # 15行 [240]='.'--- [254]='.'[255]='\n'
    return (ord(coords[0]) - ord('a')) * 16 + ord(coords[1]) - ord('a')


def allIndexStr():
    """ 快速获取一个 以字符下标为值的列表 """
    """ spot[0]='aa' spot[1]='ab' ...."""
    spot = []
    for i in range(0, 15):
        for j in range(0, 16):
            spot.append(chr(i + 97) + chr(j + 97))
    return spot


def getLine(coord, board):
    """
    获得中心点的四周点情况 返回一个字符串列表
    coord[0] y 纵坐标 coord[1] x 控制横坐标
    board  棋局
    """
    line = ['', '', '', '']
    i = 0
    """ 核心思想就是 将周围点两个坐标x，y的限制 转化为一个位置index的限制 """
    while (i != 9):
        if ord(coord[1]) - ord('a') - 4 + i in range(0, 15):  # line[0]是横线 只需保证 横坐标在棋盘里就好
            line[0] += board[(ord(coord[0]) - ord('a')) * 16 + ord(coord[1]) - ord('a') - 4 + i]
        else:
            line[0] += ' '
        if ord(coord[0]) - ord('a') - 4 + i in range(0, 15):  # line[2]是竖线 只需保证 纵坐标在棋盘里就好
            line[2] += board[(ord(coord[0]) - ord('a') - 4 + i) * 16 + ord(coord[1]) - ord('a')]
        else:
            line[2] += ' '
        # - 4 + i 是从最小值上升判断  + 4 - i 是从最大值下降判断 两者没有什么不同 根据index的求法而定
        if ord(coord[1]) - ord('a') - 4 + i in range(0, 15) and ord(coord[0]) - ord('a') - 4 + i in range(0,
                                                                                                          15):  # line[1]是\线 保证 横纵坐标都在棋盘里就好
            line[1] += board[(ord(coord[0]) - ord('a') - 4 + i) * 16 + ord(coord[1]) - ord('a') - 4 + i]
        else:
            line[1] += ' '
        if ord(coord[1]) - ord('a') + 4 - i in range(0, 15) and ord(coord[0]) - ord('a') - 4 + i in range(0,
                                                                                                          15):  # line[3]是/线 保证 横纵坐标都在棋盘里就好
            line[3] += board[(ord(coord[0]) - ord('a') - 4 + i) * 16 + ord(coord[1]) - ord('a') + 4 - i]
        else:
            line[3] += ' '

        i += 1
    return line


def judge(testOrder):
    """ 服务器并没有给我们我们是 M 还是 O"""
    """ 根据棋局的命令序列判断"""
    if (len(testOrder) // 2) % 2 == 0:  # 我是黑方
        return 'MO'
    else:  # 我是白方
        return 'OM'


def RuleWithPoints():
    """ 返回一个 规则字典 对应规则和分值"""
    RWP = {
        ("CMMMM", "MCMMM", "MMCMM", "MMMCM", "MMMMC"): 10000,
        ("COOOO", "OOOOC"): 6000,
        (".CMMM.", ".MCMM.", ".MMCM.", ".MMMC."): 5000,
        ("COOO.", ".OOOC", ".OOCO.", ".OCOO."): 2500,
        ("OCMMM.", "OMCMM.", "OMMCM.", "OMMMC.", ".CMMMO", ".MCMMO", ".MMCMO", ".MMMCO"): 2000,
        (".MMC.", ".MCM.", ".CMM."): 400,
        (".OOC", "COO.", "MOOOC", "COOOM"): 400,
        (".MMCO", ".MCMO", ".CMMO", "OMMC.", "OMCM.", "OCMM.", "MOOC", "COOM"): 200,
        (".MC.", ".CM."): 50,
        ('.'): 20
    }
    return RWP


def getMaxCoords(Order, RWP, indexSrc):
    """对于每一个当下的棋局 返回一个最成功的下点"""

    board = ''  # 棋板
    for i in range(0, 15):
        board += '...............' + '\n'

    step = 0  # 步数 用于判断黑白 黑方先走
    BW = judge(Order)

    for i in range(0, len(Order), 2):  # i = 0 2 4 6 8

        index = getIndexNum(Order[i:i + 2])

        # Python不允许直接修改字符串 只能用拼接的方法
        if (step % 2) == 0:
            board = board[0: index] + BW[0] + board[index + 1:]
        else:
            board = board[0: index] + BW[1] + board[index + 1:]
        step += 1
    # print(board)

    maxCoord = ''
    maxPoints = 0
    for i in range(0, len(board)):
        if board[i] == '.':
            tempBoard = board[0: i] + 'C' + board[i + 1:]
            coord = indexSrc[i]
            lines4 = ','.join(getLine(coord, tempBoard))
            points = 0
            for rules, value in RWP.items():
                for rul in range(0, len(rules)):
                    if rules[rul] in lines4:
                        points += value * lines4.count(rules[rul])

            if points > maxPoints:
                maxPoints = points
                maxCoord = coord

    print(f"{maxCoord} {maxPoints}")
    return maxCoord


def getNextStep(url, answer):
    """提交答案 获取下一题链接"""
    param = {
        'ans': answer[:-1]
    }

    getHtml = re.get(url, params=param)
    print(getHtml.text)


url = "http://202.207.12.156:9017/step_08"
getHtml = re.get(url)

stepOrders = getHtml.json()['questions']

RWP = RuleWithPoints()
indexSrc = allIndexStr()

# answer = 'ki,he,ih,le,hg,ia,eh,gi,ci,hi,ke,kh,gl,gm,hi,kh,hj,'

answer = ''
for order in stepOrders:
    answer += getMaxCoords(order, RWP, indexSrc) + ','

getNextStep(url, answer)
'''
#任务9：
import requests as re
import time as t
def fastModular(x):
    """x[0] = base """
    """x[1] = power"""
    """x[2] = modulus"""
    result = 1
    while (x[1] > 0):
        if (x[1] & 1):
            result = result * x[0] % x[2]
        x[1] = int(x[1] / 2)
        x[0] = x[0] * x[0] % x[2]
    return result


def str_to_num(strings):
    sum = 0
    lens = len(strings)
    for i in range(0, lens):
        sum += ord(strings[i]) * 256 ** (lens - i - 1)
    return sum


def encodeLogin(password):
    # 公钥
    power = 65537
    modulus = 135261828916791946705313569652794581721330948863485438876915508683244111694485850733278569559191167660149469895899348939039437830613284874764820878002628686548956779897196112828969255650312573935871059275664474562666268163936821302832645284397530568872432109324825205567091066297960733513602409443790146687029

    return hex(fastModular([str_to_num(password), power, modulus]))


def join_game(user, myHexPass):
    """加入游戏并返回一个 get回复包对象"""

    url = 'http://202.207.12.156:9017/join_game'
    param = {
        'user': user,
        'password': myHexPass,
        'data_type': 'json'
    }

    getHtml = re.get(url, params=param)

    print(f"Open a new game{getHtml.text}")
    return getHtml


def check_game(game_id):
    url = 'http://202.207.12.156:9017/check_game/' + str(game_id)
    getState = re.get(url)
    # print(getState.text)    # 测试显示数据用
    return getState


def play_game(user, myHexPass, game_id, coord):
    url = 'http://202.207.12.156:9017/play_game/' + str(game_id)
    param = {
        'user': user,
        'password': myHexPass,
        'data_type': 'json',
        'coord': coord
    }
    re.get(url, params=param)


def getIndexNum(coords):
    """coords y x"""
    # 0行 [0]='.'--- [14]='.'[15]='\n'
    # 1行 [16]='.'--- [30]='.'[31]='\n'
    # 2行 [32]='.'--- [46]='.'[47]='\n'
    # 15行 [240]='.'--- [254]='.'[255]='\n'
    return (ord(coords[0]) - ord('a')) * 16 + ord(coords[1]) - ord('a')


def allIndexStr():
    spot = []
    for i in range(0, 15):
        for j in range(0, 16):
            spot.append(chr(i + 97) + chr(j + 97))
    return spot


def getLine(coord, board):
    """
    获得中心点的四周 15 点情况 返回一个字符串列表
    coord[0] y 纵坐标 coord[1] x 控制横坐标
    board  棋局
    """
    line = ['', '', '', '']
    i = 0
    """ 核心思想就是 将周围点两个坐标x，y的限制 转化为一个位置index的限制 """
    while (i != 15):
        if ord(coord[1]) - ord('a') - 7 + i in range(0, 15):  # line[0]是横线 只需保证 横坐标在棋盘里就好
            line[0] += board[(ord(coord[0]) - ord('a')) * 16 + ord(coord[1]) - ord('a') - 7 + i]
        else:
            line[0] += ' '
        if ord(coord[0]) - ord('a') - 7 + i in range(0, 15):  # line[2]是竖线 只需保证 纵坐标在棋盘里就好
            line[2] += board[(ord(coord[0]) - ord('a') - 7 + i) * 16 + ord(coord[1]) - ord('a')]
        else:
            line[2] += ' '
        # - 7 + i 是从最小值上升判断  + 7 - i 是从最大值下降判断 两者没有什么不同 根据index的求法而定
        if ord(coord[1]) - ord('a') - 7 + i in range(0, 15) and ord(coord[0]) - ord('a') - 7 + i in range(0,
                                                                                                          15):  # line[1]是\线 保证 横纵坐标都在棋盘里就好
            line[1] += board[(ord(coord[0]) - ord('a') - 7 + i) * 16 + ord(coord[1]) - ord('a') - 7 + i]
        else:
            line[1] += ' '
        if ord(coord[1]) - ord('a') + 7 - i in range(0, 15) and ord(coord[0]) - ord('a') - 7 + i in range(0,
                                                                                                          15):  # line[3]是/线 保证 横纵坐标都在棋盘里就好
            line[3] += board[(ord(coord[0]) - ord('a') - 7 + i) * 16 + ord(coord[1]) - ord('a') + 7 - i]
        else:
            line[3] += ' '

        i += 1
    return line


def judge(testOrder):
    if (len(testOrder) // 2) % 2 == 0:  # 我是黑方
        return 'MO'
    else:  # 我是白方
        return 'OM'


def RuleWithPoints():
    RWP = {
        ("CMMMM", "MCMMM", "MMCMM", "MMMCM", "MMMMC"): 10000,
        ("COOOO", "OCOOO", "OOCOO", "OOOCO", "OOOOC"): 6000,
        (".CMMM.", ".MCMM.", ".MMCM.", ".MMMC."): 5000,
        ("COOO.", ".OOOC", ".OOCO.", ".OCOO."): 2500,
        ("OCMMM.", "OMCMM.", "OMMCM.", "OMMMC.", ".CMMMO", ".MCMMO", ".MMCMO", ".MMMCO"): 2000,
        (".MMC.", ".MCM.", ".CMM."): 400,
        (".OOC", "COO.", "MOOOC", "COOOM"): 400,
        (".MMCO", ".MCMO", ".CMMO", "OMMC.", "OMCM.", "OCMM.", "MOOC", "COOM"): 200,
        (".MC.", ".CM."): 50,
        ('.'): 1
    }
    return RWP


def getMaxCoords(Order, RWP, indexSrc):
    """对于每一个当下的棋局 返回一个最成功的下点"""

    board = ''  # 棋板
    for i in range(0, 15):
        board += '...............' + '\n'

    step = 0  # 步数 用于判断黑白 黑方先走
    BW = judge(Order)

    for i in range(0, len(Order), 2):  # i = 0 2 4 6 8

        index = getIndexNum(Order[i:i + 2])

        # Python不允许直接修改字符串 只能用拼接的方法
        if (step % 2) == 0:
            board = board[0: index] + BW[0] + board[index + 1:]
        else:
            board = board[0: index] + BW[1] + board[index + 1:]
        step += 1
    print(board)  # 测试显示数据用

    maxCoord = ''
    maxPoints = 0
    for i in range(0, len(board)):
        if board[i] == '.':
            tempBoard = board[0: i] + 'C' + board[i + 1:]
            coord = indexSrc[i]
            lines4 = ','.join(getLine(coord, tempBoard))
            points = 0
            for rules, value in RWP.items():
                for rul in range(0, len(rules)):
                    if rules[rul] in lines4:
                        points += value * lines4.count(rules[rul])

            if points > maxPoints:
                maxPoints = points
                maxCoord = coord

    print(f"{maxCoord} {maxPoints}", end=' ')
    return maxCoord


user = '20_YR_3'
password = '20060824yy,'
myHexPass = encodeLogin(password)
RWP = RuleWithPoints()
indexSrc = allIndexStr()

game_id = join_game(user, myHexPass).json()["game_id"]
state = check_game(game_id).json()

print("Looking forgame partners ...")
while state['ready'] == "False":
    state = check_game(game_id).json()
    print(state['ready'], end=" ")
    t.sleep(5)

if state['creator'] != user:
    opponent = state['creator']
else:
    opponent = state['opponent_name']

while state['ready'] == "True":
    if state['current_turn'] == user:
        order = state['board']
        coord = getMaxCoords(order, RWP, indexSrc)
        play = play_game(user, myHexPass, game_id, coord)
        print(f"Playing {coord}")
    else:
        print(f"Waiting for {opponent} to play")

    t.sleep(5)
    state = check_game(game_id).json()

    if state['winner'] != "None":
        print(f"The winner is {state['winner']}")
        break


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
