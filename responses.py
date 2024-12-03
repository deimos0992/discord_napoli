from random import choice, randint
from utility import returnNextMatch

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'prossima partita' in lowered:
        return returnNextMatch()
