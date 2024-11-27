import os
import llmClient
import fileAccess

from typing import List
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
new_path = os.getenv('NEWPATH')

# Add a global variable to store the progress
progress = 0
file_list = []


def convert_run(client=llmClient.init()):
    taskName = "convert Go file to support MongoDB to replace MySQL support"
    filepath = "/root/go/src/device-manager/legacy/model"
    genpath = "/tmp"
    files = fileAccess.list_files(filepath)
    for file in files:
        if not file.lower().endswith('.go'):
            continue
        prompts = "The file was created by goctl to support MySQL access, now we need to refactoring the file to support MongoDB"
        filename = file
        fullfilepath = filepath + "/" + filename
        genfile = genpath + "/" + filename
        filecontent = fileAccess.load_file(fullfilepath)

        prompts = prompts + ":" + filecontent
        response = llmClient.execute_prompt(prompts, taskName, client)
        processedResponse = llmClient.process_llm_response(response)
        print(f"write file:\n{file}")
        fileAccess.output_content(genfile, processedResponse)


def generate_new_code(path, prompt):
    """使用LLM模型和Prompt改写指定文件夹下的所有Go代码文件"""
    global progress
    # Reset the progress
    progress = 0
    # Get the total number of files
    # total_files = len(os.listdir(path))
    # Get the total number of Go files
    go_files = [f for f in os.listdir(path) if f.endswith('.go')]
    total_files = len(go_files)

    taskName = "convert Go file to support MongoDB to replace MySQL support"
    print(f"start to convert {total_files} files")

    # 新输出code的文件夹目录（在原文件目录下增加一个新文件夹）
    new_path_dir = path + "/" + new_path
    print(f"new_path_dir: {new_path_dir}")
    if not os.path.exists(new_path_dir):
        os.makedirs(new_path_dir)

    # 指定Prompt.txt的路径
    # prompt_file = "./prompts/prompt.txt"
    client = llmClient.init()
    # 读取Prompt
    # with open(prompt_file, "r") as file:
    #    prompts = file.read().strip()
    prompts = prompt

    print(f"prompts: {prompts}")
    for i, filename in enumerate(os.listdir(path)):
        if filename.endswith(".go"):
            file_list.append({"name": filename, "status": "Processing"})
            # prompts = "The file was created by goctl to support MySQL access, now we need to refactoring the file to support MongoDB"
            fullfilepath = path + "/" + filename
            genfile = new_path_dir + "/" + filename
            filecontent = fileAccess.load_file(fullfilepath)

            prompts = prompts + ":" + filecontent
            print(f"start to convert:\n{progress}")
            response = llmClient.execute_prompt(prompts, taskName, client)
            processedResponse = llmClient.process_llm_response(response)
            # print(f"write file:\n{file}")
            fileAccess.output_content(genfile, processedResponse)
            progress = (i + 1) / total_files
            print(f"current progress: {progress}")
            # update the file list
            for file in file_list:
                if file["name"] == filename:
                    file["status"] = "Processed"
                    break
