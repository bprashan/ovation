import os
from openai import AzureOpenAI
import json
import re
import subprocess

azure_ci_retries_url = os.getenv("AZURE_CI_RETRIES_URL")
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"
azure_ci_retries_key = os.getenv("AZURE_CI_RETRIES_KEY")
api_version = "2024-12-01-preview"

# Set proxy details as environment variables
os.environ['http_proxy'] = 'http://proxy-chain.intel.com:911/'
os.environ['https_proxy'] = 'http://proxy-chain.intel.com:912/'
os.environ['no_proxy'] = "localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,intel.com,.openai.azure.com,10.*"


print(azure_ci_retries_url)
print(azure_ci_retries_key)

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=azure_ci_retries_url,
    api_key=azure_ci_retries_key,
)

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return str(e)

jenkins_console_output = read_file_content('jenkins_console_output.txt')

prompt = f"""
You are a helpful assistant.

Jenkins_console_output : {jenkins_console_output}

Analyze the Jenkins console output for system or platform issues such as missing dependencies, `ModuleNotFoundError`, or port-in-use errors, and generate Linux shell commands to resolve the issues.

# Instructions

- Carefully review the Jenkins console output provided.
- Identify errors such as:
  - Missing dependencies 
  - Python `ModuleNotFoundError`
  - Port-in-use errors
- Generate the appropriate Linux shell commands to resolve each issue. Ensure commands are safe to run and are tailored to the error in question.
- Focus on common fixes such as installing missing packages, killing processes that are using required ports, or setting up the appropriate environment.
  
# Output Format

Provide only the Linux shell command(s) to address the issues, separated by line breaks if multiple commands are necessary. Do not include any explanations or additional context—output only the commands. 

# Examples

**Input (Jenkins Console Output):**
```
ModuleNotFoundError: No module named 'requests'
```

**Output:**
```bash
pip install requests
```

---

**Input (Jenkins Console Output):**
```
Error: Port 8080 is already in use
```

**Output:**
```bash
sudo lsof -i :8080
sudo kill -9 <PID>
```

---

Ensure commands provided in the output are functional, minimally invasive, and align with the type of error encountered.

"""

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": prompt,
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=deployment
)

print(response.choices[0].message.content)

#Extract the automation script part using regular expressions with re.DOTALL
cmd = re.search(r'```bash(.*?)```', response.choices[0].message.content, re.DOTALL)
if cmd:
     cmd = cmd.group(1).strip()
else:
     cmd = ""


# Generate the bash script file with the extracted content if it exists
script_path = 'patch.sh'
if cmd:
    with open(script_path, 'w') as file:
          file.write("#!/bin/bash")
          file.write("\n")
          file.write(cmd)
    print("Automation script generated and saved to patch.sh")
else:
     print("No Automation script found in the file content.")

#Execute patch.py file
print("Executing patch.sh file")
if os.path.exists(script_path):
    # Run the script
    process = subprocess.Popen(['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end='')

    # Wait for the process to complete
    process.wait()

client.close()

