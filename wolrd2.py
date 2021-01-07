#!/usr/bin/env python
# TODO Import the Turtlesim environment when ROS is installed
# from turtlesim_enacter import TurtleSimEnacter

# Olivier Georgeon, 2020.
# This code is used to teach Develpmental AI.


class Agent:
    def __init__(self, _hedonist_table, maxEnnui):
        """ Creating our agent """
        self.hedonist_table = _hedonist_table
        self._action = 0
        self.anticipated_outcome = 0

        self.maxEnnui = maxEnnui
        self.memoire = {}

        self.bonneAnticipationCompteur = 0
        self.actionPrefereCompteur = 0
        self.actionPrefere = 0
        self.outcomePrefere = 0
        self.derniereAction = 0


    #la grande différence est qu'ici on à une action preféré (celle qui rapporte le plus) et on suit cet action au maximum
    def action(self, outcome):
        """ Computing the next action to enact """
        if self.valMeilleurHedonist(outcome):
            self.actionPrefere = self._action
            self.outcomePrefere = outcome
            self.actionPrefereCompteur = 0

        self._action = self.actionPrefere

        #si il s'ennuie on change d'action et on remet les compteurs à zéro
        if self.boolEnnui(): self.changerAction()

        #on met à jour la mémoire en fonction de l'outcome comme pour l'agent 1
        self.majMemoire(outcome)

        #on met à jours le compte de bonne anticipation faite et d'action préféré faite
        self.majCompteur(outcome)
        
        self.derniere_action = self._action
        return self._action

    def majMemoire(self, outcome):
        if self._action not in self.memoire.keys():
            self.memoire[self._action] = outcome
        elif self.anticipated_outcome != outcome:
            self.memoire[self.derniere_action] = outcome

    def majCompteur(self, outcome):
        if self.anticipated_outcome == outcome:
            self.bonneAnticipationCompteur += 1

        if self.actionPrefere == self._action:
            self.actionPrefereCompteur += 1

    def valMeilleurHedonist(self, outcome):
        return self.hedonist_table[self._action][
            outcome] > self.hedonist_table[self.actionPrefere][self.outcomePrefere]

    def changerAction(self):
        self.bonneAnticipationCompteur = 0
        self.actionPrefereCompteur = 0
        if self._action == 1:
            self._action = 0
        else:
            self._action = 1

    def anticipation(self):
        """ computing the anticipated outcome from the latest action """
        # TODO: Implement the agent's anticipation mechanism

        self.anticipated_outcome = self.memoire[self._action]

        return self.anticipated_outcome

    def boolEnnui(self):
        return self.bonneAnticipationCompteur >= self.maxEnnui and self.actionPrefereCompteur >= self.maxEnnui

    def satisfaction(self, new_outcome):
        """ Computing a tuple representing the agent's satisfaction after the last interaction """
        # True if the anticipation was correct
        anticipation_satisfaction = (self.anticipated_outcome == new_outcome)
        # The value of the enacted interaction
        hedonist_satisfaction = self.hedonist_table[self._action][new_outcome]

        return anticipation_satisfaction, hedonist_satisfaction, self.boolEnnui(
        )


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
    print("L'agent 2 cherche à faire la meilleur action mais il peut s'ennuier comme l'agent 1 et alors il change d'action juste un fois pour tester de nouveau horizon \n")
    print(" Action:  , Anticipation:  , Outcome:  , (Bonne Anticipation , Valeur Hedoniste, Ennuie) \n" )
    for i in range(15):
        action = agent.action(outcome)
        outcome = environment.outcome(action)
        print(" Action: " + str(action) + ", Anticipation: " +
              str(agent.anticipation()) + ", Outcome: " + str(outcome) +
              ", Satisfaction: " + str(agent.satisfaction(outcome)))


bonneAnticipationCompteur = 0
# TODO Define the hedonist values of interactions (action, outcome)
hedonist_table = [[-1, 1], [-1, 1]]
# TODO Choose an agent
a = Agent(hedonist_table, 4)
# TODO Choose an environment
e = Environment1()
# e = Environment2()
# e = TurtleSimEnacter()

world(a, e)