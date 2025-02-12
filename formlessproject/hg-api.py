'''

hugging face spaces : limcheekin/zephyr-7B-beta-GGUF

Dockerfile :
# Grab a fresh copy of the Python image
FROM python:3.11-slim

# Install build and runtime dependencies
RUN apt-get update && \
    apt-get install -y \
    libopenblas-dev \
    ninja-build \
    build-essential \
    pkg-config \
    curl

RUN pip install -U pip setuptools wheel && \
    CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" FORCE_CMAKE=1 pip install --verbose llama-cpp-python[server]

# Download model
RUN mkdir model && \
    curl -L https://huggingface.co/TheBloke/zephyr-7B-beta-GGUF/resolve/main/zephyr-7b-beta.Q4_K_M.gguf -o model/gguf-model.bin

COPY ./start_server.sh ./
COPY ./main.py ./
COPY ./index.html ./

# Make the server start script executable
RUN chmod +x ./start_server.sh

# Set environment variable for the host
ENV HOST=0.0.0.0
ENV PORT=7860

# Expose a port for the server
EXPOSE ${PORT}

# Run the server start script
CMD ["/bin/sh", "./start_server.sh"]    


Readme:
title: zephyr-7B-beta-GGUF (Q4_K_M)
colorFrom: purple
colorTo: blue
sdk: docker
models:
  - HuggingFaceH4/zephyr-7b-beta
  - TheBloke/zephyr-7B-beta-GGUF
tags:
  - inference api
  - openai-api compatible
  - llama-cpp-python
  - zephyr-7B-beta-GGUF
  - gguf
pinned: false


zephyr-7B-beta-GGUF (Q4_K_M)

index.html:
<!DOCTYPE html>
<html>
  <head>
    <title>zephyr-7B-beta-GGUF (Q4_K_M)</title>
  </head>
  <body>
    <h1>zephyr-7B-beta-GGUF (Q4_K_M)</h1>
    <p>
      With the utilization of the
      <a href="https://github.com/abetlen/llama-cpp-python">llama-cpp-python</a>
      package, we are excited to introduce the GGUF model hosted in the Hugging
      Face Docker Spaces, made accessible through an OpenAI-compatible API. This
      space includes comprehensive API documentation to facilitate seamless
      integration.
    </p>
    <ul>
      <li>
        The API endpoint:
        <a href="https://limcheekin-zephyr-7b-beta-gguf.hf.space/v1"
          >https://limcheekin-zephyr-7b-beta-gguf.hf.space/v1</a
        >
      </li>
      <li>
        The API doc:
        <a href="https://limcheekin-zephyr-7b-beta-gguf.hf.space/docs"
          >https://limcheekin-zephyr-7b-beta-gguf.hf.space/docs</a
        >
      </li>
    </ul>
    <p>
      Go ahead and try it out the API endpoint yourself with the
      <a
        href="https://huggingface.co/spaces/limcheekin/zephyr-7B-beta-GGUF/blob/main/zephyr-7b.ipynb"
        target="_blank"
      >
        zephyr-7b.ipynb</a
      >
      jupyter notebook.
    </p>
    <p>
      If you find this resource valuable, your support in the form of starring
      the space would be greatly appreciated. Your engagement plays a vital role
      in furthering the application for a community GPU grant, ultimately
      enhancing the capabilities and accessibility of this space.
    </p>
  </body>
</html>


main.py:
from llama_cpp.server.app import create_app, Settings
from fastapi.responses import HTMLResponse
from fastapi.middleware.gzip import GZipMiddleware
import os

app = create_app(
    Settings(
        n_threads=2,  # set to number of cpu cores
        model="model/gguf-model.bin",
        embedding=True
    )
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Read the content of index.html once and store it in memory
with open("index.html", "r") as f:
    content = f.read()


@app.get("/", response_class=HTMLResponse)
async def read_items():
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,
                host=os.environ["HOST"],
                port=int(os.environ["PORT"])
                )


start_server.sh:
#!/bin/sh

# For mlock support
ulimit -l unlimited

python3 -B main.p


this is an working llm api hosted on huggin face spaces

api request url : https://limcheekin-zephyr-7b-beta-gguf.hf.space/v1/engines/copilot-codex/completions

post request body :
{
  "prompt": "\n\n### Instructions:\nWhat is the capital of France?\n\n### Response:\n",
  "stop": [
    "\n",
    "###"
  ]
}

responses:
{
  "id": "cmpl-b5f0353f-ad77-4474-8372-9ad56b63c4be",
  "object": "text_completion",
  "created": 1699270579,
  "model": "model/gguf-model.bin",
  "choices": [
    {
      "text": "The capital of France is Paris. ",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 21,
    "completion_tokens": 9,
    "total_tokens": 30
  }
}


insteed of gguf model use huggingface model = atharvapawar/flaskCodemistral-7b-mj-finetuned
link : https://huggingface.co/atharvapawar/flaskCodemistral-7b-mj-finetuned/blob/main/adapter_model.bin



'''