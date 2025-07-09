import pyautogui
import pyperclip
import time
import logging
import cv2
import numpy as np
import os
from PIL import ImageGrab
from pathlib import Path

class UIController:
    """Handles UI automation using image recognition instead of coordinates"""
    
    def __init__(self, assets_dir="assets"):
        self.assets_dir = Path(assets_dir)
        self.confidence_threshold = 0.7
        self.last_chat_text = ""
        self.platform = "whatsapp"  # Default platform
        
        # Initialize PyAutoGUI safely
        pyautogui.PAUSE = 0.5
        pyautogui.FAILSAFE = True
    
    def set_platform(self, platform):
        """Set the messaging platform to use"""
        self.platform = platform.lower()
        logging.info(f"Platform set to: {self.platform}")
    
    def find_and_click(self, image_name, double_click=False, confidence=None):
        """Find an image on screen and click it"""
        if confidence is None:
            confidence = self.confidence_threshold
            
        image_path = self.assets_dir / f"{self.platform}_{image_name}.png"
        
        if not image_path.exists():
            logging.error(f"Image not found: {image_path}")
            return False
        
        try:
            location = pyautogui.locateCenterOnScreen(str(image_path), confidence=confidence)
            if location:
                if double_click:
                    pyautogui.doubleClick(location)
                else:
                    pyautogui.click(location)
                return True
            else:
                logging.warning(f"Could not find {image_name} on screen")
                return False
        except Exception as e:
            logging.error(f"Error finding/clicking {image_name}: {str(e)}")
            return False
    
    def open_messaging_app(self):
        """Open the configured messaging application"""
        logging.info(f"Opening {self.platform}...")
        
        # Try to find and click the app icon
        if self.find_and_click("icon", double_click=True):
            time.sleep(3)  # Wait for app to open
            return True
            
        # If icon not found, try alternative methods based on platform
        if self.platform == "whatsapp":
            try:
                # On macOS, try using Spotlight
                pyautogui.hotkey('command', 'space')
                time.sleep(0.5)
                pyautogui.write('whatsapp')
                time.sleep(0.5)
                pyautogui.press('return')
                time.sleep(3)
                return True
            except Exception as e:
                logging.error(f"Failed to open WhatsApp: {str(e)}")
                return False
                
        return False
    
    def select_chat_area(self):
        """Select the chat area to copy text from"""
        # Try to find and click the chat area
        if self.find_and_click("chat_area"):
            time.sleep(0.5)
            # Select all text in the chat area
            pyautogui.hotkey('command', 'a')
            time.sleep(0.5)
            return True
        else:
            logging.warning("Could not find chat area")
            return False
    
    def copy_chat_text(self):
        """Copy the current chat text using select all and copy"""
        try:
            # Select the chat area first
            if self.select_chat_area():
                # Copy the selected text
                pyautogui.hotkey('command', 'c')
                time.sleep(0.5)
                
                # Get the copied text
                chat_text = pyperclip.paste()
                return chat_text if chat_text else ""
            return ""
        except Exception as e:
            logging.error(f"Error copying chat text: {str(e)}")
            return ""
    
    def send_message(self, message):
        """Send a message in the messaging app"""
        try:
            # Find and click the message box
            if not self.find_and_click("message_box"):
                logging.warning("Could not find message box")
                return False
            
            # Copy message to clipboard and paste
            pyperclip.copy(message)
            time.sleep(0.5)
            pyautogui.hotkey('command', 'v')
            time.sleep(0.5)
            
            # Send the message
            pyautogui.press('return')
            return True
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            return False
    
    def get_last_message(self, chat_text):
        """Extract the last message from the chat text"""
        if not chat_text:
            return ""
            
        # Split by lines and find the last non-empty message
        lines = [line.strip() for line in chat_text.split('\n') if line.strip()]
        return lines[-1] if lines else ""
    
    def is_message_from_other_person(self, message, persona_name):
        """Check if the message is from another person (not the bot)"""
        if not message:
            return False
            
        # Simple heuristic: if the message contains the persona name, it's likely not from another person
        # This is a simplification and might need refinement based on specific chat format
        return persona_name.lower() not in message.lower()