# 🚀 Smart Logistics Robot
[中文版 🇨🇳](./README.md) | [English Version 🇬🇧](./README_EN.md)


> **Author:** dzx  
> A Python-based intelligent logistics robot system  
> Integrated with **KDNiao API** (Real-time logistics tracking) and **Zhipu AI API** (Smart dialogue).  
> Capable of performing **real logistics tracking + intelligent chatbot conversations**.

---

## 🧠 Overview

This project is an intelligent robot system that can **query real logistics information** and **engage in smart natural language conversations**.  
It was developed in four stages, evolving from a simple rule-based bot to a full-featured intelligent logistics assistant.

---

## 📁 Project Structure

| Folder | Description |
|---------|--------------|
| `chatbot` | The first-generation logistics bot based on a preset Q&A library. It can only answer predefined questions. |
| `ai_robot` | Integrated with Zhipu AI API for intelligent open-domain conversation. |
| `wuliu_robot` | Integrated with KDNiao API for real logistics tracking. |
| `smartwuliu_robot` | Combines the features of both `ai_robot` and `wuliu_robot` for a fully functional smart logistics robot. |

---

## ✨ Key Features

- 🤖 **Smart Q&A:** Powered by Zhipu AI for natural and multi-turn conversations.  
- 📦 **Real-time Logistics Tracking:** Uses KDNiao API to access authentic delivery information.  
- 🧩 **Multi-functional Integration:** Combines conversation, tracking, and history management.  
- 🧠 **Modular Design:** Each component is independent and extendable.  
- 💬 **CLI Interface:** Simple command-line interface for user interaction.

---

## 🏗️ Tech Stack

| Technology | Description |
|-------------|-------------|
| **Python 3.9+** | Core programming language |
| **Zhipu AI API** | Provides intelligent language capabilities |
| **KDNiao API** | Enables real-time logistics tracking |
| **hashlib / requests / json** | For API communication and data processing |
| **CLI (Command-Line Interface)** | Lightweight text-based interaction |

---

## ⚙️ Setup and Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/dzx12389/logistics_robot.git
cd logistics_robot
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run Examples
#### Run the basic chatbot:
```bash
python chatbot/main.py
```

#### Run the intelligent AI chatbot:
```bash
python ai_robot/main.py
```

#### Run the logistics tracking bot:
```bash
python wuliu_robot/main.py
```

#### Run the full smart logistics bot:
```bash
python smartwuliu_robot/smart_logistics_bot.py
```

---

## 🧩 How to Use

### Smart Logistics Bot (smartwuliu_robot)
| Command | Description |
|----------|-------------|
| Enter a tracking number | Query real logistics information |
| Enter any question | Engage in smart conversation |
| `history` | View chat or tracking history |
| `exit` | Exit the program |

---

## 📷 Screenshots

### 🧱 1️⃣ Basic Chatbot (chatbot)
![chatbot](docs/images/chatbot_demo.png)

### 🧠 2️⃣ AI Chatbot (ai_robot)
![ai_robot](docs/images/ai_robot_demo.png)

### 📦 3️⃣ Logistics Tracking Bot (wuliu_robot)
![wuliu_robot](docs/images/wuliu_robot_demo.png)

### 🚀 4️⃣ Smart Logistics Bot (smartwuliu_robot)
![smartwuliu_robot](docs/images/smartwuliu_robot_demo.png)

---

## 🔌 API Configuration

### Zhipu AI API
Set the following in `config.py`:
```python
ZHIPU_API_KEY = "your_zhipu_api_key"
```

### KDNiao API
Set the following in `config.py`:
```python
KDNIAO_API_KEY = "your_kdniao_api_key"
KDNIAO_USER_ID = "your_user_id"
```

---

## 🌱 Future Plans
- [ ] Add a GUI interface  
- [ ] Support multi-model conversation engines  
- [ ] Integrate voice input and output  
- [ ] Enhance context memory and chat history

---

## 📜 License
This project is for **learning and research purposes only**.  
Commercial use is prohibited.  
© 2025 dzx. All rights reserved.

---

## ❤️ Acknowledgements
Special thanks to:  
- [Zhipu AI](https://open.bigmodel.cn/) for providing intelligent dialogue capabilities.  
- [KDNiao](https://www.kdniao.com/) for real-time logistics tracking API.  
- All contributors and testers who supported this project 🙌
