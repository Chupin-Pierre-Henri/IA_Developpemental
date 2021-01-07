#!/usr/bin/env python
# TODO Import the Turtlesim environment when ROS is installed
# from turtlesim_enacter import TurtleSimEnacter

# Olivier Georgeon, 2020.
# This code is used to teach Develpmental AI.


class Agent:
    def __init__(self, _hedonist_table):
        """ Creating our agent """
        self.hedonist_table = _hedonist_table
        self._action = 0
        self.anticipated_outcome = 0
        
        self.compteurEnnui = 0
        self.memoire = {}





    def action(self, outcome):
        """ Computing the next action to enact """
        # ici on regarde si le compteurEnnui est arrivé à la limite ou non fixé à 4
        # s'il a atteint cette limite alors on inverse son action prévue
        if self.compteurEnnui >= 4:
            self.compteurEnnui = 0
            if self._action == 1:
                self._action = 0
            else:
                self._action = 1

        # ici on initialise la memoire avec l'action qui est l'outcome
        if self._action not in self.memoire.keys():
            self.memoire[self._action] = outcome

        # ici si l'anticipation n'est pas égale à l'outcome alors on donne à la mémoire la valeur de l'outcome
        #à l'indice de l'action fait cet fois si
        if self.anticipated_outcome != outcome:
            self.memoire[self._action] = outcome

        #ici c'est l'anticipation précédente est égale à l'outcome actuelle
        # on augmente juste l'ennui de 1
        if self.anticipated_outcome == outcome:
            self.compteurEnnui += 1 

        

        return self._action

    def anticipation(self):
        """ computing the anticipated outcome from the latest action """
        # TODO: Implement the agent's anticipation mechanism
        #on donne à l'anticipation la valeur de la mémoire pour l'action faite
        self.anticipated_outcome = self.memoire[self._action]
        
        return self.anticipated_outcome



    def satisfaction(self, new_outcome):
        """ Computing a tuple representing the agent's satisfaction after the last interaction """
        # True if the anticipation was correct
        anticipation_satisfaction = (self.anticipated_outcome == new_outcome)
        # The value of the enacted interaction
        hedonist_satisfaction = self.hedonist_table[self._action][new_outcome]
        return anticipation_satisfaction, hedonist_satisfaction, self.compteurEnnui == 4


class Environment1:
    """ In Environment 1, action 0 yields outcome 0, action 1 yields outcome 1 """
    def outcome(self, action):
        if action == 0:
            return 0
        else:
            return 1


class Environment2:
    """ In Environment 2, action 0 yields outcome 1, action 1 yields outcome 0 """
    def outcome(self, action):
        if action == 0:
            return 1
        else:
            return 0


def world(agent, environment):
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    print("L'agent 1 fait tous le temps la même action mais au bout d'un cycle de 4 bonne anticipation il s'ennuie et change alors d'action à faire \n")
    print(" Action:  , Anticipation:  , Outcome:  , (Bonne Anticipation , Valeur Hedoniste, ennuie) \n" )
    for i in range(15):
        action = agent.action(outcome)
        outcome = environment.outcome(action)
        print(" Action: " + str(action) + ", Anticipation: " + str(agent.anticipation()) + ", Outcome: " + str(outcome)
              + ", Satisfaction: " + str(agent.satisfaction(outcome)))

compteurEnnui = 0
# TODO Define the hedonist values of interactions (action, outcome)
hedonist_table = [[-1, 1], [-1, 1]]
# TODO Choose an agent
a = Agent(hedonist_table)
# TODO Choose an environment
#e = Environment1()
e = Environment2()
# e = TurtleSimEnacter()

world(a, e)