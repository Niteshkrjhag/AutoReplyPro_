import pyautogui
import time
import pyperclip
import cohere
import logging
import sys
import json
import threading
import random
from pathlib import Path
import re
import socket
import requests.exceptions

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# --- PyAutoGUI Configuration ---
pyautogui.PAUSE = 0.1

class WhatsAppBot:
    """
    An advanced WhatsApp auto-reply bot engineered for human-like conversation.
    """
    def __init__(self):
        # --- Core Configuration ---
        self.config = {
            'api_key': 'OuZwuEkZf2PbrtECPpT1rI5JZFyFPFK3HPOaIexg',
            'persona_name': 'Nitesh',
            'check_interval': 4,
            'inactivity_timeout': 600,
            'api_timeout': 10,  # Timeout for API calls in seconds
            'whatsapp_coords': (1124, 860),
            'chat_area': {'start_x': 400, 'start_y': 100, 'end_x': 1200, 'end_y': 900},
            'message_box_coords': (652, 950),
            'debug_mode': True,
            'cohere_model': 'command-a-03-2025',
            'use_fallback_mode': True,  # Whether to use fallback responses when API times out
        }
        self.load_config()

        # --- Prepare fallback responses ---
        self.fallback_responses = [
            "Hey! Kya chal raha hai? 😊",
            "Arey yaar, abhi thoda busy hoon. Thodi der baad baat karte hain?",
            "Haan bhai, bol?",
            "Acha, samajh gaya. Koi baat nahi!",
            "Haha, mazak kar raha tha yaar! 😂",
            "Kya plan hai aaj ka?",
            "Sab theek? Kuch problem hai kya?",
            "Sorry, thoda late ho gaya reply karne mein!",
            "Bilkul sahi keh raha hai tu!",
            "Arey waah! Kya baat hai! 👍",
            "Chal, thodi der baad baat karte hain.",
            "Haan, main free hoon. Bata?",
            "Mil ke baat karenge iske baare mein.",
            "Arre koi nahi, next time pakka!",
            "Sahi hai yaar! 🔥",
        ]

        # --- API and State Initialization ---
        self.co = None
        if self.config['api_key']:
            try:
                # Using ClientV2 for Cohere Chat API
                self.co = cohere.ClientV2(api_key=self.config['api_key'])
                logging.info("Cohere API Client V2 initialized successfully.")
            except Exception as e:
                logging.error(f"Failed to initialize Cohere API: {e}")

        self.last_message_processed = ""
        self.running = False
        self.scan_thread = None

    def load_config(self):
        """Loads configuration from config.json, allowing overrides."""
        try:
            if Path("config.json").exists():
                with open("config.json", "r") as f:
                    self.config.update(json.load(f))
                logging.info("Configuration loaded from config.json.")
        except Exception as e:
            logging.error(f"Error loading config.json: {e}")

    def save_config(self):
        """Saves the current configuration to config.json."""
        try:
            with open("config.json", "w") as f:
                json.dump(self.config, f, indent=4)
            logging.info("Configuration saved to config.json.")
        except Exception as e:
            logging.error(f"Error saving config.json: {e}")

    # --- UI Automation Methods ---

    def open_whatsapp(self):
        """Brings the WhatsApp application to the foreground."""
        try:
            x, y = self.config['whatsapp_coords']
            logging.info(f"Activating WhatsApp at coordinates ({x}, {y}).")
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()
            time.sleep(2)
            return True
        except Exception as e:
            logging.error(f"Could not open WhatsApp: {e}")
            return False

    def copy_chat_text(self):
        """Atomically clears clipboard, selects chat area, and copies text."""
        try:
            pyperclip.copy("") # Atomic clear
            ca = self.config['chat_area']
            pyautogui.moveTo(ca['start_x'], ca['start_y'], duration=0.2)
            pyautogui.dragTo(ca['end_x'], ca['end_y'], duration=0.5, button='left')
            pyautogui.hotkey('command', 'c')
            time.sleep(0.5)
            chat_text = pyperclip.paste()
            if chat_text and len(chat_text) > 10:
                return chat_text
            return ""
        except Exception as e:
            logging.error(f"Error copying chat text: {e}")
            return ""

    def get_last_message(self, chat_text):
        """Extracts the very last message line from the chat history."""
        lines = [line.strip() for line in chat_text.split('\n') if line.strip()]
        return lines[-1] if lines else ""

    def is_from_other_person(self, message):
        """Checks if a message was sent by the other user."""
        return not message.lstrip().startswith(f"{self.config['persona_name']}:")

    def send_response(self, reply):
        """Clears the message box completely, then pastes and sends the reply."""
        try:
            x, y = self.config['message_box_coords']
            pyautogui.click(x, y)
            time.sleep(0.3)
            pyautogui.hotkey('command', 'a')  # Select all
            time.sleep(0.2)
            pyautogui.press('delete')         # Clear
            time.sleep(0.2)
            pyperclip.copy(reply)             # Paste new reply
            pyautogui.hotkey('command', 'v')
            time.sleep(0.3)
            pyautogui.press('return')
            logging.info(f"SUCCESS: Sent reply: {reply}")
            return True
        except Exception as e:
            logging.error(f"Failed to send response: {e}")
            return False

    # --- AI Core Logic ---

    def _get_fallback_response(self):
        """Returns a random fallback response when API fails."""
        return random.choice(self.fallback_responses)
    
    def _api_call_with_timeout(self, chat_history):
        """Make API call with timeout to prevent long waits."""
        # Create a result container that can be accessed across threads
        result = {"response": None, "error": None}
        
        # System message - simplified for faster processing
        system_message = {
            "role": "system", 
            "content": f"""
You are '{self.config['persona_name']}', a friend chatting on WhatsApp. Use a mix of Hindi and English.
Be brief (under 20 words), casual, and conversational. Match the tone of the last message.
Add occasional emojis. Do not explain or use meta-commentary. Just reply as {self.config['persona_name']}.
"""
        }
        
        # Create a user message with just the essential context
        user_message = {
            "role": "user",
            "content": f"WhatsApp chat:\n{chat_history}\n\nReply to the last message as me."
        }
        
        # Function to make the API call in a separate thread
        def make_api_call():
            try:
                result["response"] = self.co.chat(
                    model=self.config['cohere_model'],
                    messages=[system_message, user_message],
                    temperature=0.75,
                )
            except Exception as e:
                result["error"] = e
        
        # Start API call in a thread
        api_thread = threading.Thread(target=make_api_call)
        api_thread.daemon = True
        api_thread.start()
        
        # Wait for the thread to finish or timeout
        api_thread.join(timeout=self.config['api_timeout'])
        
        # Check results
        if api_thread.is_alive():
            # Thread is still running, which means it timed out
            logging.warning(f"API call timed out after {self.config['api_timeout']} seconds")
            return None, TimeoutError("API call timed out")
        
        if result["error"]:
            return None, result["error"]
            
        return result["response"], None

    def generate_response(self, chat_history):
        """Generates a human-like response using Cohere Chat API with timeout protection."""
        if not self.co:
            return self._get_fallback_response() if self.config['use_fallback_mode'] else "Error: Cohere API not initialized."
            
        try:
            # Make API call with timeout
            response, error = self._api_call_with_timeout(chat_history)
            
            # If there was an error or timeout
            if error:
                logging.error(f"Error calling Cohere API: {error}")
                return self._get_fallback_response() if self.config['use_fallback_mode'] else f"Sorry, couldn't get a response: {str(error)[:30]}..."
            
            if not response:
                return self._get_fallback_response() if self.config['use_fallback_mode'] else "Sorry, no response from API."
            
            # Extract and clean the reply text
            reply_text = response.message.content[0].text.strip()
            
            # Remove name prefix if present
            if reply_text.startswith(f"{self.config['persona_name']}:"):
                reply_text = reply_text.split(":", 1)[1].strip()
                
            # Remove quotes
            reply_text = reply_text.strip('"\'')

            logging.info(f"AI generated: {reply_text}")
            return reply_text
            
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return self._get_fallback_response() if self.config['use_fallback_mode'] else "Sorry, error generating response."

    def _scan_loop(self):
        """Main loop that checks for new messages and responds"""
        if not self.open_whatsapp():
            self.running = False
            return

        last_activity_time = time.time()
        
        initial_chat = self.copy_chat_text()
        self.last_message_processed = self.get_last_message(initial_chat)
        logging.info(f"Starting scan. Last message: \"{self.last_message_processed}\"")

        while self.running:
            try:
                current_chat_text = self.copy_chat_text()
                if not current_chat_text:
                    time.sleep(self.config['check_interval'])
                    continue

                last_message_on_screen = self.get_last_message(current_chat_text)

                # Check if this is a new message we haven't processed yet
                if last_message_on_screen and last_message_on_screen != self.last_message_processed:
                    # Check if the message is from the other person
                    if self.is_from_other_person(last_message_on_screen):
                        logging.info(f"New message from other person: \"{last_message_on_screen}\"")
                        last_activity_time = time.time()  # Reset inactivity timer

                        # Generate and send a response
                        reply = self.generate_response(current_chat_text)
                        if reply:
                            self.send_response(reply)
                            # Update what we've processed AFTER sending
                            self.last_message_processed = self.get_last_message(self.copy_chat_text())
                    else:
                        # If it's our own message, just mark it as processed
                        self.last_message_processed = last_message_on_screen

                # Check for inactivity timeout
                if time.time() - last_activity_time > self.config['inactivity_timeout']:
                    logging.info("No activity for a while. Stopping scan.")
                    break

                time.sleep(self.config['check_interval'])
            except Exception as e:
                logging.error(f"Error in scan loop: {e}")
                time.sleep(5)  # Shorter pause on error

        self.running = False
        logging.info("Scan loop ended.")

    def start_scanning(self):
        """Start looking for new messages"""
        if self.running:
            logging.warning("Already scanning!")
            return False
            
        if not self.co and not self.config['use_fallback_mode']:
            logging.error("Cannot start: Cohere API not initialized and fallback mode disabled")
            return False
            
        self.running = True
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()
        logging.info("Started scanning for messages")
        return True

    def stop_scanning(self):
        """Stop looking for new messages"""
        if not self.running:
            logging.info("Not currently scanning")
            return
            
        self.running = False
        if self.scan_thread:
            self.scan_thread.join(timeout=3.0)
        logging.info("Stopped scanning")

