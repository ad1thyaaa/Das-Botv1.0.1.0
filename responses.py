import random
import re

DEFAULT_RESPONSES = [
    "Hmm...", "Interesting...", "Go on...", "Tell me more.", "I see."
]

KEYWORDS_RESPONSES = {
    "purpose": ["I'm here to chat and keep you company!", "Just your friendly assistant!"],
    "made": ["I was created by Adithya!", "Das was made to talk and play!"],
    "day": ["I'm just a bunch of code, but I feel great!", "It's been a good day!"],
    "joke": ["You want a joke? I got tons!"],
    "repeat": ["Tell me what to repeat!"],
    "game": ["You wanna play a game? Sure!"],
    "weather": ["Let me check the weather..."],
    "time": ["I can fetch the time for you."],
    "bye": ["bye!", "see ya!", "take care!", "cya later!"],
    "goodbye": ["bye!", "see ya!", "take care!", "cya later!"],
    "byebye": ["bye!", "see ya!", "take care!", "cya later!"],
    # Added greetings
    "hi": ["Hey there!", "Hello!", "Hi! How can I help you?"],
    "hello": ["Hello!", "Hi there!", "Hey! What’s up?"],
    "hey": ["Hey!", "Hello!", "Hi!"],
}

OK_RESPONSES = ["alright what else?", "okie-dokie!", "sure thing!", "cool, tell me more."]

# Jokes list (unchanged)
JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field.",
    "Why don’t skeletons fight each other? They don’t have the guts.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why did the bicycle fall over? Because it was two-tired.",
    "I would tell you a joke about construction, but I’m still working on it.",
    "What do you call fake spaghetti? An impasta.",
    "Why was the math book sad? It had too many problems.",
    "What do you call cheese that isn’t yours? Nacho cheese.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I asked my dog what's two minus two. He said nothing.",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "Why can't your nose be 12 inches long? Because then it would be a foot.",
    "Why did the chicken join a band? Because it had the drumsticks.",
    "How do you organize a space party? You planet.",
    "I’m reading a book on anti-gravity. It’s impossible to put down.",
    "What do you call a fish wearing a bowtie? Sofishticated.",
    "What did the ocean say to the beach? Nothing, it just waved.",
    "How do you make holy water? You boil the hell out of it.",
    "I bought shoes from a drug dealer. I don’t know what he laced them with, but I was tripping.",
    "Did you hear about the restaurant on the moon? Great food, no atmosphere.",
    "What do you call an alligator in a vest? An investigator.",
    "Why don’t eggs tell jokes? They’d crack each other up.",
    "Why can't you hear a pterodactyl go to the bathroom? Because the 'P' is silent.",
    "I'm on a seafood diet. I see food and I eat it.",
    "What do you call a factory that makes okay products? A satisfactory.",
    "Why did the man put his money in the freezer? He wanted cold hard cash.",
    "What did one wall say to the other? I’ll meet you at the corner.",
    "Why don’t some couples go to the gym? Because some relationships don’t work out.",
    "Want to hear a joke about paper? Never mind, it’s tearable.",
    "Why was Cinderella so bad at soccer? Because she always ran away from the ball.",
    "Why do bees have sticky hair? Because they use honeycombs.",
    "What do you get when you cross a snowman with a vampire? Frostbite.",
    "Why don’t programmers like nature? Too many bugs.",
    "What’s orange and sounds like a parrot? A carrot.",
    "What’s brown and sticky? A stick.",
    "What do you call two birds in love? Tweethearts.",
    "What do you call a sleeping bull? A bulldozer.",
    "Why do cows wear bells? Because their horns don’t work.",
    "How do you find Will Smith in the snow? You look for fresh prints.",
    "Why don’t seagulls fly over the bay? Because then they’d be bagels.",
    "Why did the coffee file a police report? It got mugged.",
    "What do you call a belt made of watches? A waist of time.",
    "Why did the man run around his bed? Because he was trying to catch up on his sleep.",
    "Why are ghosts bad at lying? Because they are too transparent.",
    "Why did the tomato turn red? Because it saw the salad dressing.",
    "What do you get when you mix a joke with a rhetorical question?",
    "How does a penguin build its house? Igloos it together.",
    "Why do bicycles fall over? Because they are two-tired.",
    "What did the janitor say when he jumped out of the closet? Supplies!",
    "Why did the stadium get hot after the game? All the fans left.",
    "Why don’t elephants use computers? They’re afraid of the mouse.",
    "How do you catch a squirrel? Climb a tree and act like a nut.",
    "Why did the banana go to the doctor? It wasn’t peeling well.",
    "Why did the man get hit by a bike every day? Because he was stuck in a vicious cycle.",
    "What did one plate say to the other? Lunch is on me.",
    "Why can’t you give Elsa a balloon? Because she’ll let it go.",
    "What kind of music do mummies listen to? Wrap music.",
    "Why did the fish blush? Because it saw the ocean’s bottom.",
    "Why do pancakes always win at baseball? They have the best batter.",
    "Why are elevator jokes so good? They work on many levels.",
    "Why did the music teacher go to jail? Because she got caught with too many notes.",
    "What do you call a dog magician? A labracadabrador.",
    "How do cows stay up to date? They read the moos-paper.",
    "What do you get if you cross a cat with a dark horse? Kitty Perry.",
    "Why did the grape stop in the middle of the road? It ran out of juice.",
    "What kind of shoes does a thief wear? Sneakers.",
    "Why was the computer cold? It left its Windows open.",
    "Why did the skeleton go to the party alone? He had no body to go with.",
    "What did the zero say to the eight? Nice belt!",
    "Why did the cookie cry? Because his mom was a wafer too long.",
    "Why are frogs so happy? Because they eat whatever bugs them.",
    "How does a cucumber become a pickle? It goes through a jarring experience.",
    "Why do ducks have feathers? To cover their butt quacks.",
    "Why can’t a nose be 12 inches long? Because then it would be a foot.",
    "What do you call a pile of cats? A meowtain.",
    "How do you make a tissue dance? Put a little boogie in it.",
    "Why don’t oysters donate to charity? Because they are shellfish.",
    "What does a cloud wear under his raincoat? Thunderwear.",
    "Why did the banker switch careers? He lost interest.",
    "What do you call a pony with a cough? A little horse."
]

