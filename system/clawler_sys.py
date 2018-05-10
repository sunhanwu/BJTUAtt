import sys_config
def login():
    user=sys_config.UserInfo()
    # user.username=input("请输入Facebook账号")

    pass

def clawler():
    print('正在爬取用户数据...')
    pass

def clawler_menu():
    print("1.临时爬取")
    print("2.展示已有数据")
    try:
        choice=input("")
        if choice == '1':
            login()
        if choice=='2':
            print("正在分析已有数据...")
            clawler()
            pass
    except Exception:
        print("输入有误！")
        pass



