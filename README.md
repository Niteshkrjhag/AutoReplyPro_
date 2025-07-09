# AutoReplyPro

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A sophisticated WhatsApp auto-reply bot powered by Cohere AI that generates human-like responses to incoming messages. This tool uses screen automation to interact with WhatsApp Desktop, providing a seamless chatting experience even when you're away.

## ✨ Features

- **AI-Powered Responses**: Leverages Cohere's language models to generate contextually relevant, human-like replies
- **Multiple AI Models**: Choose between different Cohere models - faster (command-a) or more capable (command-r)
- **Natural Mixed-Language Support**: Excels at Hindi-English (Hinglish) conversations
- **Fallback Mode**: Continues functioning with pre-defined responses when API is unavailable
- **Response Testing**: Test AI-generated responses before deploying the bot
- **Configurable Settings**: Customize response style, API timeouts, and check intervals
- **User-Friendly Setup**: Interactive coordinate setup wizard for easy configuration

## 🚀 Real-World Applications

- **Personal Assistant**: Maintain your social presence when you're busy or unavailable
- **Customer Support**: Provide initial responses to common inquiries outside business hours
- **Social Media Management**: Keep engagement high on WhatsApp Business accounts
- **Networking Tool**: Never miss an important conversation, even when you're offline

## 📋 Prerequisites

- Python 3.7+
- WhatsApp Desktop Application
- Cohere API key (free tier available at [cohere.ai](https://cohere.ai))
- macOS (for optimal compatibility due to pyobjc dependencies)

## 🔧 Installation

1. Clone this repository or download the source code
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a Cohere API account and get your API key from the dashboard

## ⚙️ Setup and Configuration

1. Run the application:

```bash
python main.py
```

2. You'll see the main menu with the following options:

```
--- MENU (Status: STOPPED) ---
1. Start Scanning
2. Stop Scanning
3. Setup Coordinates
4. Configure API Key
5. Test Response Generation
6. Configure Settings
7. Exit
```

3. Use the interactive menu to set up and control the bot:

   - **Option 1: Start Scanning**
     - Activates the bot to monitor WhatsApp for new messages
     - Automatically responds to incoming messages

   - **Option 2: Stop Scanning**
     - Halts the bot's monitoring and response activity
     - Use this when you want to take over the conversation

   - **Option 3: Setup Coordinates**
     - Follow the wizard to position your cursor over WhatsApp UI elements
     - Set coordinates for WhatsApp icon, chat area, and message box

   - **Option 4: Configure API Key**
     - Enter your Cohere API key for AI-powered responses

   - **Option 5: Test Response Generation**
     - Test how the AI would respond to sample chat histories
     - Verify response quality before activating the bot

   - **Option 6: Configure Settings**
     - Select AI model (command-a-03-2025 for speed or command-r-03-2025 for quality)
     - Set API timeout duration (5-60 seconds)
     - Toggle fallback mode (on/off)

   - **Option 7: Exit**
     - Safely closes the application

## 🎮 Usage

1. Open WhatsApp Desktop and navigate to the chat you want the bot to monitor
2. Run the program and select option `1` to start scanning
3. The bot will:
   - Monitor for new incoming messages
   - Generate contextually appropriate responses using AI
   - Automatically reply to messages
4. Select option `2` to stop the bot at any time

## 🔍 How It Works

1. The bot uses PyAutoGUI to monitor the WhatsApp chat area
2. When a new message is detected, it copies the chat text
3. The message is sent to Cohere's AI for generating a response
4. The response is automatically typed and sent in WhatsApp
5. In case of API failure, the bot uses fallback responses to maintain conversation

## ⚠️ Limitations

- Requires WhatsApp Desktop to be visible on screen
- Screen resolution changes may require reconfiguring coordinates
- Response generation depends on Cohere API availability
- Currently optimized for macOS due to pyobjc dependencies

## 📝 Note

This project is intended for educational and personal use. Please respect WhatsApp's terms of service and others' privacy when using this bot.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/niteshkrjhag/autoreplypro/issues).

## 📄 License

This project is [MIT](LICENSE) licensed.

---
*Last updated: 2025-07-09 13:22:35 UTC by @Niteshkrjhag*

## 📹 Demo Video

Watch the full demo here:
https://youtu.be/hZiXlHr4EVE?feature=shared
