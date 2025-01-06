import math
import random
from datetime import datetime, timedelta
from tools.LLM.run_gpt_prompt import *
import numpy as np
from sklearn.cluster import DBSCAN



# 简易实现基础版本

# 小镇基本设施地图
MAP =     [['医院', '咖啡店', '#', '蜜雪冰城', '学校', '#', '#', '小芳家', '#', '#', '火锅店', '#', '#'],
          ['#', '#', '绿道', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', '#', '#', '#', '#', '#', '小明家', '#', '小王家', '#', '#', '#', '#'],
          ['#', '#', '肯德基', '乡村基', '#', '#', '#', '#', '#', '#', '#', '健身房', '#'],
          ['电影院', '#', '#', '#', '#', '商场', '#', '#', '#', '#', '#', '#', '#'],
          ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
          ['#', '#', '#', '#', '#', '#', '#', '海边', '#', '#', '#', '#', '#']]

can_go_place = ['医院','咖啡店','蜜雪冰城', '学校','小芳家', '火锅店','绿道','小明家', '小王家','肯德基', '乡村基', '健身房','电影院', '商场','海边' ]

# TODO 暂时不考虑环境周围物品
objs = {
    "医院" : ["药","医生"],
    "咖啡店" : ["咖啡机","猫","咖啡","凳子"],
}

# 世界的规则
# TODO 暂时只考虑学校上学的时间，配合苏醒时间
world_rule = ""

# 角色
agents_name =  ["小明","小王","小芳"]

class agent_v:
    def __init__(self,name,MAP):
        self.name = name
        self.MAP = MAP
        self.schedule = []
        self.Visual_Range = 1
        self.home = ""
        self.curr_place  = ""
        self.position = (0,0)
        self.schedule_time = []
        self.last_action = ""
        self.memory = ""
        self.wake = ""
        self.curr_action = ""
        self.curr_action_pronunciatio  = ""
        self.ziliao = open(f"./agents/{self.name}/1.txt",encoding="utf-8").readlines()

    def getpositon(self):
        return self.position


    def goto_scene(self,scene_name):
        for row_index, row in enumerate(self.MAP):
            for col_index, cell in enumerate(row):
                if cell == scene_name:
                    self.position = (row_index,col_index)
                    self.curr_place =  scene_name
        return None  # 如果没有找到，返回 None

    def Is_nearby(self,position):
        x1=self.position[0]
        x2=position[0]
        y1=self.position[1]
        y2=position[1]
        manhattan_distance = abs(x1 - x2) + abs(y1 - y2)
        # 计算欧几里得距离
        euclidean_distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        # 判断是否相邻
        return manhattan_distance == 1 or euclidean_distance == 1 or euclidean_distance == math.sqrt(2)



# DBSCAN聚类方式感知聊天
def DBSCAN_chat(agents):
    result = []
    points_list =  []
    agent_list = []
    for agent in agents:
        points_list.append(agent.getpositon())
        agent_list.append(agent)
    points_array = np.array(points_list)
    dbscan = DBSCAN(eps=1.5, min_samples=1)
    labels = dbscan.fit_predict(points_array)

    for point, label,agent in zip(points_list, labels,agent_list):
        # print(f"Point {point} belongs to cluster {label}")
        index  = int(label)
        if index >= len(result):
            result.extend([[] for _ in range(index - len(result) + 1)])
        result[index] += [(point,agent)]
        # 筛选至少两个元素的聚类
    filtered_clusters = [cluster for cluster in result if len(cluster) >= 2]
    # 如果没有符合条件的聚类，返回 None
    if not filtered_clusters:
        return None
    if random.random() < 0.5:
        selected_cluster = random.choice(filtered_clusters)
        return [i[1] for i in selected_cluster]
    else:
        return None



# memory记忆 TODO 暂时考虑使用永久记忆，不设置遗忘曲线
'''
    记录：
        聊天的总结
        每天的工作计划
        这几天有什么重要的事情
'''

# 时间
START_TIME =  "2024-11-16-06-30"
# 每个step是十分钟
min_per_step  = 10
# 计算时间的表示的函数
def get_now_time(oldtime,step_num):
    def format_time(dt):
        return dt.strftime("%Y-%m-%d-%H-%M")
    def calculate_new_time(oldtime, step_num):
        # 将字符串转换为 datetime 对象
        start_time = datetime.strptime(oldtime, "%Y-%m-%d-%H-%M")
        # 计算新的时间
        new_time = start_time + timedelta(minutes=min_per_step * step_num)
        # 将新的时间格式化为字符串
        return format_time(new_time)
    return calculate_new_time(oldtime, step_num)

# 获取时间对于的星期
def get_weekday(nowtime):
    date_format = '%Y-%m-%d-%H-%M'
    dt = datetime.strptime(nowtime, date_format)
    # 获取星期几，0表示星期一，6表示星期日
    weekday = dt.weekday()
    # 定义星期几的名称
    days_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]
    return days_of_week[weekday]

