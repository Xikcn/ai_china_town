import os
import re
from tools.LLM.ollama_agent import *
import sys

# 修改当前工作目录
os.chdir('../')


api_url = "http://127.0.0.1:11434/api"
ollama_agent = OllamaAgent("qwen2.5:14b", api_url, "agent_chat")

    # agent1_name = '丹尼'
    # agent2_name = '苏克'
    #
    # positiuon = '厨房'
    # agent1_memory = '丹尼这几天在学校，但是听说妈妈和父亲要去旅游，今天丹尼才放假回家见到父母'
    # agent2_memory = '苏克老婆天天加班心情很不好，所以苏克和老婆商量去上海旅游三天，这几天苏克也天天加班，还没和孩子说这事情，今天回家也一直在厨房做饭，刚看到丹尼走进厨房'
    #
    # x = double_agents_chat(positiuon,agent1_name,agent2_name,'',agent1_memory,agent2_memory)
    #
    # print(x)
    # print(type(x))

can_go_place = ['医院', '咖啡店', '蜜雪冰城', '学校', '小芳家', '火锅店', '绿道', '小明家', '小王家', '肯德基',
                    '乡村基', '健身房', '电影院', '商场', '海边']


# 每日计划表
def run_gpt_prompt_generate_hourly_schedule(persona,now_time):
    def create_prompt_input(persona,
                            p_f_ds_hourly_org,
                            hour_str,
                            intermission2=None,
                            test_input=None):
        pass

    def __func_clean_up(gpt_response, prompt=""):

        cr = gpt_response
        return cr

    def __func_validate(gpt_response, prompt=""):
        try:
            gpt_response = gpt_response.replace("```","").split("json")[1][1:]
            gpt_response = json.loads(gpt_response.strip('\n'))['output']
            total_time = sum(item[1] for item in gpt_response)
            # print(total_time)
            if total_time > 1920:
                return False
            __func_clean_up(gpt_response, prompt="")
        except:
            return False
        return True



    generate_prompt = OllamaAgent.generate_prompt(
        [persona,now_time],
        r"./tools/LLM/prompt_template/生成日程安排时间表.txt")
    output = ollama_agent.ollama_safe_generate_response(generate_prompt, "", "你不需要调整，只需要给我输出一个最终的结果，我需要一个标准的数组格式", 3,
                                                        __func_validate, __func_clean_up)

    if "json" in output:
        output = output.replace("```", "").split("json")[1][1:]
        output = json.loads(output.strip('\n'))['output']
        return output

    else:
        # print(output)
        return output


# 每天苏醒时间
def run_gpt_prompt_wake_up_hour(persona,now_time,hourly_schedule):
    def __func_clean_up(gpt_response, prompt=""):
        cr = gpt_response
        return cr

    def __func_validate(gpt_response, prompt=""):
        try:
            if "output" in gpt_response:
                pattern = r'"output"\s*:\s*"([^"]+)"'
                match = re.search(pattern, gpt_response)
                output_value = match.group(1)
                __func_clean_up(output_value, prompt="")
            else:
                return False
        except:
            return False
        return True
    generate_prompt = OllamaAgent.generate_prompt(
        [persona,now_time,hourly_schedule],
        r"./tools/LLM/prompt_template/起床时间.txt")
    output = ollama_agent.ollama_safe_generate_response(generate_prompt, "",
                                                        "只需要给我输出一个最终的结果不需要给我其他任何信息，我需要一个标准的日期格式，比如：07-01（表示早上七点零一分起床）",
                                                        3,
                                                        __func_validate, __func_clean_up)
    pattern = r'"output"\s*:\s*"([^"]+)"'
    match = re.search(pattern, output)
    output = match.group(1)
    return output