WORD_LIST = ["ocean", "planet", "rocket", "jungle", "castle", "wizard", "knight", "forest", "dragon", "castle",
    "storm", "shadow", "river", "mountain", "ghost", "pirate", "treasure", "comet", "galaxy", "canyon",
    "island", "castle", "lion", "thunder", "volcano", "desert", "storm", "breeze", "harbor", "mirror",
    "magic", "sword", "cliff", "legend", "voyage", "whisper", "ember", "phoenix", "maze", "arrow",
    "flame", "glacier", "riddle", "spark", "echo", "frost", "spire", "wave", "charm", "rift"
]

def tell_joke():
    return random.choice(JOKES)

def handle_ok(message):
    return random.choice(OK_RESPONSES)

def find_response(message):
    msg = message.lower()
    words = re.findall(r'\b\w+\b', msg)  # split into words to avoid substring issues

    # Check greetings first
    for greet in ["hi", "hello", "hey"]:
        if greet in words:
            return random.choice(KEYWORDS_RESPONSES[greet])

    # Check farewells
    if any(farewell in msg for farewell in ["bye", "goodbye", "byebye"]):
        return random.choice(KEYWORDS_RESPONSES["bye"])

    if "weather" in msg:
        return "weather"

    if "time" in msg:
        return "time"

    if "joke" in msg:
        return tell_joke()

    if "repeat" in msg:
        return "repeat"

    if "play" in msg or "game" in msg:
        return "game"

    if "ok" in words and len(words) <= 3:
        return handle_ok(msg)

    for keyword, responses in KEYWORDS_RESPONSES.items():
        if keyword in msg:
            return random.choice(responses)

    return random.choice(DEFAULT_RESPONSES)
