import json
import os
import time
from openai import OpenAI
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append('../')

api_key = os.environ.get("API_KEY")


class DeepSeekAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )


    def temp_sleep(self,seconds=0.1):
        time.sleep(seconds)

    def ollama_safe_generate_response(self,prompt,example_output,special_instruction,repeat=3,func_validate=None, func_clean_up=None,fail_safe=None):
        prompt = '"""\n' + prompt + '\n"""\n'
        prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
        prompt += "Example output json\n"
        prompt += "```json\n"
        prompt += '{"output": "' + str(example_output) + '"}\n'
        prompt += "json"
        # print("prompt",prompt)
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

        completion = self.client.chat.completions.create(
            model="deepseek-chat",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'user', 'content': prompt}],
            temperature=1
        )
        response = completion.model_dump_json()
        # print(response,1)

        response = json.loads(response)['choices'][0]['message']['content']
        # print(response)
        # print(response, 2)
        x = {
            "model": "deepseek-chat",
            "response": f'{response}',
        }

        x_serialized = json.dumps(x, ensure_ascii=False)

        return x_serialized



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



