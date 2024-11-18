"""
Author: 谢凯军

File: ollama_structure.py
Description: 根据相关任务分配相关提示词与对LLM输出的结果进行提取与处理
"""
import sys
sys.path.append('../')
from ollama_agent import *





# 两个智能体间的对话-test
def double_agents_chat(maze,persona,target_persona,curr_context,init_summ_idea,target_summ_idea):
    agent1_name = persona
    agent2_name = target_persona
    generate_prompt1 = OllamaAgent.generate_prompt(
        [agent1_name, agent2_name, curr_context, init_summ_idea, target_summ_idea], "./prompt_template/test.txt")

    example_output = '[["丹尼", "你好"], ["苏克", "你也是"] ... ]'
    special_instruction = '输出应该是一个列表类型，其中内部列表的形式为[“<名字>”，“<话语>”]。'
    repeat = 1
    x = ollama_agent.ollama_safe_generate_response(generate_prompt1, example_output, special_instruction, repeat=1)
    print(json.loads(x)['response'])


#



if __name__ == '__main__':
    # TODO 此处应该把url放配置文件
    api_url = "http://127.0.0.1:11434/api"
    ollama_agent = OllamaAgent("qwen2.5:14b", api_url, "agent_chat")
    agent1_memory = '丹尼这几天在学校，但是听说妈妈和父亲要去旅游，今天丹尼才放假回家见到父母'
    agent2_memory = '苏克老婆天天加班心情很不好，所以苏克和老婆商量去上海旅游三天，这几天苏克也天天加班，还没和孩子说这事情，今天回家也一直在厨房做饭，刚看到丹尼走进厨房'
    double_agents_chat('丹尼家的厨房','丹尼','jack','',agent1_memory,agent2_memory)