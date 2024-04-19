import numpy as np
import pandas as pd
import requests

class Game:

    def __init__(self, rounds:int):
        self.rounds = rounds

    def build_request(self, nums:np.ndarray) -> str:
        numbers = str(list(nums))
        numbers = numbers[1:len(numbers)-1].replace(' ','')
        request_string = f"http://numbersapi.com/{numbers}"
        return request_string

    def generate_rounds_dict(self) -> dict:
        game_information = dict()
        while True:
            numbers = np.random.randint(1,1000, self.rounds)
            response = requests.get(self.build_request(numbers))
            information_data = response.json()
            for possible_number in information_data:
                if (f"{str(possible_number)} is the" in information_data[possible_number]):
                    question = information_data[possible_number].replace(f"{str(possible_number)} is", "Make a market on")
                    game_information[possible_number] = question
                if len(game_information)==self.rounds:
                    break
            if len(game_information)==self.rounds:
                break
        return game_information

    def get_user_answers(self) -> dict:
        questions = self.generate_rounds_dict()
        answers = dict()
        for q in questions:
            user_response = input(questions[q])
            try:
                user_response = user_response.split('-')
                user_response[0], user_response[1] = int(user_response[0]), int(user_response[1])
                answers[int(q)] = user_response
            except:
                Exception("Invalid Response, answer forfeited")
        return answers

    def calculate_score(self, user_answers:dict) -> int:
        good_intervals = dict()
        for a in user_answers:
            if (user_answers[a][0]<=a and user_answers[a][1]>=a):
                good_intervals[a] = user_answers[a]
        error_sum = sum(list(int(good_intervals[i][1]/good_intervals[i][0]) for i in good_intervals))
        score = (10+error_sum)*(2**(self.rounds-len(good_intervals)))
        return score

    def start_estimathon(self):
        print()
        user_answers = self.get_user_answers()
        score = self.calculate_score(user_answers)
        print(f"\nFinal Score : {score}")

if __name__=="__main__":
    print("Welcome to estimathon!!")
    r = input("Input how many rounds you want to play (Default=13): ")
    if (int(r)<2):
        print("Invalid number, default 13 rounds selected\n")
        test_game = Game(13)
    else:
        print()
        test_game = Game(int(r))
    test_game.start_estimathon()
