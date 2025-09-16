# Contributing to AutoReplyPro

Thank you for your interest in contributing to AutoReplyPro! This document provides comprehensive guidelines for contributing to this AI-powered WhatsApp automation project.

## 🌟 Ways to Contribute

### **Code Contributions**
- Bug fixes and performance improvements
- New features and functionality enhancements
- Documentation improvements
- Test coverage expansion
- Platform compatibility extensions

### **Non-Code Contributions**
- Bug reports and feature requests
- Documentation improvements
- UI/UX feedback and suggestions
- Testing on different platforms
- Community support and mentoring

## 🛠️ Development Setup

### **Prerequisites**
- Python 3.7+ (3.9+ recommended)
- Git version control
- Code editor (VS Code recommended)
- macOS (primary development platform)

### **Local Environment Setup**
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork locally
git clone https://github.com/YOUR_USERNAME/AutoReplyPro_.git
cd AutoReplyPro_

# 3. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. Install development dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt  # If available

# 5. Set up pre-commit hooks (if configured)
pre-commit install

# 6. Create a new branch for your feature
git checkout -b feature/your-feature-name
```

### **Project Structure Understanding**
```
AutoReplyPro_/
├── app.py              # Main application entry point
├── config.json         # Configuration storage
├── requirements.txt    # Python dependencies
├── assets/            # UI automation assets
│   ├── message_box.png
│   └── whatsApp_icon.png
└── src/               # Core modules
    ├── ai_engine.py       # Cohere AI integration
    ├── config_manager.py  # Configuration management
    ├── gui.py            # PySimpleGUI interface
    └── ui_controller.py   # Screen automation logic
```

## 📝 Coding Standards

### **Python Style Guide**
Follow PEP 8 with these specific guidelines:

```python
# 1. Use meaningful variable and function names
def generate_contextual_response(chat_history: str) -> str:
    """Generate AI response based on conversation context."""
    pass

# 2. Include comprehensive docstrings
class AIEngine:
    """
    Handles AI-powered response generation using Cohere API.
    
    This class manages the integration with Cohere's language models,
    handles API timeouts, and provides fallback mechanisms.
    """

# 3. Use type hints where appropriate
def configure_api_timeout(self, timeout: int) -> bool:
    """Set API timeout with validation."""
    if not 5 <= timeout <= 60:
        return False
    self.config['api_timeout'] = timeout
    return True

# 4. Handle exceptions gracefully
try:
    response = self.co.chat(model=model, messages=messages)
    return response.message.content[0].text
except cohere.errors.ApiError as e:
    logging.error(f"Cohere API error: {e}")
    return self._get_fallback_response()
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    return "Sorry, I couldn't generate a response."
```

### **Code Quality Requirements**
- **Testing**: Include unit tests for new functionality
- **Logging**: Use appropriate logging levels (DEBUG, INFO, WARNING, ERROR)
- **Error Handling**: Implement comprehensive exception handling
- **Documentation**: Update docstrings and comments for complex logic
- **Configuration**: Make new features configurable when appropriate

## 🧪 Testing Guidelines

### **Test Structure**
```python
import unittest
from unittest.mock import Mock, patch
from src.ai_engine import AIEngine

class TestAIEngine(unittest.TestCase):
    """Test cases for AIEngine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.ai_engine = AIEngine()
        self.sample_chat = "User: Hello\nNitesh: Hi there!"
    
    def test_response_generation_success(self):
        """Test successful response generation."""
        # Test implementation
        pass
    
    def test_api_timeout_handling(self):
        """Test API timeout scenarios."""
        # Test implementation
        pass
    
    @patch('cohere.ClientV2')
    def test_fallback_response(self, mock_cohere):
        """Test fallback mechanism when API fails."""
        # Test implementation
        pass
```

### **Running Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_ai_engine.py

# Run with coverage
python -m pytest --cov=src tests/
```

## 🐛 Bug Reports

### **Before Submitting**
1. Check existing issues to avoid duplicates
2. Ensure you're using the latest version
3. Verify the bug isn't configuration-related

### **Bug Report Template**
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: macOS 12.0
- Python: 3.9.7
- AutoReplyPro Version: 1.0
- Dependencies: (paste pip freeze output)

## Additional Context
- Screenshots (if applicable)
- Log files (if available)
- Configuration settings (remove API keys)
```

## 🚀 Feature Requests

### **Feature Request Template**
```markdown
## Feature Description
Clear description of the proposed feature

## Problem Statement
What problem does this solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other approaches were considered?

## Implementation Ideas
Technical approach suggestions (optional)

## Priority
- [ ] Low
- [ ] Medium
- [ ] High
- [ ] Critical
```

## 📋 Pull Request Process

### **Before Submitting**
1. Ensure your branch is up to date with main
2. Run all tests and ensure they pass
3. Update documentation if needed
4. Test your changes thoroughly

### **Pull Request Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All existing tests pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
```

### **Review Process**
1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: Maintainer reviews code quality
3. **Testing**: Functionality testing on target platform
4. **Approval**: Merge approval from project maintainer

## 🎯 Priority Areas for Contribution

### **High Priority**
- **Cross-platform support**: Windows and Linux compatibility
- **Security enhancements**: API key encryption, secure storage
- **Performance optimization**: Faster response generation
- **Error handling**: More robust exception management

### **Medium Priority**
- **UI improvements**: Better user experience
- **Additional AI models**: Integration with other AI providers
- **Configuration validation**: Better config file validation
- **Logging enhancements**: Structured logging with rotation

### **Documentation**
- **API documentation**: Comprehensive API docs
- **Tutorial videos**: Step-by-step setup guides
- **Best practices**: Usage recommendations
- **Troubleshooting**: Common issues and solutions

## 🤝 Community Guidelines

### **Communication**
- **Be Respectful**: Treat all community members with respect
- **Be Constructive**: Provide helpful feedback and suggestions
- **Be Patient**: Remember that maintainers are volunteers
- **Be Clear**: Communicate clearly and provide necessary context

### **Code of Conduct**
Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## 📞 Getting Help

### **Channels**
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: niteshkrjhag@example.com (for sensitive issues)

### **Response Times**
- **Critical Issues**: Within 24 hours
- **Bug Reports**: Within 3-5 days
- **Feature Requests**: Within 1 week
- **Pull Reviews**: Within 1 week

## 🙏 Recognition

Contributors are recognized through:
- **Contributors file**: Listed in CONTRIBUTORS.md
- **Release notes**: Major contributions highlighted
- **GitHub**: Contributor status and badges
- **Recommendations**: LinkedIn recommendations for significant contributions

---

Thank you for contributing to AutoReplyPro! Your contributions help make this project better for everyone. 🚀