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
        prompt += "Example output json\n"
        prompt += "```json\n"
        prompt += '{"output": "' + str(example_output) + '"}\n'
        prompt += "json"

        for i in range(repeat):
            # print(f"repeat:{i}")
            try:
                curr_gpt_response = self.ollama_request(prompt).strip()
                # print("ollama_safe_generate_response:---",curr_gpt_response)
                curr_gpt_response = json.loads(curr_gpt_response)['response']
                if func_validate(curr_gpt_response):
                    return curr_gpt_response
            except:
                pass
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
            generated_text = response.text
            return generated_text
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




