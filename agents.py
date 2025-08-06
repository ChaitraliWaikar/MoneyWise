import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FinancialLiteracyAgent:
    def __init__(self):
        # Configure Gemini AI
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Try to find a working model
        self.model = None
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro'
        ]
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                break
            except Exception as e:
                continue
        
        if not self.model:
            # Try to use the first available model
            try:
                for model in genai.list_models():
                    if 'generateContent' in model.supported_generation_methods:
                        try:
                            self.model = genai.GenerativeModel(model.name)
                            break
                        except:
                            continue
            except Exception as e:
                pass
        
        if not self.model:
            raise Exception("Could not initialize any Gemini model")
    
    def provide_info(self, topic):
        """
        Provide financial literacy information based on the user's topic
        """
        try:
            if not self.model:
                return "AI model not available. Please check your API key and internet connection."
            
            # Create a detailed prompt for financial literacy
            prompt = f"""
            You are a helpful financial literacy assistant. Please provide clear, practical, and educational information about: {topic}
            
            Guidelines:
            - Keep the response concise but informative (200-400 words)
            - Use simple language that's easy to understand
            - Include practical tips and examples when relevant
            - Focus on actionable advice
            - If the topic is too broad, provide an overview with key points
            - If the topic isn't related to financial literacy, politely redirect to financial topics
            
            Topic: {topic}
            """
            
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please try again."

class BudgetingAgent:
    def __init__(self):
        # Use the same initialization logic as FinancialLiteracyAgent
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Try to find a working model
        self.model = None
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro'
        ]
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                break
            except:
                continue
                
        if not self.model:
            try:
                for model in genai.list_models():
                    if 'generateContent' in model.supported_generation_methods:
                        try:
                            self.model = genai.GenerativeModel(model.name)
                            break
                        except:
                            continue
            except:
                pass
    
    def analyze_and_suggest(self, income, needs, wants, savings_debt):
        """
        Analyze budget allocation and provide suggestions
        """
        try:
            if not self.model:
                return "AI model not available. Please check your API key and internet connection."
                
            total_expenses = needs + wants + savings_debt
            remaining = income - total_expenses
            
            # Calculate percentages
            needs_percent = (needs / income) * 100 if income > 0 else 0
            wants_percent = (wants / income) * 100 if income > 0 else 0
            savings_percent = (savings_debt / income) * 100 if income > 0 else 0
            
            # Create detailed prompt for budget analysis
            prompt = f"""
            Analyze this budget and provide personalized financial advice:
            
            Monthly Income: ${income:,.2f}
            Needs (housing, food, utilities, etc.): ${needs:,.2f} ({needs_percent:.1f}%)
            Wants (entertainment, dining out, etc.): ${wants:,.2f} ({wants_percent:.1f}%)
            Savings/Debt Payment: ${savings_debt:,.2f} ({savings_percent:.1f}%)
            
            Remaining Money: ${remaining:,.2f}
            
            Please provide:
            1. An assessment of this budget allocation
            2. Specific recommendations for improvement
            3. Whether this follows the 50/30/20 rule (50% needs, 30% wants, 20% savings)
            4. Actionable tips for better financial management
            
            Keep the response practical and encouraging, around 250-350 words.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}. Please check your input values and try again."