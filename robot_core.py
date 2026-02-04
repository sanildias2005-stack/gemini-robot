import os
import subprocess
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

SYSTEM_PROMPT = """
You are a system automation robot.
Your job is to read the user's instructions and output valid JSON like this:

{
  "action": "shell",
  "command": "THE WINDOWS CMD COMMAND HERE"
}

Rules:
- ALWAYS output JSON only.
- If required to find files, write correct Windows commands.
- If user wants to move/copy files, write commands.
- You NEVER run commands yourself — just provide JSON with "command".
"""

def run_shell(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        return e.output

def ask_gemini(prompt):
    response = client.chat.completions.create(
        model="google/gemini-pro-1.5-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]