import requests

# Define the URL
url = "https://limcheekin-zephyr-7b-beta-gguf.hf.space/v1/engines/copilot-codex/completions"

# Define a list of question and answer pairs
few_shot_data = [
    {
        "prompt": "\n\n### Instructions:\nQ: How does the Car Customization Assistant work?\nA: Our assistant uses natural conversations to collect user preferences, suggests configurations, and converts them into requirements for automated implementation.\n\n### Response:\n",
        "stop": ["\n", "###"]
    },
    {
        "prompt": "\n\n### Instructions:\nQ: How does it simplify preference consolidation?\nA: Our innovative approach replaces manual processes with a 24/7 virtual personalization expert.\n\n### Response:\n",
        "stop": ["\n", "###"]
    },
    {
        "prompt": "\n\n### Instructions:\nQ: Can I see a visual preview of my customized product?\nA: Yes, you'll receive a visual preview of your customized product before purchase to ensure satisfaction.\n\n### Response:\n",
        "stop": ["\n", "###"]
    }
]


fewshotData = ""
for data in few_shot_data:
    fewshotData = fewshotData + data['prompt']


prompt = fewshotData + "\n\n### Instructions:\nWhat is the capital of France?\n\n### Response:\n",

print(prompt, "\n\n\n\n")

# Send a POST request with few-shot data list
response = requests.post(url, json=prompt)

# Check if the request was successful
if response.status_code == 200:
    print(f"Response for prompt: {prompt}")
    print(response.text)
    print("\n" + "=" * 50 + "\n")
else:
    print(f"Request failed for prompt: {prompt} with status code {response.status_code}")


'''
import requests

# Define the URL and request body
url = "https://limcheekin-zephyr-7b-beta-gguf.hf.space/v1/engines/copilot-codex/completions"
data = {
    "prompt": "\n\n### Instructions:\nHow does the Car Customization Assistant work?\n\n### Response:\n",
    "stop": [
        "\n",
        "###"
    ]
}

# Send the POST request
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Print the response content
    print(response.text)
else:
    print(f"Request failed with status code {response.status_code}")


'''