# Bryant D. Pham
# ID: 12204588
# This project was non-collaborative and was worked on alone.
# all code was placed into one file for grading purposes.


import json
import urllib.parse
import urllib.request
import random

from pathlib import Path
from time import sleep


GLOBAL_SLEEP = 2


class Body:
    """Class representing each Solar System object. It compartmentalizes each of the object's characteristics."""
    def __init__(self, name: str, semimajor_axis: int, eccentricity: float,
                 mass: str, gravity: float, mean_radius: int, body_type: str, mass_raw: {float, int}):

        self._name = name                       # english name.
        self._semimajor = semimajor_axis        # semimajor axis in km.
        self._eccentricity = eccentricity       # orbital eccentricity.
        self._mass = mass                       # body mass in 10^n kg.
        self._gravity = gravity                 # surface gravity in m/s/s.
        self._radius = mean_radius              # mean radius in km.
        self._type = body_type                  # body type (Star, Planet, Dwarf Planet, Asteroid, Comet, or Moon.

        self._mass_raw = mass_raw               # (massValue, massExponent

        self._units = {"Semimajor Axis": "km", "Eccentricity": "", "Mass": "kg", "Gravity": "m/s/s", "Radius": "km"}

    def get_name(self) -> str:
        return self._name

    def get_semimajor_axis(self) -> int:
        return self._semimajor

    def get_eccentricity(self) -> float:
        return self._eccentricity

    def get_mass(self) -> str:
        return self._mass

    def get_gravity(self) -> float:
        return self._gravity

    def get_radius(self) -> int:
        return self._radius

    def get_type(self) -> str:
        return self._type

    def get_mass_raw(self) -> {float, int}:
        return self._mass_raw

    def get_units(self, characteristic: str) -> str:
        return self._units[characteristic]


