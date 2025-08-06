from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

# Load environment variables first
print("🔧 Loading environment variables...")
load_dotenv()
print(f"✅ Environment loaded. API key present: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")

# Initialize Flask app
print("🚀 Initializing Flask app...")
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-dev-key')
print("✅ Flask app initialized")

# Try to import and initialize agents
print("🤖 Importing agents...")
try:
    from agents import FinancialLiteracyAgent, BudgetingAgent
    print("✅ Agents imported successfully")
    
    print("🔧 Initializing FinancialLiteracyAgent...")
    literacy_agent = FinancialLiteracyAgent()
    print("✅ FinancialLiteracyAgent initialized")
    
    print("🔧 Initializing BudgetingAgent...")
    budgeting_agent = BudgetingAgent()
    print("✅ BudgetingAgent initialized")
    
    agents_ready = True
    print("🎉 All agents ready!")
    
except Exception as e:
    print(f"❌ Error initializing agents: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    literacy_agent = None
    budgeting_agent = None
    agents_ready = False

@app.route('/')
def index():
    print("📄 Serving index page...")
    return render_template('index.html')

@app.route('/literacy', methods=['GET', 'POST'])
def literacy():
    print(f"📝 Literacy route accessed - Method: {request.method}")
    response = ""
    
    if request.method == 'POST':
        topic = request.form.get('topic')
        print(f"📝 Topic received: {topic}")
        
        if topic and agents_ready and literacy_agent:
            try:
                print("🤖 Generating response...")
                response = literacy_agent.provide_info(topic)
                print(f"✅ Response generated: {len(response)} characters")
            except Exception as e:
                print(f"❌ Error generating response: {e}")
                response = f"Error generating response: {str(e)}"
        elif not agents_ready:
            response = "AI agent is not available. Please check your API configuration."
        else:
            response = "Please enter a topic to get information about."
    
    return render_template('literacy.html', response=response)

@app.route('/budgeting', methods=['GET', 'POST'])
def budgeting():
    print(f"💰 Budgeting route accessed - Method: {request.method}")
    feedback = ""
    
    if request.method == 'POST':
        try:
            income = float(request.form.get('income', 0))
            needs = float(request.form.get('needs', 0))
            wants = float(request.form.get('wants', 0))
            savings_debt = float(request.form.get('savings_debt', 0))
            
            print(f"💰 Budget data: Income=${income}, Needs=${needs}, Wants=${wants}, Savings=${savings_debt}")
            
            if agents_ready and budgeting_agent:
                print("🤖 Analyzing budget...")
                feedback = budgeting_agent.analyze_and_suggest(income, needs, wants, savings_debt)
                print(f"✅ Budget analysis completed: {len(feedback)} characters")
            else:
                feedback = "AI agent is not available. Please check your API configuration."
                
        except (ValueError, TypeError) as e:
            print(f"❌ Input error: {e}")
            feedback = "Please enter valid numerical values for all fields."
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            feedback = f"An error occurred: {str(e)}"
    
    return render_template('budgeting.html', feedback=feedback)

@app.route('/test')
def test():
    """Simple test route to check if Flask is working"""
    return "<h1>Flask is working! 🎉</h1><p>If you see this, your Flask app is running correctly.</p>"

@app.route('/test-gemini')
def test_gemini():
    print("🧪 Testing Gemini integration...")
    try:
        if agents_ready and literacy_agent:
            response = literacy_agent.provide_info("How should a student manage money?")
            return f"<h2>✅ Gemini Test Success:</h2><div style='padding:20px; background:#f0f0f0;'>{response}</div>"
        else:
            return "<h2>❌ Gemini Test Failed:</h2><p>AI agents not available</p>"
    except Exception as e:
        print(f"❌ Test error: {e}")
        return f"<h2>❌ Gemini Test Error:</h2><p>{str(e)}</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>Page Not Found</h1><p>Go back to <a href='/'>home</a></p>", 404

@app.errorhandler(500)
def internal_error(e):
    return f"<h1>Internal Server Error</h1><p>{str(e)}</p>", 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 STARTING FINANCIAL LITERACY APP")
    print("="*50)
    print(f"📁 Template folder: {app.template_folder}")
    print(f"🔑 Secret key: {'Configured' if app.secret_key else 'Missing'}")
    print(f"🤖 AI agents: {'Ready' if agents_ready else 'Error'}")
    print(f"🌐 URL: http://127.0.0.1:5000")
    print(f"🧪 Test URL: http://127.0.0.1:5000/test")
    print("="*50)
    
    try:
        print("🎯 Starting Flask development server...")
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")