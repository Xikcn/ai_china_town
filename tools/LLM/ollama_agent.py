import json
import time

import requests
import warnings



warnings.filterwarnings('ignore')
import sys
sys.path.append('../')

class OllamaAgent:
    def __init__(self, model,baseurl,user_id):
        self.model = model
        self.baseurl = baseurl
        self.user_id = user_id

    def temp_sleep(self,seconds=0.1):
        time.sleep(seconds)

    def ollama_safe_generate_response(self,prompt,example_output,special_instruction,repeat=3,func_validate=None, func_clean_up=None,fail_safe=None):
        prompt = '"""\n' + prompt + '\n"""\n'
        prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
        prompt += "Example output json:\n"
        prompt += '{"output": "' + str(example_output) + '"}'

        for i in range(repeat):
            # print(f"repeat:{i}")
            try:
                curr_gpt_response = self.ollama_request(prompt).strip()
                # print("ollama_safe_generate_response:---",curr_gpt_response)
                curr_gpt_response = json.loads(curr_gpt_response)['response']
                if func_validate(curr_gpt_response):
                    return curr_gpt_response
            except:
                continue
        return fail_safe


    def ollama_request(self,prompt):
        self.temp_sleep()
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        # 发送 POST 请求
        response = requests.post(self.baseurl+"/generate", json=data)
        # 检查响应状态码
        if response.status_code == 200:
            # 获取生成的文本
            generated_text = response
            return generated_text.text
        else:
            print(f"Error: {response.status_code}")
            print(response.text)


    @staticmethod
    def generate_prompt(curr_input, prompt_lib_file):
        """
        Takes in the current input (e.g. comment that you want to classifiy) and
        the path to a prompt file. The prompt file contains the raw str prompt that
        will be used, which contains the following substr: !<INPUT>! -- this
        function replaces this substr with the actual curr_input to produce the
        final promopt that will be sent to the GPT3 server.
        ARGS:
          curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                      INPUT, THIS CAN BE A LIST.)
          prompt_lib_file: the path to the promopt file.
        RETURNS:
          a str prompt that will be sent to OpenAI's GPT server.
        """
        if type(curr_input) == type("string"):
            curr_input = [curr_input]
        curr_input = [str(i) for i in curr_input]

        f = open(prompt_lib_file, "r",encoding="utf-8")
        prompt = f.read()
        f.close()
        for count, i in enumerate(curr_input):
            prompt = prompt.replace(f"!<INPUT {count}>!", i)
        if "<commentblockmarker>###</commentblockmarker>" in prompt:
            prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
        return prompt.strip()


if __name__ == '__main__':
    agent1_name = '丹尼'
    agent2_name = '苏克'
    guanxi = '父子'
    positiuon = '厨房'
    agent1_memory = '丹尼这几天在学校，但是听说妈妈和父亲要去旅游，今天丹尼才放假回家见到父母'
    agent2_memory = '苏克老婆天天加班心情很不好，所以苏克和老婆商量去上海旅游三天，这几天苏克也天天加班，还没和孩子说这事情，今天回家也一直在厨房做饭，刚看到丹尼走进厨房'


    generate_prompt1 = OllamaAgent.generate_prompt([agent1_name,agent2_name,guanxi,positiuon,agent1_memory,agent2_memory],"./prompt_template/test.txt")
    print(generate_prompt1)
    # API 服务的 URL
    api_url = "http://127.0.0.1:11434/api"

    agent_chat = OllamaAgent("qwen2.5",api_url,"agent_chat")

    example_output = '[["丹尼", "你好"], ["苏克", "你也是"] ... ]'
    special_instruction ='输出应该是一个列表类型，其中内部列表的形式为[“<名字>”，“<话语>”]。'
    repeat = 1
    x = agent_chat.ollama_safe_generate_response(generate_prompt1,example_output,special_instruction,repeat=1)
    print(x)