# 时间转为2024年11月16日早上06点30分格式
def format_date_time(date_str):
    # 定义输入日期时间的格式
    input_format = '%Y-%m-%d-%H-%M'

    # 解析日期时间字符串
    dt = datetime.strptime(date_str, input_format)

    # 定义输出日期时间的格式
    output_format = '%Y年%m月%d日%H点%M分'

    # 格式化日期时间字符串
    formatted_date = dt.strftime(output_format)

    return formatted_date

# 比较两个时间谁更早
def compare_times(time_str1, time_str2, time_format="%H-%M"):
    """
    比较两个时间字符串，返回哪个时间更早。

    :param time_str1: 第一个时间字符串
    :param time_str2: 第二个时间字符串
    :param time_format: 时间字符串的格式，默认为 "%Y-%m-%d-%H-%M"
    :return: 返回一个字符串，表示哪个时间更早，或者是否相等
    """
    # 解析时间字符串为 datetime 对象
    time1 = datetime.strptime(time_str1, time_format)
    time2 = datetime.strptime(time_str2, time_format)

    # 比较两个时间
    if time1 < time2:
        return True
    elif time1 > time2:
        return False
    else:
        return True




# 日程安排转为开始时间
#  TODO 时间有问题，睡觉时间,传入参数[1:]即可解决
def update_schedule(wake_up_time_str, schedule):
    # 将字符串格式的时间转换为datetime对象
    wake_up_time = datetime.strptime(wake_up_time_str, '%H-%M')

    # 初始化当前时间为醒来时间
    current_time = wake_up_time

    # 创建一个新的列表来存储更新后的日程安排
    updated_schedule = []

    for activity, duration in schedule:
        updated_schedule.append([activity, current_time.strftime('%H-%M')])
        current_time += timedelta(minutes=duration)

    return updated_schedule

# 确定当前时间agent开展的活动
def find_current_activity(current_time_str, schedule):
    # 将当前时间字符串转换为datetime对象
    current_time = datetime.strptime(current_time_str, '%H-%M')

    # 遍历日程安排列表，找到当前时间对应的日程安排项
    for i, (activity, time_str) in enumerate(schedule):
        time_str = time_str.replace(':', '-')
        # 将日程安排的时间字符串转换为datetime对象
        activity_time = datetime.strptime(time_str, '%H-%M')

        # 如果当前时间小于等于当前日程安排的时间，则返回当前日程安排项
        if current_time <= activity_time:
            return [activity, time_str]

    # 如果当前时间大于所有日程安排的时间，返回最后一个日程安排项
    return ['睡觉','00-00']

