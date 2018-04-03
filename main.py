from random import shuffle
from sys import argv as ag
import math

class Individual:
    # strategy 0: dove
    # strategy 1: hawk
    id = 0
    resource = 0
    strategy = 0
    is_dead = False

    def __init__(self, id, strategy, resource=0):
        self.id = id
        self.strategy = strategy
        self.resource = resource

    def update_resource(self, value):
        self.resource += value

    def print_type(self):
        strategy_type = "Dove" if self.strategy is 0 else "Hawk"
        print("Individual {}: {}".format(self.id, strategy_type))

    def __str__(self):
        return "Individual {}={}".format(self.id, self.resource)


def display_out(type, prior,
                first_player,
                second_player):

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
    strategy = player_one.strategy + player_two.strategy
    # display the types
    priority = 1 if player_one.strategy >= player_two.strategy else 2

    display_out(1, priority, player_one, player_two)

    if strategy == 0:
        print("Dove/Dove: Dove: +{}	Dove: +{}".format(resource/2, resource/2))
        player_one.resource += resource/2
        player_two.resource += resource/2

        display_out(2, priority, player_one, player_two)

    elif strategy == 1:
        print("Hawk/Dove: Hawk: +{}	Dove: +0".format(resource))
        if player_one.strategy > player_two.strategy:
            player_one.resource += resource
        else:
            player_two.resource += resource

        display_out(2, priority, player_one, player_two)

    else:
        hawk_attack1 = resource - hawk_attack
        hawk_attack2 = hawk_attack1 - hawk_attack

        op1 = "" if hawk_attack1 < 0 else "+"
        op2 = "" if hawk_attack2 < 0 else "+"

        print("Hawk/Hawk: Hawk: {}{}	Hawk: {}{}".format(op1, hawk_attack1, op2, hawk_attack2))
        player_one.resource += hawk_attack1
        player_two.resource += hawk_attack2
        if player_one.resource < 0:
            print("Hawk one has died!")
            player_one.is_dead = True
            pop_num -= 1
        if player_two.resource < 0:
            print("Hawk two has died!")
            player_two.is_dead = True
            pop_num -= 1

        display_out(2, priority, player_one, player_two)


    print("")
    return pop_num


def populate (hawk_size, dove_size):

    hawks = [Individual(i, 1) for i in range(hawk_size)]
    doves = [Individual(j + hawk_size, 0) for j in range(dove_size)]
    population = hawks + doves
    return population



def encounter_simulate(population,
                       n,
                       pop_size,
                       resource,
                       hawk_cost):

    cur = 1
    total_alive = pop_size

    while cur <= n and total_alive > 1:

        shuffle(population)
        first_player = population[0]
        second_player = population[1]
        if not first_player.is_dead and not second_player.is_dead:
            total_alive = battle(first_player, second_player, total_alive, resource, hawk_cost)
            cur += 1


def display_menu():
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

    if 1 < len(ag) < 6:
        try:
            pop_size = int(ag[1])
            hawk_percent = 20 if len(ag) < 3 else float(ag[2])
            resource = 50 if len(ag) < 4 else int(ag[3])
            hawk_cost = 100 if len(ag) < 5 else int(ag[4])
            hawk_size = math.trunc((hawk_percent / 100.0) * pop_size)
            dove_size = pop_size - hawk_size
            hawk_list = []
            population = populate(hawk_size, dove_size)

            display_menu()
            encounters = int(input())







            encounter_simulate(population, encounters, pop_size, resource, hawk_cost)

        except OSError as ose:
            print("OS Error: {}".format(ose))

        except ValueError as ve:
            print("Cannot convert the type <String> into int explicitly.")

        except IndexError as ie:
            print("Usage: ./project02 popSize [percentHawks] [resourceAmt] [costHawk-Hawk]")

    else:
        print("Usage: ./project02 popSize [percentHawks] [resourceAmt] [costHawk-Hawk]")











