from __future__ import print_function, unicode_literals
from sklearn.externals import joblib
from textblob import TextBlob
import re


GREETING_KEYWORDS = ("hello", "hi", "greetings", "how are you", "what's up",'good morning','good evening')

GREETING_RESPONS = "Hey how you doing ?"

def check_for_greeting(parsed, sentence):
    if sentence.lower () in GREETING_KEYWORDS:
        return GREETING_RESPONS
    else:
        for word in parsed.words:
            if word.lower() in GREETING_KEYWORDS:
                return GREETING_RESPONS

NONE_RESPONSE = "Sorry I didn't get you !"


def check_if_order (sentence):

    if(len(sentence.pos_tags))> 1 :
        if sentence.pos_tags[0][1]=='VB' or sentence.pos_tags[0][1]=='NN':


            return "You are giving me an order"
def QuestionOrNot (sentence):
    for w, p in sentence.pos_tags :
        if (p == 'WDT' or p=='WP' or p =='WP$' or p =='WRB' ):
            noun= find_noun(sentence)
            if noun :
                if noun=='name':
                    response='My name is robotchat'
                    return response
            else :
                    pronoun = find_pronoun(sentence)
                    if (pronoun == "I" or pronoun =="my"):
                        verb = find_verb(sentence)
                        if (verb[0] == 'do' or verb[0] == 'are' or verb[0] == 'is' or  verb[0] == 'did' ):
                            response = 'I am a robot and you can only ask me questions and i will try to help you :) !'
                            return response


def starts_with_vowel(word):
    return True if word[0] in 'aeiou' else False




def find_pronoun(sent):
    pronoun = None
    length =len(sent.pos_tags)
    counter =0
    for word, part_of_speech in sent.pos_tags:
        counter +=1
        if counter != (length):
            if part_of_speech == 'PRP' and word.lower() == 'you':
                pronoun = 'I'
            elif part_of_speech == 'PRP' and word == 'I':

                pronoun = 'You'

            elif part_of_speech == 'PRP$' and word.lower() == 'your':

                pronoun = 'my'


    return pronoun

def find_verb(sent):
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):
            verb = word
            pos = part_of_speech
            break
    return verb, pos


def find_noun(sent):

    noun = None

    if not noun:
        for w, p in sent.pos_tags:
            if (p == 'NN' or p =='NNP' or p=='NNS'):
                noun = w
                break

    return noun

def find_adjective(sent):
    adj = None
    for w, p in sent.pos_tags:
        if p == 'JJ':
            adj = w
            break
    return adj



def construct_response(pronoun, noun, verb,sentence):
    print(pronoun, noun, verb,sentence)
    resp = []

    # if pronoun:
    #     resp.append(pronoun)

    if verb and not noun :
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is', "'m"):
            if pronoun.lower() == 'you':
                # resp=[]
                resp.append( "do u think you are ")
            else:
                resp.append(verb_word)
        else :

            resp.append( 'me too i '+sentence.split(' ', 1)[1])
    if not verb and noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)

    if verb and noun :
        resp=[]
        resp.append('I love ' + noun)


    return " ".join(resp)


def check_for_comment_about_bot(pronoun, noun, adjective):
    resp = None
    if pronoun == 'I' and (noun or adjective):
        resp = "I got you, you are talking about me don't you"
    return resp

def RemovenonChars (sentence):
    sentence =re.sub("[^a-zA-Z]", " ", sentence)
    return sentence
def RemoveExtraSpaces(sentence):
    sentence = (sentence.strip() )
    return sentence
def preprocess_text(sentence):
    sentence=RemovenonChars(sentence)
    sentence=RemoveExtraSpaces(sentence)
    cleaned = []
    words = sentence.split(' ')
    for w in words:
        if w == 'i':
            w = 'I'

        if w == "i'm":
            w = "I'm"

        if w == 'r':
            w = 'are'

        if w == 'u':
            w = 'you'
        cleaned.append(w)

    return ' '.join(cleaned)

def respond(sentence):
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    resp = ''

    resp = check_for_greeting(parsed,cleaned)

    if not resp :
        resp = QuestionOrNot (parsed)
    if not resp :
        resp = check_if_order(parsed)

    if not resp :

        pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)
        resp = check_for_comment_about_bot(pronoun, noun, adjective)


    if not resp:
        if not pronoun:
            resp = NONE_RESPONSE

        else:
            resp = construct_response(pronoun, noun, verb,sentence)
    if not resp:
        resp = NONE_RESPONSE


    return resp

def find_candidate_parts_of_speech(parsed):
    pronoun = None
    noun = None
    adjective = None
    verb = None
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    return pronoun, noun, adjective, verb




begin = ''
response="hello i'am a chatbot how can i help ? to exit type Bye "
while ((begin.lower() !='bye') ):
    begin = input(response+'\n')
    response =respond(begin)

