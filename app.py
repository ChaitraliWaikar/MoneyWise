from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-dev-key')

# Import and initialize agents
try:
    from agents import FinancialLiteracyAgent, BudgetingAgent
    literacy_agent = FinancialLiteracyAgent()
    budgeting_agent = BudgetingAgent()
    agents_ready = True
except Exception as e:
    print(f"Error initializing agents: {e}")
    literacy_agent = None
    budgeting_agent = None
    agents_ready = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/literacy', methods=['GET', 'POST'])
def literacy():
    response = ""
    if request.method == 'POST':
        topic = request.form.get('topic')
        if not topic:
            response = "Please enter a topic."
        elif not agents_ready or not literacy_agent:
            response = "AI agent is not available. Check API configuration."
        else:
            try:
                response = literacy_agent.provide_info(topic)
            except Exception as e:
                response = f"Error generating response: {str(e)}"
    return render_template('literacy.html', response=response)


@app.route('/budgeting', methods=['GET', 'POST'])
def budgeting():
    feedback = ""
    if request.method == 'POST':
        try:
            income = float(request.form.get('income', 0))
            needs = float(request.form.get('needs', 0))
            wants = float(request.form.get('wants', 0))
            savings_debt = float(request.form.get('savings_debt', 0))

            if not agents_ready or not budgeting_agent:
                feedback = "AI agent is not available. Check API configuration."
            else:
                feedback = budgeting_agent.analyze_and_suggest(income, needs, wants, savings_debt)
        except ValueError:
            feedback = "Please enter valid numerical values."
        except Exception as e:
            feedback = f"An error occurred: {str(e)}"
    return render_template('budgeting.html', feedback=feedback)


@app.route('/test')
def test():
    return "<h1>Flask is working!</h1>"


@app.route('/test-gemini')
def test_gemini():
    if agents_ready and literacy_agent:
        try:
            response = literacy_agent.provide_info("How should a student manage money?")
            return f"<h2>Gemini Test Success:</h2><pre>{response}</pre>"
        except Exception as e:
            return f"<h2>Test Error:</h2><p>{str(e)}</p>"
    return "<h2>Gemini Test Failed:</h2><p>Agents not available</p>"


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - Page Not Found</h1><p><a href='/'>Home</a></p>", 404


@app.errorhandler(500)
def internal_error(e):
    return "<h1>500 - Internal Server Error</h1>", 500


if __name__ == '__main__':
    print("Starting MoneyWise Flask app...")
    print(f"AI agents: {'Ready' if agents_ready else 'Not ready'}")
    app.run(debug=True, host='127.0.0.1', port=5000)
