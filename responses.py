from random import choice, randint


def get_response(user_input) -> str:
    if not user_input.startswith('!'):
        return None

    command = user_input[1:].lower()

    if command == '':
        return 'You did not specify a command.'
    elif command == 'hello':
        return 'Hi there'
    elif command == 'test':
        return 'Test works'
    elif command == 'cael':
        return 'Cael is gay'
    else:
        return choice(['I don\'t know what you mean', 'I don\'t understand', 'I don\'t know'])
    
