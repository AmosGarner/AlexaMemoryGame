import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def newGame():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text).simple_card('Welcome', speech_text)

@ask.intent("YesIntent")
def startRound():
    numbers = [randint(0, 9) for _ in range(3)]
    speech_text = render_template('round', numbers=numbers)
    session.attributes['Numbers'] = numbers[::-1]
    return question(speech_text).reprompt(speech_text).simple_card('Round', speech_text)

@ask.intent("AnswerIntent")
def answer(first,second,third):
    incomingNumbers = [int(first),int(second),int(third)]
    sessionNumbers = session.attributes['Numbers']
    winningNumbers = [int(sessionNumbers[0]), int(sessionNumbers[1]), int(sessionNumbers[2])]
    speech_text = render_template('lose')
    if incomingNumbers == winningNumbers:
        speech_text = render_template('win')
    return statement(speech_text).simple_card('Response',speech_text)

if __name__ == '__main__':
    app.run()
