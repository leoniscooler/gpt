# ChatGPT

A full-featured ChatGPT replica built with [Streamlit](https://streamlit.io) -- **no API key required**. Powered by [g4f](https://github.com/xtekky/gpt4free) for free access to GPT models.

## Features

- **No API key needed** -- works out of the box, anyone can use it immediately
- **ChatGPT-style dark UI** -- pixel-accurate dark theme matching the real ChatGPT interface
- **Streaming responses** -- tokens appear in real time for a fast, responsive feel
- **Multi-model support** -- switch between GPT-4o, GPT-4o mini, GPT-4, and GPT-3.5 Turbo
- **Conversation management** -- create multiple chats, switch between them, and clear history
- **Auto-titling** -- conversations are automatically named from your first message

## Setup

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run locally

streamlit run streamlit_app.py

That is it -- no API key configuration needed!

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to share.streamlit.io
3. Connect the repo
4. Deploy -- no secrets needed!

## Tech Stack

- **Streamlit** -- UI framework
- **g4f** -- free GPT model access with streaming (no API key)
- **Custom CSS** -- ChatGPT-accurate dark theme