import PySimpleGUI as sg
import threading
import logging
import json
import os
from pathlib import Path

class AutoReplyGUI:
    """Graphical user interface for the AutoReplyPro application"""
    
    def __init__(self, config_manager, ai_engine, ui_controller):
        self.config_manager = config_manager
        self.ai_engine = ai_engine
        self.ui_controller = ui_controller
        
        self.running = False
        self.thread = None
        self.window = None
        
        # Set theme - using a try/except to handle older PySimpleGUI versions
        try:
            sg.theme('LightGrey1')
        except AttributeError:
            # Older versions of PySimpleGUI use ChangeLookAndFeel instead of theme
            try:
                sg.ChangeLookAndFeel('LightGrey1')
            except:
                logging.warning("Could not set PySimpleGUI theme - using default")
        
        # Load saved config
        self.config = self.config_manager.load_config()
    
    def create_layout(self):
        """Create the GUI layout"""
        # API Key Section
        api_frame = [
            [sg.Text("Cohere API Key:")], 
            [sg.Input(self.config.get('api_key', ''), key='-API_KEY-', password_char='*', size=(40, 1))],
            [sg.Button("Test API Connection", key='-TEST_API-')]
        ]
        
        # Persona Settings
        persona_frame = [
            [sg.Text("Your Name:"), sg.Input(self.config.get('persona_name', 'Nitesh'), key='-PERSONA_NAME-', size=(20, 1))],
            [sg.Text("Language Mix:"), 
             sg.Combo(['Hindi-English', 'English', 'Hindi', 'Nepali-Hindi-English'], 
                      default_value=self.config.get('language_mix', 'Hindi-English'), 
                      key='-LANGUAGE_MIX-', size=(20, 1))],
            [sg.Text("Response Tone:"), 
             sg.Combo(['warm', 'professional', 'casual', 'funny'], 
                      default_value=self.config.get('tone', 'warm'), 
                      key='-TONE-', size=(20, 1))],
            [sg.Text("Max Response Length:"), 
             sg.Slider(range=(10, 50), default_value=self.config.get('max_length', 20), 
                      orientation='h', key='-MAX_LENGTH-', size=(20, 15))],
            [sg.Text("Temperature (Creativity):"), 
             sg.Slider(range=(0.1, 1.0), resolution=0.1, default_value=self.config.get('temperature', 0.8), 
                      orientation='h', key='-TEMPERATURE-', size=(20, 15))]
        ]
        
        # Platform Settings
        platform_frame = [
            [sg.Text("Messaging Platform:"), 
             sg.Combo(['WhatsApp', 'Telegram', 'Facebook Messenger'], 
                      default_value=self.config.get('platform', 'WhatsApp'), 
                      key='-PLATFORM-', size=(20, 1), enable_events=True)],
            [sg.Text("Check Interval (seconds):"), 
             sg.Slider(range=(1, 30), default_value=self.config.get('check_interval', 5), 
                      orientation='h', key='-CHECK_INTERVAL-', size=(20, 15))],
            [sg.Button("Setup UI Recognition", key='-SETUP_UI-')]
        ]
        
        # Control Buttons
        control_buttons = [
            [sg.Button("Start Auto-Reply", key='-START-', size=(15, 1), button_color=('white', 'green')),
             sg.Button("Stop", key='-STOP-', size=(15, 1), button_color=('white', 'red'), disabled=True)],
            [sg.Button("Save Settings", key='-SAVE-', size=(15, 1)),
             sg.Button("Exit", key='-EXIT-', size=(15, 1))]
        ]
        
        # Logs Area
        log_frame = [
            [sg.Text("Activity Log:")],
            [sg.Multiline(size=(60, 10), key='-LOG-', autoscroll=True, disabled=True)],
            [sg.Checkbox("Show debug messages", default=self.config.get('show_debug', False), key='-SHOW_DEBUG-')]
        ]
        
        # Combine all elements
        layout = [
            [sg.Text("AutoReplyPro", font=("Helvetica", 16))],
            [sg.Column([
                [sg.Frame("API Settings", api_frame, size=(300, 100))],
                [sg.Frame("Persona Settings", persona_frame, size=(300, 200))],
                [sg.Frame("Platform Settings", platform_frame, size=(300, 150))]
            ]), 
            sg.Column([
                [sg.Frame("Controls", control_buttons, size=(300, 100))],
                [sg.Frame("Logs", log_frame, size=(300, 250))]
            ])],
            [sg.Text("Status: Ready", key='-STATUS-')]
        ]
        
        return layout
    
    def run(self):
        """Create and run the GUI application"""
        layout = self.create_layout()
        self.window = sg.Window('AutoReplyPro', layout, finalize=True)
        
        # Set up custom logging handler to redirect to the GUI
        log_handler = GUILogHandler(self.window)
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', 
                                         datefmt='%H:%M:%S')
        log_handler.setFormatter(log_formatter)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        root_logger.addHandler(log_handler)
        
        # Log startup message
        logging.info("AutoReplyPro started")
        
        # Initialize API if key is present
        if self.config.get('api_key'):
            self.ai_engine.initialize_client(self.config['api_key'])
        
        # Set platform
        self.ui_controller.set_platform(self.config.get('platform', 'WhatsApp').lower())
        
        # Main event loop
        while True:
            event, values = self.window.read(timeout=100)
            
            # Handle exit events
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                self.stop_auto_reply()
                break
                
            # Handle button events
            elif event == '-TEST_API-':
                self.test_api_connection(values['-API_KEY-'])
                
            elif event == '-SETUP_UI-':
                self.setup_ui_recognition(values['-PLATFORM-'])
                
            elif event == '-START-':
                self.start_auto_reply(values)
                
            elif event == '-STOP-':
                self.stop_auto_reply()
                
            elif event == '-SAVE-':
                self.save_settings(values)
                
            elif event == '-PLATFORM-':
                # Update platform in UI controller when changed
                self.ui_controller.set_platform(values['-PLATFORM-'].lower())
                
            # Update log visibility based on debug checkbox
            if values and '-SHOW_DEBUG-' in values:
                log_handler.show_debug = values['-SHOW_DEBUG-']
        
        if self.window:
            self.window.close()
    
    def test_api_connection(self, api_key):
        """Test the connection to the Cohere API"""
        logging.info("Testing API connection...")
        if self.ai_engine.initialize_client(api_key):
            logging.info("✅ API connection successful!")
            self.window['-STATUS-'].update("Status: API connected")
        else:
            logging.error("❌ API connection failed. Check your API key and internet connection.")
            self.window['-STATUS-'].update("Status: API connection failed")
    
    def setup_ui_recognition(self, platform):
        """Guide the user through setting up UI recognition for their platform"""
        platform_lower = platform.lower()
        
        # Create assets directory if it doesn't exist
        assets_dir = Path("assets")
        assets_dir.mkdir(exist_ok=True)
        
        instructions = [
            f"We'll now set up image recognition for {platform}.",
            "This will help the app find elements on your screen.",
            "\n1. First, we'll capture the app icon."
        ]
        
        sg.popup('\n'.join(instructions), title="UI Setup Instructions")
        
        # Capture app icon
        if sg.popup_yes_no(f"Open {platform} if it's not already open.\n\nThen click Yes when ready to capture the app icon.", 
                           title="Capture App Icon") == "Yes":
            self.capture_screen_region(f"{platform_lower}_icon", "Select the app icon")
        
        # Capture message box
        if sg.popup_yes_no(f"Now, we'll capture the message input box in {platform}.\n\nClick Yes when ready.", 
                           title="Capture Message Box") == "Yes":
            self.capture_screen_region(f"{platform_lower}_message_box", "Select the message input box")
        
        # Capture chat area
        if sg.popup_yes_no(f"Finally, we'll capture the chat area in {platform}.\n\nClick Yes when ready.", 
                           title="Capture Chat Area") == "Yes":
            self.capture_screen_region(f"{platform_lower}_chat_area", "Select the main chat area")
        
        sg.popup("Setup completed! The app can now recognize the UI elements.", title="Setup Complete")
    
    def capture_screen_region(self, image_name, instruction):
        """Helper to capture a specific region of the screen"""
        # First, hide the window temporarily
        self.window.hide()
        
        try:
            # Create a simple GUI for selection
            layout = [[sg.Text(f"{instruction}, then press Enter")]]
            select_window = sg.Window("Select Region", layout, no_titlebar=True, keep_on_top=True, 
                                     location=(10, 10), finalize=True)
            
            # Wait for a moment to let user read instructions
            select_window.read(timeout=2000)
            select_window.close()
            
            # Use PyAutoGUI to select region
            logging.info(f"Click and drag to select the {image_name} region...")
            try:
                x1, y1, x2, y2 = self.get_region_from_user()
                if x1 is not None:
                    # Capture the region
                    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                    save_path = f"assets/{image_name}.png"
                    screenshot.save(save_path)
                    logging.info(f"✅ Captured and saved {image_name} to {save_path}")
                else:
                    logging.warning(f"❌ Failed to capture {image_name}")
            except Exception as e:
                logging.error(f"Error capturing region: {str(e)}")
        finally:
            # Show the main window again
            self.window.un_hide()
    
    def get_region_from_user(self):
        """Get a screen region selection from the user"""
        try:
            # Use PyAutoGUI's built-in selection method if available
            region = pyautogui.screenshot()
            x1, y1, width, height = pyautogui.dragTo()
            return x1, y1, x1 + width, y1 + height
        except:
            # Fallback method if dragTo is not working
            from pynput import mouse
            
            coords = []
            
            def on_click(x, y, button, pressed):
                if pressed and button == mouse.Button.left:
                    coords.append((x, y))
                    if len(coords) == 2:
                        return False  # Stop listener
            
            # Start listener
            with mouse.Listener(on_click=on_click) as listener:
                listener.join()
            
            if len(coords) == 2:
                x1, y1 = coords[0]
                x2, y2 = coords[1]
                return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
            return None, None, None, None
    
    def start_auto_reply(self, values):
        """Start the auto-reply process in a separate thread"""
        if self.running:
            logging.warning("Auto-reply is already running")
            return
            
        # Update UI
        self.window['-START-'].update(disabled=True)
        self.window['-STOP-'].update(disabled=False)
        self.window['-STATUS-'].update("Status: Running")
        
        # Save current settings
        self.save_settings(values)
        
        # Initialize necessary components
        api_key = values['-API_KEY-']
        if not self.ai_engine.initialize_client(api_key):
            logging.error("Failed to initialize AI engine. Please check your API key.")
            self.window['-START-'].update(disabled=False)
            self.window['-STOP-'].update(disabled=True)
            self.window['-STATUS-'].update("Status: Error - API initialization failed")
            return
            
        # Set up platform
        self.ui_controller.set_platform(values['-PLATFORM-'].lower())
        
        # Start the thread
        self.running = True
        self.thread = threading.Thread(target=self.auto_reply_worker, args=(values,), daemon=True)
        self.thread.start()
        
        logging.info("✅ Auto-reply started")
    
    def stop_auto_reply(self):
        """Stop the auto-reply process"""
        if not self.running:
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
            self.thread = None
            
        # Update UI
        if self.window:
            self.window['-START-'].update(disabled=False)
            self.window['-STOP-'].update(disabled=True)
            self.window['-STATUS-'].update("Status: Stopped")
            
        logging.info("Auto-reply stopped")
    
    def save_settings(self, values):
        """Save current settings to configuration file"""
        if not values:
            return
            
        config = {
            'api_key': values['-API_KEY-'],
            'persona_name': values['-PERSONA_NAME-'],
            'language_mix': values['-LANGUAGE_MIX-'],
            'tone': values['-TONE-'],
            'max_length': int(values['-MAX_LENGTH-']),
            'temperature': float(values['-TEMPERATURE-']),
            'platform': values['-PLATFORM-'],
            'check_interval': int(values['-CHECK_INTERVAL-']),
            'show_debug': values['-SHOW_DEBUG-']
        }
        
        self.config_manager.save_config(config)
        logging.info("Settings saved")
    
    def auto_reply_worker(self, values):
        """Worker function for the auto-reply thread"""
        try:
            # Extract settings
            persona_name = values['-PERSONA_NAME-']
            language_mix = values['-LANGUAGE_MIX-']
            tone = values['-TONE-']
            max_length = int(values['-MAX_LENGTH-'])
            temperature = float(values['-TEMPERATURE-'])
            check_interval = int(values['-CHECK_INTERVAL-'])
            
            # Open the messaging app
            if not self.ui_controller.open_messaging_app():
                logging.error(f"Failed to open {values['-PLATFORM-']}. Stopping auto-reply.")
                self.running = False
                self.window.write_event_value('-STOP-', None)
                return
                
            # Initialize variables for message tracking
            previous_last_message = ""
            previous_reply = ""
            
            # Main loop
            while self.running:
                try:
                    # Copy current chat text
                    current_chat_text = self.ui_controller.copy_chat_text()
                    if not current_chat_text:
                        time.sleep(1)
                        continue
                        
                    # Extract last message
                    current_last_message = self.ui_controller.get_last_message(current_chat_text)
                    
                    # Check if there's a new message from someone else
                    if (current_last_message and 
                        current_last_message != previous_last_message and 
                        self.ui_controller.is_message_from_other_person(current_last_message, persona_name)):
                        
                        logging.info(f"New message detected: {current_last_message[:30]}...")
                        
                        # Generate response
                        reply = self.ai_engine.generate_response(
                            current_chat_text, 
                            persona_name=persona_name,
                            language_mix=language_mix,
                            tone=tone,
                            max_length=max_length,
                            temperature=temperature
                        )
                        
                        # Send the response if it's new
                        if reply and reply != previous_reply:
                            logging.info(f"Sending response: {reply[:30]}...")
                            if self.ui_controller.send_message(reply):
                                previous_reply = reply
                                logging.info("Response sent successfully")
                            else:
                                logging.error("Failed to send response")
                                
                        # Update previous message
                        previous_last_message = current_last_message
                    
                    # Wait before next check
                    time.sleep(check_interval)
                    
                except Exception as e:
                    logging.error(f"Error in auto-reply loop: {str(e)}")
                    time.sleep(check_interval)
                    
        except Exception as e:
            logging.error(f"Auto-reply worker error: {str(e)}")
        finally:
            # Ensure UI is updated when thread ends
            if self.window:
                self.window.write_event_value('-STOP-', None)


class GUILogHandler(logging.Handler):
    """Custom logging handler that redirects logs to the GUI"""
    
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.show_debug = False
    
    def emit(self, record):
        """Process a log record and output to GUI"""
        # Skip debug messages unless show_debug is enabled
        if record.levelno == logging.DEBUG and not self.show_debug:
            return
            
        # Format the log message
        log_entry = self.format(record)
        
        # Add color indicators based on level
        if record.levelno >= logging.ERROR:
            prefix = "❌ "
        elif record.levelno >= logging.WARNING:
            prefix = "⚠️ "
        elif record.levelno >= logging.INFO:
            prefix = "ℹ️ "
        else:
            prefix = "🔍 "
            
        log_entry = f"{prefix}{log_entry}"
        
        # Update the GUI log element
        if self.window:
            try:
                current_log = self.window['-LOG-'].get()
                self.window['-LOG-'].update(f"{current_log}\n{log_entry}" if current_log else log_entry)
            except:
                # Window might be closed or element not available
                pass