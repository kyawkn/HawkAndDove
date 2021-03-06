# file: Main.py
# @author: Kyaw Khant Nyar (kxk3035@rit.edu)

import random
from sys import argv as ag
from sys import exit
import math


class Individual:
    """
    Individual is a class object that has attribute, id, and resource
    value as attributes
    """
    # strategy 0: dove
    # strategy 1: hawk
    id = 0
    resource = 0
    strategy = 0
    is_dead = False

    def __init__(self, id, strategy, resource=0):
        """
        initialize an individual
        :param id: individual's id
        :param strategy: individual's strategy
        :param resource: amount of resource they currently own
        """
        self.id = id
        self.strategy = strategy
        self.resource = resource

    def update_resource(self, value):
        # update the resource
        self.resource += value

    def print_type(self):
        # print the individual and its strategy type
        strategy_type = "Dove" if self.strategy is 0 else "Hawk"
        print("Individual {}: {}".format(self.id, strategy_type))

    def __str__(self):
        # str return Individual's id and its resource
        return "Individual {}={}".format(self.id, self.resource)


def display_out(type, prior,
                first_player,
                second_player):
    """
    prints out display stats
    :param type: type of display
    :param prior: priority, hawk is displayed first
    :param first_player: first individual
    :param second_player: second individual
    :return: none
    """

    if type == 1:
        if prior == 1:
            first_player.print_type()
            second_player.print_type()

        elif prior == 2:
            second_player.print_type()
            first_player.print_type()

    else:
        if prior == 1:
            print("{} {}".format(str(first_player), str(second_player)))
        else:
            print("{} {}".format(str(second_player), str(first_player)))


def battle(player_one,
           player_two,
           pop_num,
           resource,
           hawk_attack
           ):
    """
    run one competition of two random individuals using their strategy types
    :param player_one: first random individual
    :param player_two: second random individual
    :param pop_num: population of alive individuals
    :param resource: resource number to compete
    :param hawk_attack: Hawk-Hawk interaction cost
    :return: population of alive individuals
    """
    strategy = player_one.strategy + player_two.strategy
    # display the types
    priority = 1 if player_one.strategy >= player_two.strategy else 2

    # display individual id, and its strategy
    display_out(1, priority, player_one, player_two)

    # Dove-Dove
    if strategy == 0:
        half_res = math.trunc(resource/2)
        print("Dove/Dove: Dove: +{}	Dove: +{}".format(half_res, half_res))
        player_one.resource += half_res
        player_two.resource += half_res

        display_out(2, priority, player_one, player_two)

    # Hawk-Dove
    elif strategy == 1:
        print("Hawk/Dove: Hawk: +{}	Dove: +0".format(resource))
        if player_one.strategy > player_two.strategy:
            player_one.resource += resource
        else:
            player_two.resource += resource

        display_out(2, priority, player_one, player_two)

    # Hawk-Hawk
    else:
        # Hawk cost
        hawk_attack1 = resource - hawk_attack
        hawk_attack2 = hawk_attack1 - hawk_attack

        # display if Hawk is gaining or losing resource
        op1 = "" if hawk_attack1 < 0 else "+"
        op2 = "" if hawk_attack2 < 0 else "+"

        print("Hawk/Hawk: Hawk: {}{}	Hawk: {}{}".format(op1, hawk_attack1, op2, hawk_attack2))
        player_one.resource += hawk_attack1
        player_two.resource += hawk_attack2
        # check any casualty
        if player_one.resource < 0:
            print("Hawk one has died!")
            player_one.is_dead = True
            pop_num -= 1
        if player_two.resource < 0:
            print("Hawk two has died!")
            player_two.is_dead = True
            pop_num -= 1

        display_out(2, priority, player_one, player_two)

    print("")  # line break
    return pop_num


def populate (hawk_size, dove_size):
    """
    create an array of individuals using the size of hawks and doves
    :param hawk_size: hawk size
    :param dove_size: dove size
    :return: an array of individuals
    """
    hawks = [Individual(i, 1) for i in range(hawk_size)]
    doves = [Individual(j + hawk_size, 0) for j in range(dove_size)]
    population = hawks + doves
    return population


def encounter_simulate(population,
                       n,
                       pop_size,
                       resource,
                       hawk_cost):
    """
    simulate n encounters by randomly choosing two alive individuals and call
    battle to compete for the resource, and exit if all individuals are dead
    :param population: array of individuals
    :param n: number of encounters
    :param pop_size: size of the population
    :param resource: resource to compete
    :param hawk_cost: Hawk-Hawk interaction cost
    :return: None
    """
    cur = 1  # keep tracks of the iteration number
    total_alive = pop_size

    for i in range(0, n):

        first_player = random.choice(population)
        second_player = random.choice(population)
        if not first_player.is_dead and not second_player.is_dead \
                and first_player != second_player:
            total_alive = battle(first_player, second_player, total_alive, resource, hawk_cost)
            if total_alive <= 1:
                break

    if total_alive < 2:
        print("No more living individual is left.\n")
        exit(0)


