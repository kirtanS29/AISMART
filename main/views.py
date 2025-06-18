from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def home_view(request):
    return render(request, 'main/home.html')

@login_required
def dashboard_view(request):
    return render(request, 'main/dashboard.html')


import os
from django.shortcuts import render
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create model instance (can also be gemini-1.5-pro or gemini-1.5-flash)
model = genai.GenerativeModel('gemini-1.5-flash')  # ✅ correct




from textblob import TextBlob
from .models import ChatHistory

@login_required
def chatbot_view(request):
    response_text = ""
    history = []

    if request.method == 'POST':
        user_message = request.POST.get('message')

        # Call Gemini model
        try:
            gemini_response = model.generate_content(user_message)
            response_text = gemini_response.text

            # Sentiment Analysis
            blob = TextBlob(user_message)
            sentiment = blob.sentiment.polarity
            if sentiment > 0:
                sentiment_label = 'Positive'
            elif sentiment < 0:
                sentiment_label = 'Negative'
            else:
                sentiment_label = 'Neutral'

            # Save to database
            ChatHistory.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=response_text,
                sentiment=sentiment_label
            )

        except Exception as e:
            response_text = f"Error: {str(e)}"

    # Fetch user history
    if request.user.is_authenticated:
        history = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')[:10]

    return render(request, 'main/chatbot.html', {
        'response': response_text,
        'history': history
    })


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@login_required
def recommender_view(request):
    session = request.session
    if "chat_history" not in session:
        session["chat_history"] = ""

    ai_response = None

    if request.method == "POST":
        user_msg = request.POST.get("message",'').strip()
        session["chat_history"] += f"\nUser: {user_msg}"

        prompt = f"""
You are a helpful AI assistant. Here is the conversation so far:
{session['chat_history']}

1. Understand the user's intent (what product they want).
2. Ask the next question logically (budget, use-case, feature) if needed.
3. Once criteria are clear, recommend 7 relevant products.
4. Ask if they want to refine or change any preference.
5. Keep responses conversational, not instruction-like.
6. you have to give final answer in table form with specification and approx cost and also model name and link to buy the product.
7.Try to suggest newer models and give the correct model names
8.try to ask questions one by one and wait for user response before suggesting products
"""

        resp = model.generate_content(prompt)
        ai_response = resp.text.strip()
        session["chat_history"] += f"\nAI: {ai_response}"

        # Save when AI proactively recommends products
        if any(keyword in ai_response.lower() for keyword in ("here are", "i recommend", "suggesting", "my top")):
            from .models import Recommendation
            Recommendation.objects.create(
                user=request.user,
                parameters=session["chat_history"],
                recommended_products=ai_response
            )

        session.modified = True

    return render(request, "main/recommendation.html", {
        "chat_history": session["chat_history"],
        "response": ai_response
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import LifeAdvice  # Create this model

@login_required
def life_advice_view(request):
    session = request.session
    if "life_chat" not in session:
        session["life_chat"] = ""

    ai_response = None

    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()
        session["life_chat"] += f"\nUser: {user_msg}"

        prompt = f"""
You are a compassionate AI counselor helping with life issues and recommend practical solution to any problem.
Here is the ongoing chat:
{session['life_chat']}

Give empathetic, human-like responses.
- Recognize the emotional state.
- Ask questions to clarify the situation if needed.
- Offer 4–5 practical steps the user can take.
- End with a positive motivational quote or thought.
- Keep responses conversational, not like a textbook.

Respond now:
"""

        resp = model.generate_content(prompt)  # Gemini or other LLM
        ai_response = resp.text.strip()
        session["life_chat"] += f"\nAI: {ai_response}"

        LifeAdvice.objects.create(user=request.user, message=user_msg, advice=ai_response)
        session.modified = True

    return render(request, "main/life_advice.html", {
        "chat_history": session["life_chat"],
        "response": ai_response
    })
