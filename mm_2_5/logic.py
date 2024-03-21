import datetime
import errno
import os

game_options = {"ano": True, "ne": False, "yes": True, "no": False}


class CustomException(Exception):
    pass


class Attempt:
    def __init__(
        self, att_no, your_code=[], white=0, black=0, duration=datetime.time(0)
    ):

        self.__index = att_no
        self.__your_code = your_code
        self.__black_stick = white
        self.__white_stick = black
        self.__attempt_time = duration

    def __repr__(self):
        self.att_Report = ""
        self.att_Report += f"{self.__index + 1}. "
        self.att_Report += f"{self.__your_code} "
        self.att_Report += f"Black: {self.__black_stick} "
        self.att_Report += f"White: {self.__white_stick} "
        self.att_Report += f"Time: {self.__attempt_time} "
        self.att_Report += "\n"
        return self.att_Report


class MasterMind:
    def __init__(self, attempt=10, option=8, digit=5 , time_limit = 30):
        import uuid
        from random import choices

        self.__game_status = "parameter_checking"
        self.__game_active = False

        print("Test of the input parameters \n")
        # check, if all parameter of the class are in allowed limits.
        error_message = False
        if (
            isinstance(attempt, int)
            and isinstance(option, int)
            and isinstance(digit, int)
            and isinstance(time_limit, int)
        ):
            if attempt < self.limits("ATTEMPT_MIN") or attempt > self.limits(
                "ATTEMPT_MAX"
            ):
                error_message = "Count of attempts out of range!"

            elif option < self.limits("VALUES_MIN") or option > self.limits(
                "VALUES_MAX"
            ):
                error_message = "Count of options out of range!"
            elif digit < self.limits("DIGIT_MIN") or digit > self.limits("DIGIT_MAX"):
                error_message = "Count of digits out of range!"
            #only for test! Remove, when completed!
            # elif time_limit < self.limits("TIME_MIN") or time_limit > self.limits("TIME_MAX"):
            #     error_message = "Time limit out of range!"
        else:
            error_message = "Parameters must be integer!"

        if error_message:
            print(self.return_outer_limits())
            raise CustomException(error_message)
            return error_message

        print("Parameters are OK. I start the game. \n")
        self.__attempt = attempt
        self.__option = option
        self.__digit = digit

        self.__game_id = str(uuid.uuid4())
        print(f"Created new game with ID {self.__game_id}")
        print("I generate the secret code. ")
        self.__possible_values = [_ for _ in range(1, self.__option + 1)]
        self.__secret_code = choices(self.__possible_values, k=self.__digit)
        print("Secret Code was generated.")
        self.__game_status = "game_running"
        self.__current_att = 0
        self.__game_active = True
        self.__code_hacked = False
        self.__all_values_OK = False
        self.__time_left = False
        self.__all_attempts_exhausted = False

        self.__attempts_pool = []

        self.set_time_for_game(time_limit)
        self.__date_of_the_game = datetime.datetime.now()
        self.__start_time = datetime.datetime.now()
        self.__temp_time = self.__start_time
        print(f"Good luck")

    # Set time limit for the game
    # Time limit in minutes.
    def set_time_for_game(self, time_limit = 30):
        # default time for quessing set to 30 minutes.
        h = int(time_limit / 60)
        m = time_limit % 60
        self.__TIME_FOR_GAME = datetime.timedelta(days=0, hours=h, minutes=m, seconds=0)
        return True, self.__TIME_FOR_GAME

    def return_time_for_game(self):
        return self.__TIME_FOR_GAME

    def game_start(self):
        start_time = self.__date_of_the_game.time()
        return start_time

    def game_date(self):
        game_date = self.__date_of_the_game.date()
        return game_date

    def game_duration(self):
        game_duration = datetime.datetime.now() - self.__start_time
        return game_duration

    # this Dictionary return limits for:
    # - no of attempts
    # - no of digits
    # - possible values counts
    def limits(self, limit_name=" "):
        self.__the_outer_limits = {
            "ATTEMPT_MIN": 2,
            "ATTEMPT_MAX": 50,
            "DIGIT_MIN": 1,
            "DIGIT_MAX": 10,
            "VALUES_MIN": 2,
            "VALUES_MAX": 16,
            "TIME_MIN": 5, # 5 minutes per game is minimum.
            "TIME_MAX": 600,
            # 10 hours per game ought to be enough for anybody.

        }
        limit_value = self.__the_outer_limits.get(limit_name, False)
        return limit_value

    def return_outer_limits(self):
        outer_limits = ""
        outer_limits += "All limits must be integers! \n"
        outer_limits += "All limits must be positive! \n"
        outer_limits += f"Count of attempts must be in range: {self.limits('ATTEMPT_MIN')} - {self.limits('ATTEMPT_MAX')}.\n"
        outer_limits += f"Count of digits must be in range: {self.limits('DIGIT_MIN')} - {self.limits('DIGIT_MAX')}. \n"
        outer_limits += f"Values for each digit must be in range: {self.limits('VALUES_MIN')} - {self.limits('VALUES_MAX')}.\n"
        outer_limits += f"Time must be in range: {self.limits('TIME_MIN')} - {self.limits('TIME_MAX')} minutes.\n"
        return outer_limits

    def check_time_to_left(self):
        if self.__game_active:
            if self.game_duration() > self.return_time_for_game():
                print("You exceeded time limit for game!")
                self.__game_active = False
                self.__game_status = "time_exceeded"
                self.__time_left = True
        return self.__time_left

    def return_rest_time(self):
        rest_time = self.return_time_for_game() - self.game_duration()
        if rest_time.days < 0:
            return datetime.timedelta(seconds=0)
        else:
            return rest_time

    def show_secret(self):
        return f"Secret code is: {self.__secret_code} \n"

    def show_secret_list(self):
        return self.__secret_code

    def list_of_values(self):
        return self.__possible_values

    def is_running(self):
        return self.__game_active

    def game_status(self):
        return self.__game_status

    def active_attempt(self):
        return self.__current_att

    def rest_attempt(self):
        rest = self.__attempt - self.__current_att
        return rest

    def attempt_pool(self):
        return self.__attempts_pool

    def next_attempt(self, your_attempt="0 0 0 0 0"):
        self.check_time_to_left()
        if not self.__game_active:
            return False, "Game is not active!"

        if self.__current_att >= self.__attempt:
            # this case can't occur,
            # but better safe than sorry!
            print("Critical Error!")
            return False, "Critical Error!"

        # check if valid code was inserted
        input_is_ok, eval_message = self.attempt_control(your_attempt)

        # Input data are incorrect
        if not input_is_ok:
            return input_is_ok, eval_message

        # Input data are correct
        attemp_time = datetime.datetime.now() - self.__temp_time
        self.__temp_time = datetime.datetime.now()

        # evaluate attempt
        your_attempt = eval_message
        your_attempt = list(map(int, your_attempt))
        print(your_attempt)
        digit_equal = []
        attemp_rest = []
        secret_rest = []
        secret = self.__secret_code

        for _ in range(0, self.__digit):
            if secret[_] == your_attempt[_]:
                digit_equal.append(your_attempt[_])
            else:
                attemp_rest.append(your_attempt[_])
                secret_rest.append(secret[_])
        black_stick = len(digit_equal)

        white_stick = 0
        wrong_position = True
        while wrong_position:
            wrong_position = False
            for digit in attemp_rest:
                if digit in secret_rest:
                    attemp_rest.remove(digit)
                    secret_rest.remove(digit)
                    white_stick += 1
                    wrong_position = True
                    break

        the_attempt = Attempt(
            self.__current_att,
            your_attempt,
            black_stick,
            white_stick,
            attemp_time,
        )
        self.__current_att += 1
        self.__attempts_pool.append(the_attempt)

        # Update status of the current game
        if white_stick + black_stick == len(secret):
            self.__all_values_OK = True
            print("Congratulate, you quessed all Values!")

        if black_stick == len(secret):
            print("Congratulate, you hacked the secret!")
            self.__code_hacked = True
            self.__game_active = False
            self.__game_status = "code_hacked"

        if len(self.__attempts_pool) < self.__attempt:
            pass
        elif len(self.__attempts_pool) == self.__attempt:
            self.__game_active = False
            if not self.__code_hacked:
                print("not hacked")
                self.__game_status = "attempts_exhausted"
        else:
            # this case can't occur,
            # but better safe than sorry!
            print("Critical Error!")

        return True, the_attempt



    def attempt_control(self, your_attempt="0 0 0 0 0"):

        your_attempt = your_attempt.split()
        if len(your_attempt) != self.__digit:
            return False, "Wrong number of digits!"

        code_error = False
        for digit in your_attempt:
            if not digit.isdigit():
                code_error = "Digit must be positive integer!"
                break
            digit = int(digit)
            if digit not in self.list_of_values():
                code_error = "Value out of range!"
                break

        if code_error:
            return False, code_error
        else:
            return True, your_attempt
    def __repr__(self):
        self.check_time_to_left()
        MM_Report = ""
        MM_Report += " *************\n"
        MM_Report += " * L O G I C * \n"
        MM_Report += " *************\n"
        MM_Report += f"Game ID: {self.__game_id} \n"
        MM_Report += f"Date: {self.game_date()} \n"
        MM_Report += f"Game started at: {self.game_start() } \n"
        MM_Report += f" Number of attempts: {self.__attempt} \n"
        MM_Report += f" Number of digits in quesed code: {self.__digit} \n"
        MM_Report += (
            f" The digit has one of the values : \n {self.__possible_values} \n"
        )
        MM_Report += "Digit values can be repeated. \n"

        MM_Report += f"Active attempt number: {self.active_attempt() + 1} \n"
        MM_Report += f"Used attempts: {len(self.__attempts_pool)} \n"
        MM_Report += f"Rest attempts: {self.rest_attempt()} \n \n"

        MM_Report += f"Time for play: {self.return_time_for_game()} \n"
        MM_Report += f"Time left: {self.game_duration() } \n"
        MM_Report += f"Time rest: {self.return_rest_time() } \n"
        MM_Report += "\n"

        if not self.is_running():
            MM_Report += 40 * "*" + "\n"
            MM_Report += self.show_secret()
            MM_Report += 40 * "*" + "\n"
        MM_Report += "Attempts pool:\n"
        MM_Report += "***************************\n"

        if len(self.attempt_pool()):
            for single_attempt in self.__attempts_pool:
                MM_Report += repr(single_attempt)
        else:
            MM_Report += "****** Pool is empty ******\n"
        MM_Report += "***************************\n"
        MM_Report += "\n"
        MM_Report += "  Game flags:  \n"
        MM_Report += "**************\n"
        MM_Report += f" Game status: {self.__game_status} \n"
        if self.__game_active:
            MM_Report += " You are in the game. \n"

            if self.__all_values_OK:
                MM_Report += (
                    " You just guessed all the numbers. You are close to the goal! \n"
                )
            else:
                MM_Report += " Keep on! \n"
        else:
            MM_Report += " Game is over! \n"

            if self.__time_left:
                MM_Report += " You exceeded time limit! \n"

            if self.__code_hacked:
                MM_Report += "You hacked the secret! I congratulate you! \n"
            elif self.__all_values_OK:
                MM_Report += "You guessed all the numbers. Unfortunately, the sequence is wrong! \n"
            else:
                MM_Report += "You are looser! \n"

        return MM_Report

if __name__ == "__main__":
    # old version of Master Mind
    attempt = 13 # you have 10 attempts
    value = 8 # value can be 1 , 2, 3, 4, 5, 6
    digit = 5 # 4 digits of secret code
    time = 11  #5 minutes to break code
    the_game = MasterMind(attempt, value, digit, time)

    print(repr(the_game))
    while the_game.is_running():
        quess_code = input("Insert your code: ")
        attempt_inserted = False
        while not attempt_inserted:
            attempt_inserted = the_game.next_attempt(quess_code)
            print(attempt_inserted)
        print(repr(the_game))
        # print(the_game.attempt_pool())
    print("Final report:")
    print(repr(the_game))

    # Save game to the file:
    print("I will save finished game to the file.")

    try:
        with open("data/mm_games.txt", "a") as f:
            f.write("Final report: \n")
            f.write(repr(the_game))
            f.write("-" * 50)
            f.write("\n")
            print("Game was saved succesfully.")

    except FileNotFoundError:
            print("Folder /data is missing.")
            print("Create it, to have game report.")

    except PermissionError:
        print("File is read-only.")
        print("Change atributes, to have game report.")

    finally:
        print("Game over!")