def display_member(population):
    """
    print out the individuals and their resources
    :param population: array of individuals
    :menu choice: 2
    """
    new_population = sorted(population, key=lambda x: x.id)  # sort individuals by id
    livings = 0

    # loop and prints
    for ind in new_population:
        # check num of livings
        livings += 1 if ind.resource >= 0 else 0
        ind_id = ind.id
        ind_type = "Hawk" if ind.strategy > 0 else "Dove"
        ind_type_status = "DEAD" if ind.is_dead else ind_type
        rsr = ind.resource

        print("Individual[{}]={}:{}".format(ind_id, ind_type_status, rsr))
    print("Living: {}".format(livings))


def display_resource_sort(population):
    """
    display the resources along with the strategy types or DEAD if
    an Individual has negative resource
    :param population: list of the Individuals
    :menu choice: 3
    """
    new_pop = sorted(population, key=lambda x: x.resource,  reverse=True)
    for ind in new_pop:
        # check type
        ind_type = "Hawk" if ind.strategy > 0 else "Dove"
        ind_type_status = "DEAD" if ind.is_dead else ind_type
        print("{}:{}".format(ind_type_status, ind.resource))


def display_stats(pop_size,
                  hawk_per,
                  hawks,
                  dove_per,
                  doves,
                  resource,
                  hawk_cost):
    """
    format and display the stats
    menu choice: 1
    """
    print('Population size: {}\n'
          'Percentage of Hawks: {}%\n'
          'Number of Hawks: {}\n\n'
          'Percentage of Doves: {}%\n'
          'Number of Doves: {}\n\n'
          'Each resource is worth: {}\n'
          'Cost of Hawk-Hawk interaction: {}\n'.format(pop_size, hawk_per, hawks,
                                                       dove_per, doves, resource, hawk_cost))

def display_menu():
    """
    display the menu
    """
    print('===============MENU=============\n'
          '1 ) Starting Stats\n'
          '2 ) Display Individuals and Points\n'
          '3 ) Display Sorted\n'
          '4 ) Have 1000 interactions\n'
          '5 ) Have 10000 interactions\n'
          '6 ) Have N interactions\n'
          '7 ) Step through interactions \"Stop\" to return to menu\n'
          '8 ) Quit\n'
          '================================\n')


if __name__ == '__main__':
    """
    the main method takes in the arguments and process them accordingly
    by calling appropriate functions
    """
    # check arg nums
    if 1 < len(ag) < 6:
        try:
            # data
            pop_size = int(ag[1])
            hawk_percent = 20 if len(ag) < 3 else float(ag[2])
            resource = 50 if len(ag) < 4 else int(ag[3])
            hawk_cost = 100 if len(ag) < 5 else int(ag[4])
            hawk_size = math.trunc((hawk_percent / 100.0) * pop_size)
            dove_size = pop_size - hawk_size
            population = populate(hawk_size, dove_size)

            choice = ""  # menu choice init as an empty string
            while choice != 8:
                """
                only enter 8 can lead to end of program
                """
                print ("")  # empty line
                display_menu()
                try:
                    choice = int(input("> "))  # type cast into integers

                    if choice == 1:
                        display_stats(pop_size, hawk_percent, hawk_size, 100 - hawk_percent, dove_size, resource, hawk_cost )
                    elif choice == 2:
                        display_member(population)
                    elif choice == 3:
                        display_resource_sort(population)
                    elif choice == 4:
                        encounter_simulate(population, 1000, pop_size, resource, hawk_cost)
                    elif choice == 5:
                        encounter_simulate(population, 10000, pop_size, resource, hawk_cost)
                    elif choice == 6:
                        try:
                            n = int(input("N: "))
                            encounter_simulate(population, n, pop_size, resource, hawk_cost)
                        except ValueError or EOFError:
                            print("<N> must be an integer!")
                    elif choice == 7:
                        cmd = ""

                        while cmd != "Stop":
                            encounter_simulate(population, 1, pop_size, resource, hawk_cost)
                            try:
                                cmd = input()
                            except EOFError:
                                pass
                    else:
                        pass

                except ValueError:
                    pass

        # exception handling for erroneous inputs
        except OSError as ose:
            print("OS Error: {}".format(ose))

        except ValueError as ve:
            print("Cannot convert the type <String> into int explicitly.")

        except IndexError as ie:
            print("Usage: python main.py popSize [percentHawks] [resourceAmt] [costHawk-Hawk]")

    else:
        print("Usage: python main.py popSize [percentHawks] [resourceAmt] [costHawk-Hawk]")











