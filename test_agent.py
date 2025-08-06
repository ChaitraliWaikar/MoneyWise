import google.generativeai as genai
import os
from dotenv import load_dotenv
from agents import FinancialLiteracyAgent, BudgetingAgent

load_dotenv()

def check_available_models():
    """
    Helper function to check which models are available
    """
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        print("Available Gemini models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"✓ {model.name}")
            else:
                print(f"✗ {model.name} (doesn't support generateContent)")
    except Exception as e:
        print(f"Error checking models: {e}")

def test_agents():
    """
    Test function to verify agents are working correctly
    """
    try:
        print("Testing Financial Literacy Agent...")
        literacy_agent = FinancialLiteracyAgent()
        response = literacy_agent.provide_info("emergency fund")
        print(f"Response: {response[:100]}...")
        
        print("\nTesting Budgeting Agent...")
        budgeting_agent = BudgetingAgent()
        feedback = budgeting_agent.analyze_and_suggest(5000, 2500, 1500, 1000)
        print(f"Feedback: {feedback[:100]}...")
        
        print("Both agents working correctly!")
        
    except Exception as e:
        print(f"Error testing agents: {e}")

if __name__ == "__main__":
    print("Checking available models first...")
    check_available_models()
    print("\nNow testing agents...")
    test_agents()