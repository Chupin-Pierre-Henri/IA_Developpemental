#!/usr/bin/env python
# TODO Import the Turtlesim environment when ROS is installed
# from turtlesim_enacter import TurtleSimEnacter

# Olivier Georgeon, 2020.
# This code is used to teach Develpmental AI.


#comparé à l'agent 3 ici on récupère la fréquence des cycles pour pouvoir supprimer des meilleurCycle les cycles qui ne sont plus fait par l'agent
#cela permet à l'agent de s'adapter au changement d'environnement
class Agent:

    def __init__(self, _hedonist_table, maxEnnui):
        """ Creating our agent """
        self.hedonist_table = _hedonist_table
        self._action = 0
        self.anticipated_outcome = 0

        self.maxEnnui = maxEnnui
        self.memoire = {} # pour le prediction

        self.meilleurCycle = [] # meilleur cycle des (action, outcome) à repeter
        self.dernieresActions = [] # dernier action effecuter. 
        self.valActionCourante = 0 # pour boucler sur la meilleur cycle 
        self.frequenceActionsOutcome = {}
        


    def action(self, outcome):
        """ Computing the next action to enact """

        self.majMeilleurCycle(outcome)
        
        self.majMemoire(outcome)

        self._action = self.choisirAction()

        if self.boolEnnuiFct(): self.changerAction()

        if self._action not in self.memoire.keys():
            self.memoire[self._action] = outcome

        self.majCompteur(outcome)

        return self._action

    def majMemoire(self, outcome):
        if self.anticipated_outcome != outcome:
            self.memoire[self._action] = outcome

    def majCompteur(self, outcome):

        self.dernieresActions.append(self._action)
        
        if len(self.dernieresActions) > self.maxEnnui * len(self.meilleurCycle):
            self.dernieresActions = self.dernieresActions[1:]
        
        if self.anticipated_outcome != outcome:
            self.dernieresActions = [self._action]

    def majFrequence(self):
        tupleASuppr = []
        for action_outcome in self.frequenceActionsOutcome.keys():
            frequence = self.frequenceActionsOutcome[action_outcome]
            self.frequenceActionsOutcome[action_outcome] = 0
            if frequence < 1:
                if action_outcome in self.meilleurCycle:
                    self.meilleurCycle.remove(action_outcome)
                    tupleASuppr.append(action_outcome)
        
        for key_to_del in tupleASuppr:
            del self.frequenceActionsOutcome[key_to_del]

    def changerAction(self):

        # print(self.meilleurCycle)
        # print(self.frequenceActionsOutcome)

        self.majFrequence()



        self.dernieresActions = []

        self.valActionCourante = 0

        if self._action == 1:
            self._action = 0
        else:
            self._action = 1

    def anticipation(self):
        """ computing the anticipated outcome from the latest action """
        # TODO: Implement the agent's anticipation mechanism

        self.anticipated_outcome = self.memoire[self._action]

        return self.anticipated_outcome

    def satisfaction(self, new_outcome):
        """ Computing a tuple representing the agent's satisfaction after the last interaction """
        # True if the anticipation was correct
        anticipation_satisfaction = (self.anticipated_outcome == new_outcome)
        self.goodAnticipation = anticipation_satisfaction
        # The value of the enacted interaction
        hedonist_satisfaction = self.hedonist_table[self._action][new_outcome]

        return anticipation_satisfaction, hedonist_satisfaction, self.boolEnnuiFct()


    def boolEnnuiFct(self) -> bool:
        if len(self.dernieresActions) < self.maxEnnui * len(self.meilleurCycle):
            return False

        meilleurCycle_actions = []
        for action_outcome in self.meilleurCycle:
            meilleurCycle_actions.append(action_outcome[0])

        nbCycleEnAction = self.nbCycle(self.dernieresActions, meilleurCycle_actions)

        return nbCycleEnAction >= self.maxEnnui


    def nbCycle(self, actions, cycle) -> int:

        if len(cycle) < 1: return 0

        i = len(actions)
        nb_eq = 0
        while i >= len(cycle):
            c = actions[i - len(cycle): i]
            if cycle != c:
                return nb_eq
            nb_eq += 1
            i -= len(cycle)

        return nb_eq


    def valHedoniste(self, action, outcome):
        return self.hedonist_table[action][outcome]

    def meilleurValHedoniste(self):
        return max([self.valHedoniste(action_outcome[0], action_outcome[1]) for action_outcome in self.meilleurCycle])

    def majMeilleurCycle(self, outcome):

        action_outcome = (self._action, outcome)

        if action_outcome not in self.frequenceActionsOutcome.keys():
            self.frequenceActionsOutcome[action_outcome] = 1
        else: self.frequenceActionsOutcome[action_outcome] += 1


        if len(self.meilleurCycle) < 1:
            self.meilleurCycle.append(action_outcome)
            return

        chv_value = self.valHedoniste(self._action, outcome)
    
        if chv_value > self.meilleurValHedoniste():
            self.valActionCourante = 0
            self.meilleurCycle = [action_outcome]

        elif chv_value == self.meilleurValHedoniste() and action_outcome not in self.meilleurCycle:
            self.valActionCourante = 0
            self.meilleurCycle.append(action_outcome)

    def choisirAction(self):
        action_outcome = self.meilleurCycle[self.valActionCourante]
        
        self.valActionCourante += 1
        if self.valActionCourante >= len(self.meilleurCycle):
            self.valActionCourante = 0

        return action_outcome[0]


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


class Environment3:

    previous_action = 0

    def outcome(self, action):
        if action == self.previous_action:
            outcome = 0
        else:
            outcome = 1
        self.previous_action = action
        return outcome



class Environment4:

    env = Environment1()
    count = 0

    def outcome(self, action):
        if self.count < 10:
            self.count += 1
        elif self.count == 10:
            print("changment d'Environment")
            self.env = Environment2()
            self.count += 1
        elif self.count < 25:
            self.count += 1
        elif self.count == 25:
            print("changment d'Environment")
            self.env = Environment3()
            self.count += 1
        
        return self.env.outcome(action)


def add_space(i):
    if i < 10: return ' '
    return ''

def world(agent, environment):
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    for i in range(40):
        action = agent.action(outcome)
        outcome = environment.outcome(action)
        print('i:' + str(i) + add_space(i) + " Action: " + str(action) + ", Anticipation: " +
              str(agent.anticipation()) + ", Outcome: " + str(outcome) +
              ", Satisfaction: " + str(agent.satisfaction(outcome)))


# TODO Define the hedonist values of interactions (action, outcome)
hedonist_table = [[-1, 1], [-1, 1]]
# TODO Choose an agent
a = Agent(hedonist_table, 4)
# TODO Choose an environment
# e = Environment1()
# e = Environment2()
# e = Environment3()
e = Environment4()
# e = TurtleSimEnacter()

world(a, e)