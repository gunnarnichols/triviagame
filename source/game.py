from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from datetime import datetime
import random, math

from sqlalchemy.sql.expression import null
from . import db
from .models import Game, Question, Player
# from .category import mycategory

game = Blueprint('game', __name__)


@game.route('/game/settings', methods=['GET', 'POST'])
def gameSettings():
    # Set the game variables
    incomming_values = request.args.to_dict(flat=False)
    game_id = incomming_values.get('GameID')[0]
    
    total_num_questions = Question.query.count()
    if (current_user.is_authenticated):
        print("Using game for a logged in user")
        p = Player.query.get(current_user.id)
        game = Game.query.get(p.game_id)
    else:
        print("Using game for a random")
        game = Game.query.get(game_id)
    #Check if the category is defined, and if so set the game.category data to the category. Parse the questions table to get every id from that category
    #Set up the conditional logic for the initialization of the questions_left array to only populate with valued from the category.

    #get all QuestionIDs and randomize them
    print(list(range(1, total_num_questions + 1)))
    print("Random list of questions")
    questions_left = random.sample(list(range(1, total_num_questions + 1)), total_num_questions)
    print(game)
    print(game.category)
    if game.category != null:
        questions_left = []
        for k in range(total_num_questions):  
            q = Question.query.get(k+1)
            if q.category == game.category:
                questions_left.append(q.id)
        questions_left = random.sample(questions_left, len(questions_left))
    print(questions_left)

    #select the random question for the first question
    str_id = questions_left[0]
    q = Question.query.get(str_id)

    # # Shuffle the 4 potential answers
    input = [q.answer, q.option_1, q.option_2, q.option_3]
    answers = random.sample(input, len(input))

    # Determine the location of the answer
    for x in range(4):
        if answers[x] == q.answer:
            answer_location = x + 1

    #Remove the question from the questions left array
    questions_left.remove(str_id)

    #pass all the question information to the game object
    game.questions_left = str(questions_left)
    game.question = str_id
    game.answer_location = answer_location
    game.cr_time = datetime.now()
    db.session.commit()

    # Define the data to be handed off to the template
    return_data = [{"Lives" : game.lives}, {"Question Time" : game.question_time}, {"Score" : game.score}, {"Number Question Skips" : game.num_skip_question},
                   {"Question": q.question}, {"Option_1": answers[0]}, {"Option_2": answers[1]}, {"Option_3": answers[2]}, {"Option_4": answers[3]}, {"Fifth Fifty Attempt": game.num_fifty_fifty},
                   {"game_id": game.id}]
    print(return_data)
    return jsonify(return_data)

# Return the answer to the current question
@game.route('/game/answer')
def gameAnswer():
    incomming_values = request.args.to_dict(flat=False)
    game_id = incomming_values.get('GameID')[0]
    
    total_num_questions = Question.query.count()
    if (current_user.is_authenticated):
        print("Using game for a logged in user")
        p = Player.query.get(current_user.id)
        game = Game.query.get(p.game_id)
    else:
        print("Using game for a random")
        game = Game.query.get(game_id)
    
    return_data = [{"Answer_Location" : game.answer_location}]
    return(jsonify(return_data))

# Modify the game's lives
@game.route('/game/removelife')
def removeLife():
    incomming_values = request.args.to_dict(flat=False)
    game_id = incomming_values.get('GameID')[0]
    
    total_num_questions = Question.query.count()
    if (current_user.is_authenticated):
        print("Using game for a logged in user")
        p = Player.query.get(current_user.id)
        game = Game.query.get(p.game_id)
    else:
        print("Using game for a random")
        game = Game.query.get(game_id)
        
    game.lives = game.lives - 1
    db.session.commit()
    return(str(game.lives))

        
#Modify the game's remaining question skips
@game.route('/game/skip_question')
def skipQuestion():
    #TODO We need to dynamically get the game associated with the user/game instance
    incomming_values = request.args.to_dict(flat=False)
    game_id = incomming_values.get('GameID')[0]
    
    total_num_questions = Question.query.count()
    if (current_user.is_authenticated):
        print("Using game for a logged in user")
        p = Player.query.get(current_user.id)
        game = Game.query.get(p.game_id)
    else:
        print("Using game for a random")
        game = Game.query.get(game_id)
    game.num_skip_question = game.num_skip_question - 1
    db.session.commit()

    return(str(game.num_skip_question))


#Modify the game's remaining 50/50, and get the options that can be removed
@game.route('game/fifty_fifty')
def fiftyFifty():
    incomming_values = request.args.to_dict(flat=False)
    game_id = incomming_values.get('GameID')[0]
    
    total_num_questions = Question.query.count()
    if (current_user.is_authenticated):
        print("Using game for a logged in user")
        p = Player.query.get(current_user.id)
        game = Game.query.get(p.game_id)
    else:
        print("Using game for a random")
        game = Game.query.get(game_id)
    option = []
    game.num_fifty_fifty = game.num_fifty_fifty-1
    attempt = str(game.num_fifty_fifty)

    for i in range(1, 4):
        if i != game.answer_location:
            option.append(i)
    game.fifty_fifty_option = str(option)
    return_data = [{"first_option" : game.fifty_fifty_option[1]},
                   {"second_option" : game.fifty_fifty_option[4]},
                   {"attempt" : attempt}]
    db.session.commit()
    return (jsonify(return_data))


#Update Score and reset question Time
@game.route('/game/update_score')
def updateScore():
    #TODO We need to dynamically get the game associated with the user/game instance
    incomming_values = request.args.to_dict(flat=False)
    game_id = incomming_values.get('GameID')[0]
    
    total_num_questions = Question.query.count()
    if (current_user.is_authenticated):
        print("Using game for a logged in user")
        p = Player.query.get(current_user.id)
        game = Game.query.get(p.game_id)
    else:
        print("Using game for a random")
        game = Game.query.get(game_id)

    #Sent the current time for the next question, and take the difference for the passed time
    previous_time = game.cr_time
    game.cr_time = datetime.now()
    passed_time = (game.cr_time - previous_time)

    #Update the score based on how much time has passed.
    game.score = game.score + math.floor(float(100) * float(max(31 - passed_time.seconds, 0 ))/30)
    db.session.commit()

    return(str(game.score))