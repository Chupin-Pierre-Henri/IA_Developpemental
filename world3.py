#!/usr/bin/env python
# TODO Import the Turtlesim environment when ROS is installed
# from turtlesim_enacter import TurtleSimEnacter

# Olivier Georgeon, 2020.
# This code is used to teach Develpmental AI.


# 
# (0, 1, 1) (0, 0, -1) (0, 0, -1) (0, 0, -1) (1, 1, 1) -- (0, 1, 1) (1, 1, 1)  (0, 1, 1) (1, 1, 1)  (0, 1, 1) (1, 1, 1)
# 

# 
# (0, 1, 1) 
# (0, 0, -1) (0, 0, -1) (0, 0, -1) 
# (1, 1, 1) -- 
# (0, 1, 1) (1, 1, 1)  (0, 1, 1) (1, 1, 1)  (0, 1, 1) (1, 1, 1)
# 

# (0, 1, 1) (0, 1, 1)    (0, 0, -1) (0, 0, -1)  

# (0, 0, -1) (0, 0, -1) (0, 0, -1) (0, 0, -1) (1, 1, 1) (1, 1, 1) (1, 1, 1) (1, 1, 1) (1, 1, 1)


class Agent:

    def __init__(self, _hedonist_table, maxEnnui):
        """ Creating our agent """
        self.hedonist_table = _hedonist_table
        self._action = 0
        self.anticipated_outcome = 0

        self.maxEnnui = maxEnnui
        self.memoire = {} # pour le prediction

        self.boolEnnui = False
        self.valActionCourante = 0 # pour boucler sur la meilleur cycle 
        self.dernieresActions = [] # dernier action effectuer. au bout maxEnnui fois la même action et anticipation correcte on s'ennuie
        self.meilleurCycle = [] # meilleur cycle des (action, outcome) à repeter

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
        
        if len(self.dernieresActions) > self.maxEnnui:
            self.dernieresActions = self.dernieresActions[1:]

        if self.anticipated_outcome != outcome:
            self.dernieresActions = [self._action]


    def changerAction(self):

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
        # The value of the enacted interaction
        hedonist_satisfaction = self.hedonist_table[self._action][new_outcome]

        return anticipation_satisfaction, hedonist_satisfaction, self.boolEnnuiFct()
        
    def boolEnnuiFct(self):
        self.boolEnnui = len(self.dernieresActions) >= self.maxEnnui and len(set(self.dernieresActions)) <= 1
        return self.boolEnnui

    #récupère la valeur hédoniste en fonction de l'action et de l'outcome
    def valHedoniste(self, action, outcome):
        return self.hedonist_table[action][outcome]

    def meilleurValHedoniste(self):
        return max([self.valHedoniste(action_outcome[0], action_outcome[1]) for action_outcome in self.meilleurCycle])

    #met à jours le meilleur cycle
    def majMeilleurCycle(self, outcome):

        #ici c'est si on à pas de cycle encore alors on lui donne la première pair (action, outcome) qu'on a
        if len(self.meilleurCycle) < 1:
            self.meilleurCycle.append((self._action, outcome))
            return

        #on récupère la valeur hédoniste
        chv_value = self.valHedoniste(self._action, outcome)
    
        #si la valeur édoniste et plus grande que la valeur du meilleur cycle alors on change le meilleur cycle par l'action outcome actuelle
        if chv_value > self.meilleurValHedoniste():
            self.valActionCourante = 0
            self.meilleurCycle = [(self._action, outcome)]

        #si on a la même valeur et que le couple (action,outcome) n'est pas dans le cycle alors on l'ajoute au cycle
        elif chv_value == self.meilleurValHedoniste() and (self._action, outcome) not in self.meilleurCycle:
            self.valActionCourante = 0
            self.meilleurCycle.append((self._action, outcome))

    #on choisi l'action à faire en fonction du meilleur cycle que l'on a
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


def world(agent, environment):
    """ The main loop controlling the interaction of the agent with the environment """
    outcome = 0
    print("L'agent 3 fonctionne avec une recherche du meilleur cycle car si il faut pour avoir de bonne valeur alterner entre 2 action ici 0 et 1 alors il doit comprendre qu'il y a un cycle à faire l'ennuie à une limite de 2 ici \n")
    print(" Action:  , Anticipation:  , Outcome:  , (Bonne Anticipation , Valeur Hedoniste, Ennuie) \n" )
    for i in range(20):
        action = agent.action(outcome)
        outcome = environment.outcome(action)
        print(" Action: " + str(action) + ", Anticipation: " +
              str(agent.anticipation()) + ", Outcome: " + str(outcome) +
              ", Satisfaction: " + str(agent.satisfaction(outcome)))


# TODO Define the hedonist values of interactions (action, outcome)
hedonist_table = [[-1, 1], [-1, 1]]
# TODO Choose an agent
a = Agent(hedonist_table, 4)
# TODO Choose an environment
#e = Environment1()
# e = Environment2()
e = Environment3()
# e = TurtleSimEnacter()

world(a, e)