# Helper function to set up coordinates
def setup_coordinates():
    """Guide the user to set up the coordinates for WhatsApp elements"""
    bot = WhatsAppBot()
    
    print("\n--- Coordinate Setup Wizard ---")
    print("For each step, move your mouse to the right spot and press Enter.")
    
    input("1. Hover over the WhatsApp icon and press Enter...")
    bot.config['whatsapp_coords'] = pyautogui.position()
    print(f"   WhatsApp icon at: {bot.config['whatsapp_coords']}")
    
    input("\n2. Open a chat. Hover over the TOP-LEFT corner of the chat area and press Enter...")
    tl = pyautogui.position()
    
    input("3. Now hover over the BOTTOM-RIGHT corner of the chat area and press Enter...")
    br = pyautogui.position()
    
    bot.config['chat_area'] = {
        'start_x': tl.x, 
        'start_y': tl.y,
        'end_x': br.x, 
        'end_y': br.y
    }
    print(f"   Chat area from {tl} to {br}")
    
    input("\n4. Finally, hover over the message input box and press Enter...")
    bot.config['message_box_coords'] = pyautogui.position()
    print(f"   Message box at: {bot.config['message_box_coords']}")
    
    bot.save_config()
    print("\n--- Coordinates saved! ---")

# Main program function
def main():
    """Main function that displays the menu and handles user choices"""
    bot = WhatsAppBot()
    
    print("\n===================================")
    print("  WhatsApp Auto-Reply Bot  ")
    print("===================================")
    
    while True:
        status = "RUNNING" if bot.running else "STOPPED"
        print(f"\n--- MENU (Status: {status}) ---")
        print("1. Start Scanning")
        print("2. Stop Scanning")
        print("3. Setup Coordinates")
        print("4. Configure API Key")
        print("5. Test Response Generation")
        print("6. Configure Settings")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            bot.start_scanning()
        elif choice == '2':
            bot.stop_scanning()
        elif choice == '3':
            setup_coordinates()
        elif choice == '4':
            api_key = input("Enter your Cohere API Key: ").strip()
            if api_key:
                bot.config['api_key'] = api_key
                bot.save_config()
                # Re-initialize with new key
                bot.co = cohere.ClientV2(api_key=api_key)
                print("API Key saved and initialized.")
        elif choice == '5':
            print("\n--- Test the AI Response ---")
            history = input("Paste a sample chat history, then press Enter:\n")
            if history:
                print("Generating response...")
                response = bot.generate_response(history)
                print("\n-------------------------")
                print(f"AI would respond: {response}")
                print("-------------------------")
        elif choice == '6':
            print("\n--- Configure Settings ---")
            print("1. Select Cohere Model")
            print("2. Set API Timeout")
            print("3. Toggle Fallback Mode")
            print("4. Back to Main Menu")
            
            subchoice = input("Enter your choice (1-4): ").strip()
            
            if subchoice == '1':
                print("\n--- Select Cohere Model ---")
                print("1. command-a-03-2025 (faster)")
                print("2. command-r-03-2025 (more capable)")
                model_choice = input("Enter your choice (1-2): ").strip()
                
                if model_choice == '1':
                    bot.config['cohere_model'] = 'command-a-03-2025'
                elif model_choice == '2':
                    bot.config['cohere_model'] = 'command-r-03-2025'
                else:
                    print("Invalid choice. Keeping current model.")
                    continue
                    
                bot.save_config()
                print(f"Model set to {bot.config['cohere_model']}")
            
            elif subchoice == '2':
                try:
                    timeout = int(input("Enter API timeout in seconds (5-60): ").strip())
                    if 5 <= timeout <= 60:
                        bot.config['api_timeout'] = timeout
                        bot.save_config()
                        print(f"API timeout set to {timeout} seconds")
                    else:
                        print("Invalid timeout. Must be between 5 and 60 seconds.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            elif subchoice == '3':
                current = bot.config.get('use_fallback_mode', True)
                bot.config['use_fallback_mode'] = not current
                bot.save_config()
                status = "enabled" if bot.config['use_fallback_mode'] else "disabled"
                print(f"Fallback mode {status}")
                
        elif choice == '7':
            bot.stop_scanning()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1-7.")

# Program entry point
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")