class HigherLower:
    """Class representing the actual higher-lower game. It can take into account semimajor axis size, eccentricity,
    mass, gravity, and radius of two different bodies."""
    def __init__(self, solar_system: dict):
        # by default, the game has all settings enabled and is not a single category game.
        self._category = {"Semimajor Axis": True, "Eccentricity": True, "Mass": True, "Gravity": True, "Radius": True}
        temp = iter(self._category.values())
        self._single = any(temp) and not any(temp)

        # stores all the solar system bodies.
        self._bodies = list()

        # stores useful information to make this a game, such as current score and whether the player has not lost.
        self._score = 0
        self._alive = True
        self._match_categories = list()

        # performs the pre-game setup, such as printing instructions, changing settings, and inserting all bodies.
        self._print_instructions()
        self._confirm_settings()
        self._insert_bodies(solar_system)

        # for behind-the-scenes stuff:
        enable_cheats = input(f"DEBUGGING: do you want to enable cheat mode ['YES/'NO']?\n> ")
        while enable_cheats.lower() not in {"yes", "no"}:
            enable_cheats = input(f"\tDEBUGGING: bruh, it's ['YES'/'NO]\n> ")

        self._cheat = True if enable_cheats == "yes" else False if enable_cheats == "no" else "wtf"
        if self._cheat:
            self._print_all_bodies()

        # starts the actual game.
        self._continue_pregame()

    ##################################################
    #               HELPER FUNCTIONS                 #
    ##################################################

    def _increase_score(self) -> None:
        """Increases the score of the player by 1."""
        self._score += 1

    def _lose_game(self) -> None:
        """Changes the game state such that the player has lost."""
        self._alive = False

    def _get_state(self) -> bool:
        """Returns a boolean value for whether the user is alive or has lost."""
        return self._alive

    def _get_score(self) -> int:
        """Returns the current score of the player."""
        return self._score

    ##################################################
    #               PREGAME FUNCTIONS                #
    ##################################################

    def _confirm_settings(self) -> None:
        """Inquires whether the user would like to change the default settings to custom settings."""
        print("The game settings have been set to...")
        sleep(GLOBAL_SLEEP)

        # prints out the current settings.
        self._print_settings()
        sleep(GLOBAL_SLEEP)

        # repeatedly asks the user if they want to change the settings or not.
        change_settings = input("Would you like to change the settings ['Y'/'N']? ").upper().strip()
        while change_settings not in {"Y", "N"}:
            change_settings = input("\tPlease input a valid response ['Y'/'N']. ").upper().strip()

        # if the player wishes to change their settings, they may do so.
        if change_settings == "Y":
            self._change_settings()

    def _change_settings(self) -> None:
        """Performs the changes to the user settings."""
        print()

        # for each category, asks the user if they want to enable ('ON') or disable ('OFF') it.
        for category in self._category.keys():
            new_setting = input(f"Would you like to turn on or off the setting for {category} "
                                f"[\"ON/\"OFF\"]? ").upper().strip()
            while new_setting not in {"ON", "OFF"}:
                new_setting = input(f"\tPlease indicate a valid setting for {category} "
                                    f"[\"ON/\"OFF\"]. ").upper().strip()
            self._category[category] = True if new_setting == "ON" else False

        # checks if the settings are valid.
        if self._verify_new_settings():
            sleep(GLOBAL_SLEEP)
            print("\nYour new settings are...")
            self._print_settings()

        # otherwise, the user has to reset the settings and play with at least one category.
        else:
            sleep(GLOBAL_SLEEP)
            print("\nThere was an error with your settings. You must have at least one category enabled.", end="")
            self._change_settings()

    def _verify_new_settings(self) -> bool:
        """Checks to see if it is game with a single category.
        Then, returns whether the game can start (there must be at least one category)"""

        # check to see if only one category is enabled
        check_single_game = iter(self._category.values())
        self._single = any(check_single_game) and not any(check_single_game)

        # returns true if there is at least one category; returns false if the no categories are enabled.
        return any(self._category.values())

    def _print_settings(self) -> None:
        """Prints the settings of the game and indicates whether a category is enabled or disabled."""
        for category, state in self._category.items():
            print(f"{category:>14}:  {'ON' if state else 'OFF'}")
        # print(f"The game is set to {'single' if self._single else 'not single'}.")

    @staticmethod
    def _print_instructions() -> None:
        """Prints the instructions for the game and may be called multiple times."""
        sleep_amount = 3

        print("Welcome to the game of Higher and Lower but for our Solar System!")
        sleep(sleep_amount)

        print("The rules for the game is quite simple...")
        sleep(sleep_amount)

        print("You will first be given one Solar System body "
              "along with a single stat.")
        sleep(sleep_amount)

        print("You must determine whether the second body has higher or lower amount"
              " of that statistic.")
        sleep(sleep_amount)

        print("Simply type 'Higher' (case-insensitive) if the right body has a higher trait amount.")
        sleep(sleep_amount)

        print("Otherwise, type 'Lower' (case-insensitive) if the right body has a lower trait amount.")
        sleep(sleep_amount)

        print("You will get a point if you guess correctly, but if you lose, it is game over.")
        sleep(sleep_amount)

        print("The next round will always continue using the previous round's body. "
              "However, if you decide to only play with one trait, then that trait will not change. ")
        sleep(sleep_amount)
        print()

    def _continue_pregame(self) -> None:
        """Inquires whether the user would like to start the game, change settings, or view instructions."""
        pregame_sleep = 0.5
        print()

        print("What would you like to do?")
        sleep(GLOBAL_SLEEP)

        print("[START] the game.")
        sleep(pregame_sleep)

        print("[CHANGE] the settings.")
        sleep(pregame_sleep)

        print("[VIEW SETTINGS].")
        sleep(pregame_sleep)

        print("[VIEW INSTRUCTIONS].")
        sleep(pregame_sleep)

        # repeatedly asks the user for whether they want to start the game, change the settings, view settings,
        # or view the instructions again.
        command = input("> ").upper().strip()
        while command not in {"START", "CHANGE", "VIEW SETTINGS", "VIEW INSTRUCTIONS"}:
            command = input(f"\tPlease supply a valid command. ").upper().strip()

        sleep(GLOBAL_SLEEP/2)
        if command == "START":
            # we will start the game!
            self._start_game_single() if self._single else self._start_game()

        elif command == "CHANGE":
            # we will change the settings.
            self._change_settings()
            self._continue_pregame()

        elif command == "VIEW SETTINGS":
            # we will view the settings.
            self._print_settings()
            self._continue_pregame()

        elif command == "VIEW INSTRUCTIONS":
            # we will view the instructions.
            self._print_instructions()
            self._continue_pregame()

        else:
            raise ValueError("HigherLower._continue_pregame: issued unknown command that passed error checking.")

    ##################################################
    #               GAME FUNCTIONS                   #
    ##################################################

    @staticmethod
    def _convert(characteristic: str) -> str:
        """Returns the correctly formatted get_{characteristic} as a string."""
        return f"get_{characteristic.replace(' ', '_').lower()}"

    def _new_round(self, left_body: Body, right_body: Body, characteristic: str) -> str:
        """Starts a new round for the Higher Lower game.
        Then, it returns whether the user guessed 'higher' or 'lower'"""

        # "The {left body type} {left body name} has [a/an] {characteristic to compare} of {value} {units}."
        caller = getattr(Body, HigherLower._convert(characteristic))
        a_or_an = 'an' if characteristic[0].lower() in {'a', 'e', 'i', 'o', 'u'} else 'a'

        print(f"The {left_body.get_type()} {left_body.get_name()} has {a_or_an}"
              f" {characteristic.lower()} of {caller(left_body)} {left_body.get_units(characteristic)}".rstrip(),
              end=".\n")
        sleep(GLOBAL_SLEEP/2)

        # "The {right body type} {right body name} has a [HIGHER/LOWER] {characteristic to compare} than {left body}"
        print(f"The {right_body.get_type()} {right_body.get_name()} has a [HIGHER/LOWER]"
              f" {characteristic.lower()} than {left_body.get_name()}.")
        sleep(GLOBAL_SLEEP/2)

        # for debugging purposes (and for the vide)
        if self._cheat:
            sleep(GLOBAL_SLEEP/2)
            print("\t!!!!!CHEATING MODE ENABLED FOR DEMONSTRATION PURPOSES!!!!!")
            print(f"\t\tRight body has {a_or_an} {characteristic.lower()} of {caller(right_body)} "
                  f"{right_body.get_units(characteristic)}".rstrip(), end=".\n")

        sleep(GLOBAL_SLEEP/2)
        print("Please type in your answer.")
        sleep(GLOBAL_SLEEP/4)

        # repeatedly asks the user for their guess of higher or lower.
        user_answer = input("\t> ").upper().strip()
        while user_answer not in {"HIGHER", "LOWER"}:
            user_answer = input(f"Please indicate a valid answer [\"HIGHER\"/\"LOWER\"].\n\t> ").upper().strip()
        return user_answer

    def _start_game(self) -> None:
        """Starts and maintains a game where there are more than one category enabled."""
        # compiles and saves all enabled characteristics.
        self._match_categories = [key for key, value in self._category.items() if value]

        # performs simple check to see if there are more than two bodies inserted into the game.
        if len(self._bodies) >= 2:
            # chooses a random category and a random starting body.
            current_category = self._choose_random_category()
            left = self._choose_random_bodies(current_category)

            # continually runs the game until the player loses.
            while self._get_state():
                # chooses a random comparison body.
                right = self._choose_random_bodies(current_category)

                # starts the round and asks for the user's guess.
                response = self._new_round(left, right, current_category)

                # if the user checks correctly...
                if HigherLower._check_answer(left, right, current_category, response):
                    # confirms to the player that they made a correct answer.
                    self._print_correct_answer()

                    # increases the score of the user by 1.
                    self._increase_score()

                    # readmits the left body into the list containing all bodies.
                    self._bodies.append(left)

                    # the comparison body is now the basis for the next round.
                    left = right

                    # returns the category back to the enabled characteristic list and chooses a new random category.
                    self._return_category(current_category)
                    current_category = self._choose_random_category()

                # otherwise, they guessed incorrectly.
                else:
                    # the player lost the game and append the bodies back into the body list.
                    self._lose_game()
                    self._bodies.append(left)
                    self._bodies.append(right)

                    # prints the score report.
                    self._print_score_report(right, current_category)
        else:
            raise IndexError("HigherLower._start_game: You tried to play a game with less than 2 bodies!")

    def _start_game_single(self) -> None:
        """Starts and maintains a game where there are more than one category enabled."""
        # compiles what the solely enabled category was.
        single_category = self._find_single_category()

        # performs simple check to see if there are more than two bodies inserted into the game.
        if len(self._bodies) >= 2:
            # chooses a random starting body.
            left = self._choose_random_bodies(single_category)

            # continually runs the game until the player loses.
            while self._get_state():
                # chooses a random comparison body.
                right = self._choose_random_bodies(single_category)

                # starts the round and asks for the user's guess.
                response = self._new_round(left, right, single_category)

                # if the user checks correctly...
                if HigherLower._check_answer(left, right, single_category, response):
                    # confirms to the player that they made a correct answer.
                    self._print_correct_answer()

                    # increases the score of the user by 1.
                    self._increase_score()

                    # readmits the left body into the list containing all bodies.
                    self._bodies.append(left)

                    # the comparison body is now the basis for the next round.
                    left = right

                # otherwise, they guessed incorrectly.
                else:
                    # the player lost the game and append the bodies back into the body list.
                    self._lose_game()
                    self._bodies.append(left)
                    self._bodies.append(right)

                    # prints the score report.
                    self._print_score_report(right, single_category)
        else:
            raise IndexError("HigherLower._start_game_single: You tried to play a game with less than 2 bodies!")

    def _find_single_category(self) -> str:
        """Iterates through the list of categories, assuming it's a single game, and returns whichever is enabled."""
        # returns the first setting that is enabled.
        # this assumes that only one setting was enabled, so it short-circuit returns.
        for key, value in self._category.items():
            if value:
                return key
        else:
            raise IndexError("HigherLower._find_single_category: there were no categories enabled.")

    def _choose_random_category(self) -> str:
        """Chooses and returns a random characteristic type if it was enabled."""
        # checks if there are at least one category to choose from.
        if len(self._match_categories) >= 1:
            # shuffles the master list and returns a random characteristic type.
            random.shuffle(self._match_categories)
            return self._match_categories.pop()
        else:
            raise IndexError(f"HigherLower._choose_random_category: there were not enough categories to choose one"
                             f"at random.")

    def _choose_random_bodies(self, characteristic: str) -> {Body}:
        """Chooses and returns a random valid body."""
        # shuffles the entire list of solar system bodies.
        random.shuffle(self._bodies)

        # creates a helper function to call the appropriate getter-function for the characteristic.
        caller = getattr(Body, HigherLower._convert(characteristic))
        escape = 0

        # grabs a random body.
        body = self._bodies.pop()

        # checks to see if the body has a non-zero characteristic value.
        # the API had some values set to 0 which makes the game trivial.
        while caller(body) == 0 and escape < 1000:
            # reinserts body back into solar system bodies list.
            self._bodies.append(body)

            # reshuffles the list.
            random.shuffle(self._bodies)

            # grabs a new solar system body and increments the failsafe by 1.
            body = self._bodies.pop()
            escape += 1

        # terminates body search early if it encounters an infinite loop.
        if escape >= 1000:
            raise ValueError(f"HigherLower._choose_random_bodies: game reached a fatal infinite loop.")

        return body

    def _return_category(self, characteristic: str) -> None:
        """After choosing a random category, this returns the category back to the master list for the next round."""
        self._match_categories.append(characteristic)

    @staticmethod
    def _check_answer(left: Body, right: Body, characteristic: str, response: str) -> bool:
        """Performs the calculations and returns whether the player's guess was right or wrong."""
        # creates a helper function to call the appropriate getter-function for the characteristic.
        caller = getattr(Body, HigherLower._convert(characteristic))

        # This if-statement is unoptimal as we simply could've used logical NOT on the answers.
        # however, if you wanted to review this code, I left it this way.

        # if the user guessed higher...
        if response == "HIGHER":
            # we trivially return True if the two values are the same.
            # if they are the same, then they can't be higher OR lower.
            if characteristic != "Mass" and caller(left) == caller(right):
                print(f"\tFREE POINT!!!")
                return True

            # mass has slightly different math...
            if characteristic == "Mass":
                # we extract the scientific notation values.
                left_mass_value, left_mass_exponent = left.get_mass_raw()
                right_mass_value, right_mass_exponent = right.get_mass_raw()

                # if the exponents are different, then the larger exponent is the larger mass.
                if left_mass_exponent != right_mass_exponent:
                    return left_mass_exponent < right_mass_exponent

                # otherwise, if the exponents are the same, then we have to compare the bodies.
                else:
                    return left_mass_value <= right_mass_value
            # but otherwise, we return whether the right body is higher than the left body.
            else:
                return caller(left) <= caller(right)

        elif response == "LOWER":
            # same as above.
            if characteristic != "Mass" and caller(left) == caller(right):
                print(f"\tFREE POINT!!!")
                return True

            # same as above.
            if characteristic == "Mass":
                left_mass_value, left_mass_exponent = left.get_mass_raw()
                right_mass_value, right_mass_exponent = right.get_mass_raw()

                # same logic as above, but this time, we want to see if the mass is lower.
                if left_mass_exponent != right_mass_exponent:
                    return left_mass_exponent > right_mass_exponent
                else:
                    return left_mass_value >= right_mass_value

            # same logic as above, but we want to see if the right body is lower than the left body's characteristic.
            else:
                return caller(left) >= caller(right)
        else:
            raise ValueError(f"HigherLower._check_answer: user provided incorrect response that was uncaught.")

    ##################################################
    #           BODY CREATING FUNCTIONS              #
    ##################################################

    @staticmethod
    def _create_body(prefiltered_body: dict) -> Body | None:
        """Creates a Solar System object but filters out whether the data is invalid"""
        # attempts to acquire name, semimajor axis, and eccentricity.
        name = prefiltered_body["englishName"]
        semimajor = prefiltered_body["semimajorAxis"]
        eccentricity = prefiltered_body["eccentricity"]

        # we need to first check if mass available.
        # if it was unavailable, and we attempt to look it up, we would index non-existent things!
        if prefiltered_body['mass'] is not None:
            # we also want to see if the mass value is in the proper scientific notation format.
            # if it is not proper, then we have to fix it.
            if prefiltered_body['mass']['massValue'] > 10 or prefiltered_body['mass']['massValue'] < 1:
                fixed_mass_value, fixed_mass_exponent = HigherLower._fix_mass(prefiltered_body['mass']['massValue'],
                                                                              prefiltered_body['mass']['massExponent'])
                mass = f"{fixed_mass_value} x 10^{fixed_mass_exponent}"
                mass_raw = (fixed_mass_value, fixed_mass_exponent)
            # otherwise, we fill out the mass value and mass exponent.
            else:
                mass = f"{prefiltered_body['mass']['massValue']} x 10^{prefiltered_body['mass']['massExponent']}"
                mass_raw = (prefiltered_body["mass"]["massValue"], prefiltered_body["mass"]["massExponent"])
        else:
            mass = None
            mass_raw = None

        # attempts to acquire gravity, radius, and body type.
        gravity = prefiltered_body["gravity"]
        radius = prefiltered_body["meanRadius"]
        body_type = prefiltered_body["bodyType"]

        # if any of the fields are missing, we do not include the solar system body in our game.
        # I also removed moons that contained "S/" in them because they did not have a recognizable English name
        if None not in [name, semimajor, eccentricity, mass, gravity, radius, body_type, mass_raw] and "S/" not in name:
            return Body(name.lstrip("0123456789 "), semimajor, eccentricity, mass, gravity, radius, body_type, mass_raw)
        else:
            return None

    def _insert_bodies(self, solar_system: dict) -> None:
        compiled_bodies = list()
        # iterates through the entire solar system and inserts a Body only if it has valid data.
        for body in solar_system["bodies"]:
            temp_object = HigherLower._create_body(body)
            if temp_object is not None:
                compiled_bodies.append(temp_object)

        # check to see if the list contains any bodies.
        if compiled_bodies:
            self._bodies = compiled_bodies
        else:
            raise ValueError(f"HigherLower._insert_bodies: no Solar System bodies have been inserted.")

    @staticmethod
    def _fix_mass(massValue: float, massExponent: int) -> {float, int}:
        """Helper function that properly converts the mass into scientific notation.
        Some bodies had mass values that were greater than 10."""
        new_mass_value = massValue
        new_mass_exponent = massExponent

        # if the mass value is greater or equal to 10, then we keep dividing it by 10 until we reach a legal number.
        # we also have to increase the exponent by 1 each time.
        if massValue >= 10:
            while new_mass_value >= 10:
                new_mass_value /= 10.0
                new_mass_exponent += 1
        # if the mass value is less than 1, then we keep multiplying it by 10 until we reach a legal number.
        # we also have to decrease the exponent by 1 each time.
        else:
            while new_mass_value < 1:
                new_mass_value *= 10.0
                new_mass_exponent -= 1
        # performing multiplication or division on floats (decimals) can lead to floating point errors.
        return round(new_mass_value, 3), new_mass_exponent

    ##################################################
    #               PRINTING FUNCTIONS               #
    ##################################################

    @staticmethod
    def _print_correct_answer() -> None:
        """Simple helper that prints that the player guessed correctly."""
        print()
        print(f"!"*25)
        print(f"{' '*8}CORRECT\n")

    def _print_score_report(self, right: Body, characteristic: str) -> None:
        """Simply prints that the user made an incorrect guess."""
        caller = getattr(Body, HigherLower._convert(characteristic))
        a_or_an = 'an' if characteristic[0].lower() in {'a', 'e', 'i', 'o', 'u'} else 'a'

        print("#"*39)
        print()
        print(f"Oh no! That is unfortunately incorrect!")
        print(f"{right.get_name()} has {a_or_an} {characteristic.lower()} of {caller(right)} "
              f"{right.get_units(characteristic)}".rstrip() + ".")
        print(f"Your final score is {self._get_score()}.")
        print("Thank you for playing!")

    def _print_all_bodies(self) -> None:
        """Debugging function that prints out the traits of all Solar System bodies."""
        for body in self._bodies:
            print(f"name = {body.get_name():>20} \tsemimajor axis = {body.get_semimajor_axis():>15} \teccentricity = "
                  f"{body.get_eccentricity():>5} \tmass = {body.get_mass():>20} \tgravity = {body.get_gravity():>5} "
                  f"\tradius = {body.get_radius():>10} \tbody type = {body.get_type():>15}.")


