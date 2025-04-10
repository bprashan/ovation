import os
from openai import AzureOpenAI
import json
import re
import subprocess

azure_openai_url = os.getenv("ci-retries-aiagent-endpoint")
model_name = "gpt-4o-mini"
deployment = "gpt-4o-mini"
azure_openai_key = os.getenv("ci-retries-agentai-api-key")
api_version = "2024-12-01-preview"

# Set proxy details as environment variables
os.environ['http_proxy'] = 'http://proxy-chain.intel.com:911/'
os.environ['https_proxy'] = 'http://proxy-chain.intel.com:912/'
os.environ['no_proxy'] = "localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,intel.com,.openai.azure.com,10.*"


print(azure_openai_key)
print(azure_openai_url)

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=azure_openai_url,
    api_key=azure_openai_key,
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

Analyze the Jenkins console output to identify code errors and syntax errors, use the provided Git repository as the source, and create an automation Python script that generates code patches for fixing only the failed test cases. The script should replace the old function, line, or file with the corrected version, avoid introducing syntax errors, and create backup files before making any modifications.

# Steps

1. **Analyze Jenkins Console Output**:
    - Extract errors including details about failed test cases, file names, line numbers, functions, or code blocks.
    - Use the `{{Jenkins_console_output}}` input variable to identify areas that require modification.

2. **Access Git Repository**:
    - Access the Git repository to understand the code flow.
    - Locate files or code segments related to the failed test cases.
    - Assume the source code is present in the current working directory.

3. **Generate Code Patches**:
    - Using the extracted errors, make the necessary corrections to the identified code segments to resolve the issues.
    - Focus only on fixing errors related to failed test cases.
    - Ensure all corrections are syntax-error-free.

4. **Create and Apply Automation Script**:
    - The Python script should:
        - Identify the relevant file, line, or function based on the console output.
        - Apply the necessary changes to fix the errors.
        - Create a backup of the file before modifying it.

# Output Format

- Output a Python script in markdown format designed to:
    - Automatically locate and update the relevant code sections.
    - Maintain backups.
    - Ensure syntax correctness.

The response should only include the automation Python script incorporating the above steps and requirements.

# Examples

Example Input:
- Jenkins Console Output: `File "test_module.py", line 25, in test_function - NameError: name 'test_var' is not defined`
- Git Repository: `https://github.com/example/repo.git`

Example Python Script:

```python
import os
import shutil
import subprocess
import re

# Path to the file with the error
local_repo_path = os.path.join(os.getcwd())
file_path = os.path.join(local_repo_path, "test_module.py")
backup_path = file_path + ".bak"

# Backup the original file
if not os.path.exists(backup_path):
    shutil.copy(file_path, backup_path)

# Read the Jenkins console output
jenkins_console_output = \"""
File "test_module.py", line 25, in test_function
NameError: name 'test_var' is not defined
\"""

# Parse the console output to find the issue
pattern = r'File "([^"]+)", line (\d+), in (\w+)\s+(.+)'
matches = re.findall(pattern, jenkins_console_output)

if matches:
    file_name, line_number, function_name, error_message = matches[0]
    line_number = int(line_number)
    
    # Fix the issue in the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Example fix (You would replace this logic with actual logic to resolve the specific issue)
    if "NameError" in error_message:
        lines[line_number - 1] = "    test_var = 42  # Fixed the NameError\n"

    # Write the changes back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)

    print(f"Error fixed in {{file_path}} at line {{line_number}}. Backup created at {{backup_path}}.")
else:
    print("No issues detected in the Jenkins console output.")
```

### Notes

- This script is an example template for automating the workflow of error detection and correction.
- Real errors and fixes will vary based on the actual Jenkins console output; adjust the script's logic accordingly.
- Extend the `fix` logic to handle multiple types of errors as necessary.

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

# Extract the python automation script part using regular expressions with re.DOTALL
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




