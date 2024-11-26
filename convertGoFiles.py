import llmClient
import fileAccess

def run(client = llmClient.init()):
    taskName = "convert Go file to support MongoDB to replace MySQL support"
    filepath ="/root/go/src/device-manager/legacy/model"
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
        fileAccess.output_content(genfile,processedResponse)
run()