# 行动转表情
def run_gpt_prompt_pronunciatio(Action_dec):
    def __chat_func_clean_up(gpt_response):  ############
        cr = gpt_response.strip()
        if len(cr) > 3:
            cr = cr[:3]
        return cr
    def __chat_func_validate(gpt_response):  ############
        try:
            gpt_response = json.loads(gpt_response)["output"]
            __chat_func_clean_up(gpt_response)
        except:
            return False
        return True
    example_output = "🛁🧖‍♀️"  ########
    special_instruction = "输出只包含表情符号"  ########
    generate_prompt = OllamaAgent.generate_prompt(
        [Action_dec],
        r"./tools/LLM/prompt_template/行为转为图标显示.txt")
    output = ollama_agent.ollama_safe_generate_response(generate_prompt, example_output, special_instruction, 7,__chat_func_validate,__chat_func_clean_up,'{"output":"🧘️"}')
    return json.loads(output)['output']


# 两个智能体间的对话-test
def double_agents_chat(maze,agent1_name,agent2_name,curr_context,init_summ_idea,target_summ_idea):
    def __chat_func_clean_up(gpt_response):  ############
        return gpt_response

    def __chat_func_validate(gpt_response):  ############
        try:
            __chat_func_clean_up(gpt_response)
        except:
            return False
        return True

    generate_prompt = OllamaAgent.generate_prompt(
        [maze,agent1_name, agent2_name, curr_context, init_summ_idea, target_summ_idea], r"./tools/LLM/prompt_template/聊天.txt")

    example_output = '[["丹尼", "你好"], ["苏克", "你也是"] ... ]'
    special_instruction = '输出应该是一个列表类型，其中内部列表的形式为[“<名字>”，“<话语>”]。'

    x = ollama_agent.ollama_safe_generate_response(generate_prompt, example_output, special_instruction, 3,__chat_func_validate,__chat_func_clean_up)

    return json.loads(x)['output']


# 判断做这件事情需要去哪个地方
def go_map(agent_name, home , curr_place, can_go, curr_task):
    def __chat_func_clean_up(gpt_response):  ############
        return gpt_response

    def __chat_func_validate(gpt_response):  ############
        try:
            if "output" in gpt_response:
                pattern = r'"output"\s*:\s*"([^"]+)"'
                match = re.search(pattern, gpt_response)
                output_value = match.group(1)
                __chat_func_clean_up(output_value)
            else:
                return False
        except:
            return False
        return True

    example_output = '海边'
    special_instruction = ''

    generate_prompt = OllamaAgent.generate_prompt(
        [agent_name,home , curr_place, can_go, curr_task],
        r"./tools/LLM/prompt_template/行动需要去的地方.txt")

    output = ollama_agent.ollama_safe_generate_response(generate_prompt, example_output, special_instruction, 3,__chat_func_validate,__chat_func_clean_up)
    pattern = r'"output"\s*:\s*"([^"]+)"'
    match = re.search(pattern, output)
    output = match.group(1)
    return output

# 总结今天的一切写入记忆文件
def tess():
    pass

if __name__ == '__main__':
    api_url = "http://127.0.0.1:11434/api"
    ollama_agent = OllamaAgent("qwen2.5:14b", api_url, "agent_chat")

    # agent1_name = '丹尼'
    # agent2_name = '苏克'
    #
    # positiuon = '厨房'
    # agent1_memory = '丹尼这几天在学校，但是听说妈妈和父亲要去旅游，今天丹尼才放假回家见到父母'
    # agent2_memory = '苏克老婆天天加班心情很不好，所以苏克和老婆商量去上海旅游三天，这几天苏克也天天加班，还没和孩子说这事情，今天回家也一直在厨房做饭，刚看到丹尼走进厨房'
    #
    # x = double_agents_chat(positiuon,agent1_name,agent2_name,'',agent1_memory,agent2_memory)
    #
    # print(x)
    # print(type(x))

    can_go_place = ['医院', '咖啡店', '蜜雪冰城', '学校', '小芳家', '火锅店', '绿道', '小明家', '小王家', '肯德基',
                    '乡村基', '健身房', '电影院', '商场', '海边']
    x = go_map('小明','小明家','学校',str(can_go_place),'吃午饭')
    print(x)
    print(type(x))