def acquire_solar_system(url: str) -> dict:
    """Given a URL to the API, returns a Python dictionary for the parsed JSON response.
    This function structure was what as taught when I took ICS 32A with Professor Thornton"""
    url_response = None

    try:
        # open and read the URL that was provided as an argument.
        url_request = urllib.request.Request(url)
        url_response = urllib.request.urlopen(url_request)

        # extracts the website response in json format.
        extracted_json = url_response.read().decode(encoding="utf-8")
        return json.loads(extracted_json)

    finally:
        # we want to always close the response to not burden the network.
        # we should only close it if we managed to open it.
        if url_response is not None:
            url_response.close()


def acquire_offline_solar_system(file: Path) -> dict:
    """Given a json file of the Solar System API, returns a Python diction for the parsed JSON response.
    This is for offline testing to prevent creating superfluous connections to the website."""
    with open(file) as json_file:
        extracted_json = json.load(json_file)
    return extracted_json


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    website_or_file = input("Would you like to use the website or a file ['website'/'file']?\n> ")

    if website_or_file.lower() == "website":
        # loads the game from the web API.
        URL = "https://api.le-systeme-solaire.net/rest/bodies/"
        print(f"For this project, the website pulls its data from the website and API {URL}.")
        print("~-"*58, end="~\n")
        JSON = acquire_solar_system(URL)
    elif website_or_file.lower() == "file":
        # loads the game from a pre-downloaded file.
        input_file = input("Please input the file (no quotation marks).\n> ").strip("\"")

        # IF YOU WISH TO USE A PRE-DOWNLOADED FILE, GO TO THE WEBSITE ABOVE, SAVE IT
        # AND MAKE COPY IT INTO THE PATH OBJECT. REPLACE EVERY / WITH "\\"
        file_path = Path(input_file)
        JSON = acquire_offline_solar_system(file_path)
    else:
        raise ValueError("__main__: bro just type 'website' or 'file'")

    # starts the game!
    game = HigherLower(JSON)