if __name__ == '__main__':
    agent1 =  agent_v("小明",MAP)
    agent2 =  agent_v("小芳",MAP)
    agent3 =  agent_v("小王",MAP)
    agent1.home =  "小明家"
    agent2.home =  "小芳家"
    agent3.home =  "小王家"
    agents   =  [agent1,agent2,agent3]
    agent1.goto_scene("小明家")
    agent2.goto_scene("小芳家")
    agent3.goto_scene("小王家")
    # result  =  DBSCAN_chat(agents)

    # TODO 不考虑用户输入的变量类型
    steps = int(input("欢迎来到F小镇,请输入执行的step的次数:"))
    min_per_step = int(input("请设置每步step对于的分钟数:"))
    step = 0
    now_time = START_TIME

    while True:
        if  step >= steps:
            print("已到最大执行步数，结束")
            break
        if step%int((1440/min_per_step)) == 0:
            weekday_1 = get_weekday(START_TIME)
            format_time  = format_date_time(START_TIME)
            print(f'当前时间：{format_time}({weekday_1})')
            # 获取每日计划
            for i in agents:
                # 获取角色坐标
                agent1.goto_scene("小明家")
                agent2.goto_scene("小芳家")
                agent3.goto_scene("小王家")

                # print(i.name)
                i.schedule = run_gpt_prompt_generate_hourly_schedule(i.ziliao,now_time[:10])
                # 获取苏醒时间
                i.wake = run_gpt_prompt_wake_up_hour(i.ziliao,now_time,i.schedule)
                i.schedule_time =  update_schedule(i.wake, i.schedule[1:])
                i.curr_action = "睡觉"
                i.last_action = "睡觉"
                print(f'{i.name}当前活动:{i.curr_action}(😴💤🛌)---所在地点({i.home})')



        else:
            weekday_2 = get_weekday(now_time)
            format_time = format_date_time(now_time)
            print(f'当前时间：{format_time}({weekday_2})')
            # 根据时间执行计划
                # 判断是否苏醒，是否还在睡
            for i in agents:
                # print(now_time[-5:])
                # True 左比右早
                if compare_times(now_time[-5:],i.wake):
                    # 睡 把角色行动加入数组准备打印
                    # 还没醒
                    i.curr_action = "睡觉"
                    i.last_action = "睡觉"
                    i.curr_place = i.home
                    print(f'{i.name}当前活动:{i.curr_action}(😴💤🛌)---所在地点({i.curr_place})')


                else:
                    # 没睡 按计划行动 加入数组准备打印
                    # 计算角色执行计划地点坐标，修改当前角色坐标
                    i.curr_action=find_current_activity(now_time[-5:],i.schedule_time)[0]
                    if i.last_action != i.curr_action:
                        i.curr_action_pronunciatio =  run_gpt_prompt_pronunciatio(i.curr_action)
                        i.last_action = i.curr_action
                        i.curr_place = go_map(i.name, i.home, i.curr_place, can_go_place, i.curr_action)
                        i.goto_scene(i.curr_place)
                        print(
                            f'{i.name}当前活动:{i.curr_action}({i.curr_action_pronunciatio})---所在地点({i.curr_place})')

                    else:
                        print(
                            f'{i.name}当前活动:{i.curr_action}({i.curr_action_pronunciatio})---所在地点({i.curr_place})')

            # 感知周围其他角色决策行动
                # 主视角查看全地图，获取角色坐标
                    # 触发聊天
                        # 反思聊天变成记忆存储
                    # 行动完成
            chat_part = DBSCAN_chat(agents)
            if chat_part is None:
                pass
            else:
                print(f'{chat_part[0].name}和{chat_part[1].name}在{chat_part[1].curr_place}相遇,他们在进行聊天')
                chat_part[0].curr_action =  "聊天"
                chat_part[1].curr_action = "聊天"

                if chat_part[0].curr_place == chat_part[1].curr_place:
                    print(
                        f'{chat_part[0].name}当前活动:{chat_part[0].curr_action}---所在地点({chat_part[0].curr_place}旁)')
                    print(
                        f'{chat_part[1].name}当前活动:{chat_part[1].curr_action}---所在地点({chat_part[0].curr_place}旁)')
                else:
                    print(
                        f'{chat_part[0].name}当前活动:{chat_part[0].curr_action}---所在地点({chat_part[0].curr_place}和{chat_part[1].curr_place}旁)')
                    print(
                        f'{chat_part[1].name}当前活动:{chat_part[1].curr_action}---所在地点({chat_part[0].curr_place}和{chat_part[1].curr_place}旁)')
                chat_result  = double_agents_chat(
                    chat_part[0].curr_place,
                    chat_part[0].name,
                    chat_part[1].name,
                    f"{chat_part[0].name}正在{chat_part[0].curr_action},{chat_part[1].name}正在{chat_part[1].curr_action}",
                    chat_part[0].memory,
                    chat_part[1].memory,
                    f'{now_time[:10]}-{weekday_2}')
                print(f'聊天内容:{chat_result}')
                chat_part[0].memory = chat_result
                chat_part[1].memory = chat_result


        step += 1
        now_time = get_now_time(now_time,1)
        print(f'-'*150)

