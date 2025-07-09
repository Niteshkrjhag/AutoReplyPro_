import cohere
import logging

class AIEngine:
    """Handles AI-powered response generation using Cohere API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.client = None
        if api_key:
            self.initialize_client(api_key)
    
    def initialize_client(self, api_key):
        """Initialize the Cohere client with the provided API key"""
        try:
            self.api_key = api_key
            self.client = cohere.Client(api_key)
            return True
        except Exception as e:
            logging.error(f"Failed to initialize Cohere client: {str(e)}")
            return False
    
    def generate_response(self, chat_history, persona_name="Nitesh", language_mix="Hindi-English", 
                          tone="warm", max_length=30, temperature=0.8):
        """Generate a contextually appropriate response based on chat history"""
        if not self.client:
            logging.error("Cohere client not initialized. Please set a valid API key.")
            return "Error: AI engine not initialized"
        
        # Create dynamic prompt based on user preferences
        prompt = self._create_prompt(chat_history, persona_name, language_mix, tone)
        
        try:
            response = self.client.generate(
                model='command-r-plus',
                prompt=prompt,
                max_tokens=max_length * 4,  # Approximate tokens based on word count
                temperature=temperature,
                stop_sequences=["\n"]
            )
            return response.generations[0].text.strip()
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return f"Sorry, I couldn't generate a response. Error: {str(e)[:50]}..."
    
    def _create_prompt(self, chat_history, persona_name, language_mix, tone):
        """Create a dynamic prompt based on user preferences"""
        
        language_guide = {
            "Hindi-English": "Use a mix of Hindi and English, with Hindi written in both Devanagari and Latin script.",
            "English": "Use fluent, natural English.",
            "Hindi": "Use primarily Hindi, written in both Devanagari and Latin script.",
            "Nepali-Hindi-English": "Mix Nepali, Hindi and English naturally, as appropriate."
        }
        
        tone_guide = {
            "warm": "warm, friendly, and affectionate",
            "professional": "polite, helpful, and professional",
            "casual": "casual, relaxed, and conversational",
            "funny": "humorous, light-hearted, and playful"
        }
        
        language_instruction = language_guide.get(language_mix, language_guide["Hindi-English"])
        tone_instruction = tone_guide.get(tone, tone_guide["warm"])
        
        prompt = f"""
        You are {persona_name}, responding to a chat message. {language_instruction}
        Your tone should be {tone_instruction}. Avoid any inappropriate language.
        
        Here is the chat history:
        {chat_history}

        Respond to the last message in a natural, human-like way. Keep your response 
        relatively short (around 20-30 words), contextually relevant, and make it sound 
        like a real person typing a message. 
        """
        
        # Add some example conversations to guide the model
        examples = self._get_example_conversations(language_mix)
        if examples:
            prompt += f"\n\nHere are some example conversations in your style:\n{examples}"
            
        return prompt
    
    def _get_example_conversations(self, language_mix):
        """Return example conversations based on selected language mix"""
        examples = {
            "Hindi-English": [
                {"input": "तुम क्या कर रहे हो?", "output": "कुछ खास नहीं, बस थोड़ा रिलैक्स कर रहा हूं। तुम बताओ, क्या चल रहा है?"},
                {"input": "How was your day?", "output": "Din achha tha! Thoda busy tha but productive raha. Tumhara kaisa tha?"},
                {"input": "Kya plan hai weekend ka?", "output": "Kuch khaas nahi socha, maybe thoda rest karunga. Tum batao, kuch interesting plan hai?"}
            ],
            "English": [
                {"input": "What are you up to?", "output": "Not much, just relaxing a bit. How about you?"},
                {"input": "I'm feeling a bit down today.", "output": "I'm sorry to hear that. Anything specific bothering you? I'm here if you want to talk."}
            ],
            "Hindi": [
                {"input": "आज का दिन कैसा रहा?", "output": "बहुत अच्छा! थोड़ा व्यस्त था लेकिन मज़ेदार रहा। आपका कैसा था?"},
                {"input": "क्या खा रहे हो?", "output": "अभी कुछ नहीं, सोच रहा हूँ कुछ हल्का सा बना लूँ। तुम बताओ?"}
            ]
        }
        
        selected_examples = examples.get(language_mix, examples["Hindi-English"])
        formatted_examples = "\n".join([f"Person: {ex['input']}\n{persona_name}: {ex['output']}" for ex in selected_examples])
        return formatted_examples