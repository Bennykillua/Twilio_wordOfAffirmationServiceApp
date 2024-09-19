from flask import Flask, request, render_template
from twilio.rest import Client
import random
import openai
from openai import OpenAI

from dotenv import load_dotenv
import os

from openai import OpenAI
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
# openai.api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = Client(account_sid, auth_token)

# affirmations = [
#     "You are capable of amazing things!",
#     "You are enough!",
#     "You are loved!",
#     "You are strong!",
#     "You are doing great!",
#     "You are worthy of happiness!",
#     "You are a unique and special individual!"
# ]

# Function to generate a random affirmation
# def generate_affirmation():
#     return random.choice(affirmations)


# def generate_affirmation():
#     prompt = "Generate a word of affirmation."
#     response = openai.Completion.create(
#         engine="gpt-4o-mini", 
#         prompt=prompt,
#         max_tokens=50  
#     )
#     return response.choices[0].text.strip()

def generate_affirmation():
    messages = [
        {"role": "system", "content": "You are an affirmation generator."},
        {"role": "user", "content": "Generate a word of affirmation."}
    ]
    
    response = openai_client.chat.completions.create(
        model="gpt-4",  # You can experiment with different engines like GPT-3.5 Turbo or GPT-4o-mini
        messages=messages,
        max_tokens=50
    )
    
    return response.choices[0].message.content.strip()


# Example call
affirmationn = generate_affirmation()
print(affirmationn)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_affirmation', methods=['POST'])
def send_affirmation():
    recipient_number = request.form['phone_number']
    affirmation = generate_affirmation()

    try:
        message = client.messages.create(
            body=affirmation,
            from_=twilio_phone_number,
            to=recipient_number
        )
        return "Affirmation sent successfully!"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
