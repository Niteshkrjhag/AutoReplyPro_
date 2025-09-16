# AutoReplyPro

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Cohere](https://img.shields.io/badge/AI-Cohere-purple)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)

An intelligent WhatsApp automation system that leverages advanced AI to provide contextual, human-like responses. Built with enterprise-grade architecture principles, this solution combines computer vision, natural language processing, and robust configuration management to deliver seamless automated messaging experiences.

Designed for professionals who need to maintain communication presence while focusing on high-priority tasks, AutoReplyPro demonstrates sophisticated software engineering practices including modular architecture, comprehensive error handling, and intelligent fallback mechanisms.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AutoReplyPro Architecture                │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   app.py     │    │   GUI Layer     │    │  CLI Interface  │
│ (Main Entry) │◄──►│ (PySimpleGUI)   │◄──►│  (Interactive)  │
└──────┬───────┘    └─────────────────┘    └─────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Core Engine                              │
├─────────────────┬─────────────────┬─────────────────────────┤
│   AI Engine     │ Config Manager  │    UI Controller        │
│ (Cohere API)    │ (JSON Persist)  │  (PyAutoGUI + CV)       │
│                 │                 │                         │
│ • Response Gen  │ • Settings      │ • Image Recognition     │
│ • Multi-model   │ • Persistence   │ • Screen Automation     │
│ • Fallback      │ • Validation    │ • Coordinate Setup      │
└─────────────────┴─────────────────┴─────────────────────────┘
       │                    │                     │
       ▼                    ▼                     ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Cohere API     │ │   config.json   │ │ WhatsApp Desktop│
│  • command-a    │ │  • User Prefs   │ │ • Screen Capture│
│  • command-r    │ │  • Coordinates  │ │ • UI Automation │
│  • Timeout Mgmt │ │  • API Keys     │ │ • Message I/O   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## ✨ Key Features

### 🤖 **Advanced AI Integration**
- **Multi-Model Support**: Command-A (speed-optimized) and Command-R (capability-focused) models
- **Contextual Understanding**: Analyzes complete chat history for relevant responses
- **Intelligent Fallback**: Graceful degradation with pre-configured responses during API failures
- **Response Validation**: Built-in testing framework for response quality assurance

### 🌐 **Multilingual Excellence**
- **Native Hinglish Support**: Seamless Hindi-English code-mixing for natural conversations
- **Cultural Context Awareness**: Understands colloquialisms and cultural references
- **Adaptive Language Models**: Automatically adjusts language based on conversation context

### 🛠️ **Enterprise-Grade Architecture**
- **Modular Design**: Clean separation of concerns with dedicated engines for AI, UI, and configuration
- **Thread-Safe Operations**: Asynchronous scanning with proper resource management
- **Comprehensive Error Handling**: Robust exception handling with detailed logging
- **Configuration Management**: Persistent settings with validation and migration support

### 🖥️ **Intelligent UI Automation**
- **Computer Vision Integration**: Image-based UI element detection for reliability
- **Coordinate Calibration**: Interactive setup wizard for precise UI targeting
- **Platform Abstraction**: Extensible design for multiple messaging platforms
- **Fail-Safe Mechanisms**: Built-in safety features to prevent unintended actions

## 🚀 Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI/ML** | Cohere API (Command Series) | Natural language generation and understanding |
| **GUI Framework** | PySimpleGUI | Cross-platform user interface |
| **Automation** | PyAutoGUI + OpenCV | Screen interaction and computer vision |
| **Configuration** | JSON + Custom Manager | Persistent settings and state management |
| **Concurrency** | Threading | Non-blocking operation execution |
| **Platform Integration** | PyObjC (macOS) | Native system integration |

## 📋 System Requirements

### **Minimum Requirements**
- **OS**: macOS 10.14+ (primary), Windows 10+ (limited support)
- **Python**: 3.7+ (3.9+ recommended)
- **Memory**: 512MB RAM
- **Storage**: 100MB free space
- **Network**: Stable internet for AI API calls

### **Dependencies**
- **Core**: `cohere`, `pyautogui`, `pyperclip`, `opencv-python`
- **GUI**: `PySimpleGUI`, `pillow`
- **macOS**: `pyobjc` framework suite
- **Utilities**: `requests`, `pathlib`, `threading`

## 🔧 Installation & Setup

### **1. Environment Setup**
```bash
# Clone the repository
git clone https://github.com/Niteshkrjhag/AutoReplyPro_.git
cd AutoReplyPro_

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. API Configuration**
1. Create account at [cohere.ai](https://cohere.ai)
2. Generate API key from dashboard
3. Run initial setup: `python app.py`
4. Select option 4 to configure API key

### **3. UI Calibration**
```bash
# Run coordinate setup wizard
python app.py
# Select option 3: Setup Coordinates
# Follow guided calibration for WhatsApp elements
```

## 🎯 Usage Guide

### **Command Line Interface**
```bash
python app.py
```

**Available Operations:**
1. **Start Scanning** - Begin automated monitoring
2. **Stop Scanning** - Halt automation gracefully  
3. **Setup Coordinates** - Calibrate UI elements
4. **Configure API** - Set Cohere credentials
5. **Test Responses** - Validate AI output quality
6. **Configure Settings** - Adjust behavior parameters
7. **Exit** - Clean shutdown

### **Configuration Options**
```json
{
  "ai_model": "command-a-03-2025",     // Speed vs capability
  "api_timeout": 10,                   // Response time limit
  "fallback_mode": true,               // Graceful degradation
  "language_mix": "Hindi-English",     // Communication style
  "response_tone": "warm",             // Personality setting
  "check_interval": 5                  // Monitoring frequency
}
```

## 🔄 System Flow

1. **Initialization**: Load configuration and initialize AI engine
2. **UI Detection**: Locate WhatsApp elements using computer vision
3. **Message Monitoring**: Continuously scan for new incoming messages
4. **Context Analysis**: Extract and analyze conversation history
5. **Response Generation**: Generate contextual reply using AI
6. **Quality Validation**: Verify response appropriateness
7. **Automated Delivery**: Send response via UI automation
8. **State Management**: Update conversation tracking

## 🛡️ Security & Privacy

- **API Key Protection**: Secure credential storage with encryption
- **Local Processing**: No conversation data sent to external servers (except AI API)
- **Minimal Permissions**: Requires only screen access and clipboard
- **Audit Logging**: Comprehensive activity logging for transparency
- **Rate Limiting**: Built-in throttling to prevent abuse

## 🔮 Future Roadmap

### **Near-term Enhancements**
- [ ] **Multi-Platform Support**: Telegram, Discord, Slack integration
- [ ] **Advanced ML Models**: Custom fine-tuned models for specific use cases
- [ ] **Web Dashboard**: Browser-based configuration and monitoring
- [ ] **Mobile App**: Companion app for remote control

### **Long-term Vision**
- [ ] **Enterprise Features**: Team management, analytics dashboard
- [ ] **API Integration**: RESTful API for third-party integrations
- [ ] **Cloud Deployment**: SaaS offering with scalable infrastructure
- [ ] **Voice Integration**: Voice-to-text and text-to-voice capabilities

## 🤝 Contributing

We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

**Quick Start for Contributors:**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Follow coding standards in [ARCHITECTURE.md](ARCHITECTURE.md)
4. Submit pull request with comprehensive description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Nitesh Kumar Jha**
- Software Engineer passionate about AI automation and user experience
- Demonstrates expertise in Python, AI integration, and system architecture
- Committed to building production-ready software with clean, maintainable code

---

*For technical interviews and system design discussions, see [INTERVIEW_NOTES.md](INTERVIEW_NOTES.md) and [SYSTEM_DESIGN_QA.md](SYSTEM_DESIGN_QA.md)*