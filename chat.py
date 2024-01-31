import random
import json
import torch
import shelve
from model import NeuralNet
from ntlk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Teddy"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    # with shelve.open('conversation_data.db', writeback=True) as db:
    #     if 'conversation' not in db:
    #         db['conversation'] = {'msgID': 0, 'message': {}}
    #
    #     db['conversation']['msgID'] += 1
    #     msg_id = db['conversation']['msgID']
    #     db['conversation']['message'][msg_id] = msg
    #     print("Conversation Data Saved:", db['conversation'])
    # return "I do not understand..."
    with shelve.open('conversation_data.db', writeback=True) as db:
        if 'conversation' not in db:
            db['conversation'] = {'msgID': 0, 'message': {}}

        msg_id = get_next_msg_id(db['conversation']['message'])
        db['conversation']['message'][msg_id] = msg
        db['conversation']['msgID'] = msg_id
        print("Conversation Data Saved:", db['conversation'])
    return "I do not understand..."


if __name__ == "__main__":
    print("How may i assist you? (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

def get_next_msg_id(message_data):
    available_msg_ids = set(message_data.keys())
    next_msg_id = 1
    while next_msg_id in available_msg_ids:
        next_msg_id += 1
    return next_msg_id