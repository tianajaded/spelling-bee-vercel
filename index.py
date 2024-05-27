from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
import random
import string

app = Flask(__name__)

vowels = 'aeiou'
consonants = ''.join(set(string.ascii_lowercase) - set(vowels))

class SpellinBeeGame:
    def __init__(self):
        self.center_letter = ''
        self.outer_letters = []
        self.player_scores = {}
        self.words_list = []
        self.valid_words = []
        self.pangrams = []
        self.potential_words = 0  
        self.used_words = set()

        with open('dictionary.txt', 'r') as wordfile:
            self.words_list = [word.strip().lower() for word in wordfile.readlines()]

    def is_valid_word(self, word):
        return len(word) > 3 and self.center_letter in word and word in self.valid_words
    
    def turn(self, player, word):
        if word in self.used_words:
            return 'used'  #indicate the word has already been used
        if self.is_valid_word(word):
            if 'words_found' not in self.player_scores[player]:
                self.player_scores[player]['words_found'] = []
            if word not in self.player_scores[player]['words_found']:
                self.player_scores[player]['words_found'].append(word)
                self.player_scores[player]['score'] += len(word)
                self.used_words.add(word)  #add the word to the used words set
            return 'valid'
        return 'invalid'
    
    def register_player(self, player_name):
        if len(self.player_scores) < 2:
            self.player_scores[player_name] = {'name': player_name, 'score': 0, 'words_found': []}
            return True
        return False
    
    def shuffle(self):
        while True:
            self.outer_letters = self.generate_letters()
            random.shuffle(self.outer_letters)
            self.center_letter = random.choice(string.ascii_lowercase)
            if self.center_letter not in self.outer_letters:
                break

        self.find_valid_words()
        self.potential_words = len(self.valid_words)  #update potential words count

    def generate_letters(self):
        vowels = 'aeiou'
        consonants = ''.join(set(string.ascii_lowercase) - set(vowels))
        letters = random.sample(vowels, 2) + random.sample(consonants, 4)
        return letters

    def find_valid_words(self):
        self.valid_words = [
            word for word in self.words_list
            if all(letter in (self.outer_letters + [self.center_letter]) for letter in word) and
                self.center_letter in word and  #make sure the center letter is in the word
                any(letter in vowels for letter in word) and
                any(letter in consonants for letter in word)
    ]
        self.pangrams = [word for word in self.valid_words if len(set(word)) == 7]

        #ensure at least one pangram
        if not self.pangrams:
            self.shuffle()
        print("Valid Words:", self.valid_words)
        print("Pangrams:", self.pangrams)    

    def calculate_rank(self, found_words_count):
        total_words = len(self.valid_words)
        percentage = (found_words_count / total_words) * 100

        if percentage >= 100:
            return "Queen Bee"
        elif percentage >= 70:
            return "Genius"
        elif percentage >= 50:
            return "Amazing"
        elif percentage >= 40:
            return "Great"
        elif percentage >= 25:
            return "Nice"
        elif percentage >= 15:
            return "Solid"
        elif percentage >= 8:
            return "Good"
        elif percentage >= 5:
            return "Moving Up"
        elif percentage >= 2:
            return "Good Start"
        else:
            return "Beginner"

game = SpellinBeeGame()

@app.route('/')
def index():
    return redirect(url_for('spellinbee'))

@app.route('/spellinbee')
def spellinbee():
    return render_template('spellinbee.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/register', methods=['POST'])
def register_players():
    data = request.json
    player1_name = data.get('player1')
    player2_name = data.get('player2')
    if player1_name and player2_name:
        success1 = game.register_player(player1_name)
        success2 = game.register_player(player2_name)
        if success1 and success2:
            game.shuffle()  # Shuffle letters after registering players
            letters = {'center': game.center_letter, 'outer': game.outer_letters}
            return jsonify({'msg': 'Players registered.', 'letters': letters, 'player1': player1_name, 'player2': player2_name, 'potential_words': game.potential_words}), 200
        else:
            return jsonify({'error': 'Failed to register players. Max players limit reached.'}), 400
    else:
        return jsonify({'error': 'Both player names are required.'}), 400

@app.route('/take_turn', methods=['POST'])
def take_turn():
    data = request.json
    player_name = data.get('player')
    word = data.get('word').lower()

    if player_name not in game.player_scores:
        return jsonify({'error': 'Player not registered.'}), 400

    turn_result = game.turn(player_name, word)
    if turn_result == 'used':
        return jsonify({'error': 'Word already used.'}), 400
    elif turn_result == 'valid':
        scores = {
            'player1': game.player_scores[list(game.player_scores.keys())[0]],
            'player2': game.player_scores[list(game.player_scores.keys())[1]]
        }
        ranks = {
            'player1': game.calculate_rank(len(scores['player1']['words_found'])),
            'player2': game.calculate_rank(len(scores['player2']['words_found']))
        }
        scores['player1']['rank'] = ranks['player1']
        scores['player2']['rank'] = ranks['player2']
        return jsonify({'msg': f'{player_name} scored {len(word)} points!', 'scores': scores}), 200
    else:
        return jsonify({'error': 'Invalid word. No points scored.'}), 400



# if __name__ == '__main__':
#     app.run(debug=True, port = 8080)
