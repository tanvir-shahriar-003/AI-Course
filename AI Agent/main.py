import google.generativeai as genai
import time
import json
from datetime import datetime

# ==============================================
# 🔑 Gemini API Key (Use your own API key here)
# ==============================================
genai.configure(api_key="AIzaSyDu7LVXlbiD4Baw1ArrskjILZZ74WftqeQ")

# ==============================================
# 🧠 Memory System
# ==============================================
class ConversationMemory:
    def __init__(self, max_messages=20):
        self.conversation_history = []
        self.max_messages = max_messages
        self.user_context = {}  # Stores user preferences, topics of interest, etc.
    
    def add_message(self, role, content, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp
        }
        
        self.conversation_history.append(message)
        
        # Keep only the most recent messages
        if len(self.conversation_history) > self.max_messages:
            self.conversation_history.pop(0)
    
    def get_recent_context(self, num_messages=5):
        """Get recent conversation context for the AI"""
        recent = self.conversation_history[-num_messages:] if self.conversation_history else []
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
        return context
    
    def update_user_context(self, key, value):
        """Update user preferences or context"""
        self.user_context[key] = value
    
    def get_conversation_summary(self):
        """Generate a brief summary of the conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        topics = set()
        for msg in self.conversation_history:
            content = msg['content'].lower()
            # Simple topic extraction (can be enhanced)
            if "weather" in content:
                topics.add("weather")
            if "programming" in content or "code" in content:
                topics.add("programming")
            if "music" in content or "song" in content:
                topics.add("music")
            if "food" in content or "restaurant" in content:
                topics.add("food")
        
        return f"Conversation topics: {', '.join(topics) if topics else 'Various topics'}"

# ==============================================
# 🔍 Advanced Analytical Function
# ==============================================
def advanced_analysis(prompt, conversation_memory):
    """Perform deep analysis on user queries with context awareness"""
    
    # Get recent conversation context
    context = conversation_memory.get_recent_context(3)
    
    analysis_prompt = f"""
    Based on the following conversation context and the current query, provide a comprehensive analysis.

    RECENT CONVERSATION CONTEXT:
    {context}

    CURRENT QUERY: {prompt}

    Please provide an analysis that includes:
    1. **Intent Analysis**: What is the user trying to achieve or learn?
    2. **Context Connection**: How does this relate to previous conversation topics?
    3. **Depth Assessment**: Is this a simple query or does it require complex reasoning?
    4. **Recommendations**: What additional information or perspectives might be helpful?
    5. **Potential Follow-ups**: What related questions might the user have next?

    Format your response clearly with these sections.
    """
    
    return analysis_prompt

# ==============================================
# 🤖 Enhanced Gemini Chat Function
# ==============================================
def chat_with_gemini(prompt, conversation_memory=None, analysis_mode=False, retries=3):
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Prepare enhanced prompt with memory context
    enhanced_prompt = prompt
    
    if conversation_memory and conversation_memory.conversation_history:
        context = conversation_memory.get_recent_context(3)
        context_prompt = f"""
        Previous conversation context:
        {context}
        
        Current message: {prompt}
        
        Please respond naturally, considering the conversation history while focusing on the current message.
        """
        enhanced_prompt = context_prompt
    
    # Use analytical function if requested
    if analysis_mode:
        enhanced_prompt = advanced_analysis(prompt, conversation_memory)
        print("🔍 Analysis Mode Activated...")

    for attempt in range(retries):
        try:
            response = model.generate_content(enhanced_prompt)
            return response.text

        except Exception as e:
            error_msg = str(e)

            # Handle rate limit
            if "429" in error_msg or "quota" in error_msg:
                print("⚠ Rate limit hit, retrying...")
                time.sleep(2)
                continue

            return f"Error: {e}"

    return "Error: Please try again later."

# ==============================================
# 🚀 Enhanced Main Program
# ==============================================
def main():
    # Initialize memory system
    memory = ConversationMemory()
    
    print("🤖 Hi! I am Ai agent you made for your AI Lab!")
    print("💭 I can remember our conversation and provide deep analysis.")
    print("\nSpecial commands:")
    print("  - 'analysis [your question]' - Get detailed analysis")
    print("  - 'memory' - Show conversation summary")
    print("  - 'clear' - Clear conversation memory")
    print("  - 'stop' or 'exit' - Quit the program\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["stop", "exit", "quit", "bye"]:
            print("AI: Goodbye! It was great talking with you!")
            break
        
        elif user_input.lower() == "memory":
            summary = memory.get_conversation_summary()
            print(f"AI: Conversation Summary: {summary}")
            print(f"AI: Total messages exchanged: {len(memory.conversation_history)}")
            continue
        
        elif user_input.lower() == "clear":
            memory.conversation_history.clear()
            memory.user_context.clear()
            print("AI: Conversation memory cleared!")
            continue
        
        elif user_input.lower().startswith("analysis "):
            # Analysis mode
            analysis_query = user_input[9:]  # Remove "analysis " prefix
            memory.add_message("user", f"ANALYSIS REQUEST: {analysis_query}")
            
            ai_reply = chat_with_gemini(analysis_query, memory, analysis_mode=True)
            print("\n🔍 ANALYSIS RESULT:")
            print("AI:", ai_reply)
            print("=" * 50)
            
            memory.add_message("assistant", f"ANALYSIS: {ai_reply}")
        
        else:
            # Normal chat mode
            memory.add_message("user", user_input)
            
            ai_reply = chat_with_gemini(user_input, memory)
            print("AI:", ai_reply)
            
            memory.add_message("assistant", ai_reply)

if __name__ == "__main__":
    main()
