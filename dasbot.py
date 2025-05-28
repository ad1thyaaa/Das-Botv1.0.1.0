import responses
import datetime
import pytz
import requests
import random
from responses import WORD_LIST

DEFAULT_CITY = "Thrissur"
DEFAULT_COUNTRY = "India"
DEFAULT_TIMEZONE = "Asia/Kolkata"

context = {
    "awaiting_city": False,
    "awaiting_timezone": False,
    "awaiting_repeat": False,
    "game_active": False,
    "game_word": None,
    "game_hint": None,
}

def get_word():
    return random.choice(WORD_LIST)

def get_weather(city=DEFAULT_CITY, country=DEFAULT_COUNTRY):
    try:
        url = f"http://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()

        current = data['current_condition'][0]
        desc = current['weatherDesc'][0]['value']
        temp_c = current['temp_C']

        return f"{desc}, {temp_c}°C"
    except Exception:
        return "Hmm... couldn’t fetch the weather right now."

def get_time(timezone=DEFAULT_TIMEZONE):
    try:
        zone = pytz.timezone(timezone)
        now = datetime.datetime.now(zone)
        return now.strftime("The current time is %H:%M %p")
    except Exception:
        return "Couldn't fetch time for that timezone."

def start_game():
    word = get_word()
    revealed = [word[0]] + ["_"] * (len(word) - 2) + [word[-1]]
    context["game_active"] = True
    context["game_word"] = word
    context["game_hint"] = revealed
    context["revealed_indices"] = [0, len(word) - 1]
    context["game_attempts"] = 0
    context["hint_count"] = 0
    context["max_attempts"] = len(word) - 1

    return f"Let's play 'Guess the Word'! Guess this word: {''.join(revealed)}, type:hint to get a hint."

def guess_word(guess):
    if not context.get("game_active"):
        return "No active game. Type 'play game' to start one!"

    word = context["game_word"]
    hint = context["game_hint"]
    guess = guess.strip().lower()

    if guess in ["hint", "give a hint", "help", "clue", "show hint"]:
        if context["hint_count"] >= 3:
            return f"No more hints left! Here's what you have: {''.join(hint)}"

        unrevealed = [i for i in range(len(word)) if i not in context["revealed_indices"]]
        if unrevealed:
            reveal_index = random.choice(unrevealed)
            hint[reveal_index] = word[reveal_index]
            if reveal_index not in context["revealed_indices"]:
                context["revealed_indices"].append(reveal_index)
            context["hint_count"] += 1
            return f"Hint {context['hint_count']}/3: {''.join(hint)}"
        else:
            return "All letters are already revealed!"

    if guess == "quit":
        context["game_active"] = False
        return f"Game ended. The word was '{word}'. Type 'play game' to start again."

    if len(guess) != len(word):
        return f"Your guess should be {len(word)} letters long. Try again."

    context["game_attempts"] += 1

    if guess == word:
        context["game_active"] = False
        return "Correct! You're awesome! 🎉 Type 'play game' to play again."

    if context["game_attempts"] >= context["max_attempts"]:
        context["game_active"] = False
        return f"Out of attempts! The word was '{word}'. Type 'play game' to try again."

    return f"Oops! That's not it. Try again! Hint: {''.join(hint)} Attempts left: {context['max_attempts'] - context['game_attempts']}"

def is_no_location_input(text):
    text = text.lower()
    no_location_phrases = [
        "don't know", "dont know", "idk", "i don't know", "uhh",
        "no idea", "none", "not sure", "don't remember", "dunno", "skip"
    ]
    return any(phrase in text for phrase in no_location_phrases)

def get_bot_response(message):
    global context
    msg = message.strip().lower()
    
    print(f"DEBUG: game_active = {context['game_active']}, received message: '{msg}'")
    # Special command handling
    if msg == "!how to talk with das":
        # Collect all unique responses from responses.py
        all_responses = set()
        # Assuming responses.KEYWORDS_RESPONSES is a dict of lists of replies
        if hasattr(responses, "KEYWORDS_RESPONSES"):
            for responses_list in responses.KEYWORDS_RESPONSES.values():
                all_responses.update(responses_list)
        # Add other response lists you want to include:
        if hasattr(responses, "DEFAULT_RESPONSES"):
            all_responses.update(responses.DEFAULT_RESPONSES)
        if hasattr(responses, "OK_RESPONSES"):
            all_responses.update(responses.OK_RESPONSES)
        
        return "Here's what I can say:\n- " + "\n- ".join(sorted(all_responses))

    if "how to talk with you" in msg or "how to talk with das" in msg:
        return 'Type in "!how to talk with das" and you can get to know about me more!!'

    # If waiting for city input after user asked weather
    if context.get("awaiting_city"):
        city_country = message.strip()
        context["awaiting_city"] = False
        if is_no_location_input(city_country):
            return "Since you didn’t give any city, here’s the weather at my city:\n" + get_weather()
        else:
            city = city_country.split(',')[0].strip()
            weather_report = get_weather(city)
            if weather_report is None:
                return "You sure this city exists on Earth?? This city is not from Earth, where are you from?"
            else:
                return weather_report

    # If waiting for timezone input
    if context.get("awaiting_timezone"):
        tz = message.strip().lower()
        context["awaiting_timezone"] = False
        unknown_inputs = ["don't know", "dont know", "idk", "no idea", "not sure", "no clue"]
        if not tz or any(phrase in tz for phrase in unknown_inputs):
            return "No worries! Here’s my time zone info:\n" + get_time(DEFAULT_TIMEZONE)
        else:
            return get_time(tz)

    # If waiting for repeat text
    if context.get("awaiting_repeat"):
        to_repeat = message.strip()
        context["awaiting_repeat"] = False
        return to_repeat

    if context.get("game_active"):
        return guess_word(msg)
    
    # Normal response flow
    reply = responses.find_response(message)

    if reply == "weather":
        context["awaiting_city"] = True
        return "Which city are you in? (e.g., Thrissur)"
    elif reply == "time":
        context["awaiting_timezone"] = True
        return "Which timezone are you in? (e.g., Asia/Kolkata)"
    elif reply == "repeat":
        context["awaiting_repeat"] = True
        return "What should I repeat?"
    elif reply == "game":
        return start_game()
   
    else:
        return reply

def main():
    print("Hello! I’m Das. Let’s chat!")
    farewell_keywords = [
        "bye", "goodbye", "byebye", "exit", "see ya",
        "see you", "farewell", "take care"
    ]

    while True:
        user_input = input("You: ").strip().lower()

        if any(farewell in user_input for farewell in farewell_keywords):
            print("Das: Take care! Have a nice day!")
            break

        bot_reply = get_bot_response(user_input)
        print("Das:", bot_reply)

if __name__ == "__main__":
    main()