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
Git Repository : https://github.com/bprashan/ovation.git

Analyze the Jenkins console output to identify code errors and syntax errors, use the provided Git repository as the source, and automate the process of creating a Python script to replace the old code with new code.

# Details

- You will analyze Jenkins console output logs to identify code and syntax errors.
- Use the provided Git repository as the source for identifying the lines of code that need changes.
- Write a Python automation script that replaces the old code in the repository with the corrected code.

# Steps
1. **Analyze the Console Output**:
   - Parse and identify any code or syntax errors from the Jenkins logs.
   - Determine file paths and specific lines where errors originate.

2. **Access Source Repository**:
   - Assume the source code is present in the current working directory.
   - refer to the provided Git repository to locate the files affected by the errors.

3. **Create Automation Python Script**:
   - The Python script should:
    - Identify the relevant file, line, or function based on the console output.
    - Apply the necessary changes to fix the errors.
    - The script should handle edge cases like missing files, indentation errors or already-applied patches.
    - Create a backup of the file before modifying it.

# Output Format

The output must contain the following:
1. **Python Automation Script**:
   - A fully functional Python script to automatically replace old code with corrected code, ensuring proper indentation.
   - The script should use Python libraries (like `os`, `fileinput`, `readlines` for replacements) and handle errors gracefully.
   - The script must avoid duplicating or repeating the same lines of code.
   - Maintain backups.
   - Ensure syntax correctness.

Python script must be directly provided in plain text and not wrapped in any additional formatting.

# Examples
### Python Script Example
```python
import os
import shutil

# Path to the file with the error
local_repo_path = os.path.join(os.getcwd())
file_path = os.path.join(local_repo_path, "test_module.py")
backup_path = file_path + ".bak"

# Backup the original file
if not os.path.exists(backup_path):
    shutil.copy(file_path, backup_path)
sr
# Apply patch to all files in the current repository
```

# Notes
- If the Jenkins output or error location is unclear, provide placeholders or assumptions.
- Ensure Python script are syntactically correct and functional.
- Avoid using external libraries that are not part of Python's standard library.
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

#Extract the python automation script part using regular expressions with re.DOTALL
python_code = re.search(r'```python(.*?)```', response.choices[0].message.content, re.DOTALL)
if python_code:
     python_code = python_code.group(1).strip()
else:
     python_code = ""


# Generate the bash script file with the extracted content if it exists
script_path = 'patch.py'
if python_code:
    with open(script_path, 'w') as file:
          file.write(python_code)
    print("Automation script generated and saved to patch.py")
else:
     print("No Automation script found in the file content.")

#Execute patch.py file
print("Executing patch.py file")
if os.path.exists(script_path):
    # Run the script
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    # Check the result
    if result.returncode == 0:
        print("Script executed successfully")
        print("Output:\n", result.stdout)
    else:
        print("Script execution failed")


client.close()

