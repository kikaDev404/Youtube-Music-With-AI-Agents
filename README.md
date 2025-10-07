# 🎵 Youtube Music With AI Agents

## 📘 About

**Youtube-Music-With-AI-Agents** is a project that allows you to explore and manage **YouTube Music** effortlessly using **Agentic AI** capabilities.  
You can **search for music**, **create playlists**, and **add songs to playlists** — all handled intelligently by AI.

---

## ⚙️ yt_music

`yt_music` is a **custom-built tool class** that uses the `ytmusicapi` library to create tools the AI agent can use to perform actions such as:
- Searching for songs  
- Creating playlists  
- Adding tracks to playlists  

---

## 🧠 Ollama Model

This project uses a **locally hosted Ollama model** for AI reasoning.  
You can, however, integrate **any LLM** (OpenAI, Anthropic, or others) as per your setup.

---

## 🚀 Future Enhancements

- [ ] Add an **Evaluator LLM** for improved self-correction  
- [ ] Add **more features** for non-authenticated users  

---

## 🔐 Authentication Setup

To authenticate your YouTube Music account:

1. Open **YouTube Music** in a **private/incognito window**.  
2. Press **F12** or **Inspect Element** → navigate to the **Network** tab.  
3. Perform any action (e.g., search for a song or click the YouTube Music home icon).  
4. Look for a network request named **`browse?`** on the left panel.  
5. Click it → open the **Request Headers** tab.  
6. Find and **copy** the **Cookie** data.  
7. In your project root directory, create a file named `browser.json`.  
8. Paste your details using the following structure:

```json
{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Authorization": "SAPISIDHASH asdfasdfasdfasdf SAPISID1PHASH asdfasdfasdfasdf SAPISID3PHASH asdfasdfasdfasdf",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "X-Goog-AuthUser": "0",
    "x-origin": "https://music.youtube.com",
    "Cookie": "<your cookie data>"
}
