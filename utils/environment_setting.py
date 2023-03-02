from gym_derk.envs import DerkEnv
import random
import numpy as np


class CustomEnvironment():
    def __init__(self,dx=0.5,dr=0.3,training_mode =False,turbo_mode=True):
        self.ht_primary_col = '#FF0000' #red    
        self.ht_secondary_col = '#FFA500' #orange
        self.at_primary_col = '#ADD8E6' #light blue
        self.at_secondary_col = '#FFFFFF' #white 
        self.arms = ['Talons','BloodClaws','Cleavers',
                    'Cripplers','Pistol','Magnum','Blaster']
        self.miscs = ['FrogLegs','IronBubblegum',
                        'HeliumBubblegum','Shell','Trombone']
        self.tails = ['VampireGland','ParalyzingDart']
        self.healing_tail = ['HealingGland']

        self.training_mode = training_mode


        self.home_team_conf =  self.team_conf('home')
        self.away_team_conf = self.team_conf('away')
        

        self.env = DerkEnv( turbo_mode=turbo_mode,
                home_team = self.home_team_conf,
                away_team = self.away_team_conf)
        
        self.action_space = Discrete_actions_space(dx,dr)
        


    def team_conf_4_evaluation(self,team):
        player_1_slots = [
            random.sample(self.arms,1)[0],
            random.sample(self.miscs,1)[0],
            random.sample(self.tails,1)[0]
        ]
        player_2_slots = [
            random.sample(self.arms,1)[0],
            random.sample(self.miscs,1)[0],
            random.sample(self.tails,1)[0]
        ]
        healer_player_slots = [
            random.sample(self.arms,1)[0],
            random.sample(self.miscs,1)[0],
            self.healing_tail
        ]
        if team == 'home':
            primary_color = self.ht_primary_col
            secondary_color = self.ht_secondary_col
        else:
            primary_color = self.at_primary_col
            secondary_color = self.at_secondary_col

        team_conf = [
            {'primaryColor': primary_color,
             'secondaryColor':secondary_color,
             'slots':player_1_slots,
             'rewardFunction':  { 'damageEnemyUnit': 0.1 ,
                                 'damageEnemyStatue': 0.2 ,
                                 'friendlyFire': -0.1,
                                 'killEnemyStatue': 4,
                                 'killEnemyUnit': 1}
            },
            {'primaryColor': primary_color,
             'secondaryColor':secondary_color,
             'slots':healer_player_slots,
             'rewardFunction':  { 'healTeammate1': 0.1 ,
                                 'healTeammate2': 0.1 ,
                                 'healFriendlyStatue': 0.2 ,
                                 'healEnemy': -0.1 ,
                                 'friendlyFire': -0.1,
                                 'killEnemyStatue': 4,
                                 'killEnemyUnit': 1}
            },
            {'primaryColor': primary_color,
             'secondaryColor':secondary_color,
             'slots':player_2_slots,
             'backSpikes':3,
             'rewardFunction':  { 'damageEnemyUnit': 0.1 ,
                                 'damageEnemyStatue': 0.2 ,
                                 'friendlyFire': -0.1,
                                 'killEnemyStatue': 4,
                                 'killEnemyUnit': 1}
            }]
            
        return team_conf
    
    def team_conf(self,team):
        if team == 'home':
            primary_color = self.ht_primary_col
            secondary_color = self.ht_secondary_col
        else:
            primary_color = self.at_primary_col
            secondary_color = self.at_secondary_col
        
        if self.training_mode:
            generic_rewards = {'damageEnemyUnit': 1 ,
                            'damageEnemyStatue': 2 ,
                            'healTeammate1': 1 ,
                            'healTeammate2': 1 ,
                            'healFriendlyStatue': 2 ,
                            'healEnemy': -10 ,
                            'friendlyFire': -10,
                            'killEnemyStatue': 50,
                            'killEnemyUnit': 20}
        else:
            generic_rewards = {'killEnemyStatue': 4,
                            'killEnemyUnit': 1}

        
        player_1_slots = [
            'Pistol',
            None,#'Talons',
            None#'Trombone'
        ]
        player_2_slots = [
            'Cripplers',
            None,   #'Magnum',
            None        #'Shell'
        ]
        healer_player_slots = [
            'HealingGland',
            None,#'Pistol',
            None        #'BloodClaws'
            
        ]

        team_conf = [
            {'primaryColor': primary_color,
             'secondaryColor':secondary_color,
             'slots':player_1_slots,
             'backSpikes':1,
             'rewardFunction':generic_rewards
            },
            {'primaryColor': primary_color,
             'secondaryColor':secondary_color,
             'slots': player_2_slots,
             'backSpikes':7,
             'rewardFunction': generic_rewards
            },
            {'primaryColor': primary_color,
             'secondaryColor':secondary_color,
             'slots':healer_player_slots ,
             'rewardFunction': generic_rewards
            }]
          
        return team_conf



    def reset(self):
        self.env.reset()


class Discrete_actions_space():#DerkEnv.action_space):

    def __init__(self,dx,dr):
        
        self.action_len = 5

        self.dx = dx
        self.dr = dr
        self.count = 13#14
        self.actions = {}
        self.actions_computation()
        self.n_agents = 3
        
    
    '''def actions_computation(self):
        self.actions[0] = [0,0,0,0,0]               #do nothing
        self.actions[1] = [self.dx,0,0,0,0]         #move +
        self.actions[2] = [-self.dx,0,0,0,0]        #move -
        self.actions[3] = [0,self.dr,0,0,0]         #rotate +
        self.actions[4] = [0,-self.dr,0,0,0]        #rotate -
        self.actions[5] = [0,0,1,0,0]               #chase focus
        
        self.actions[6]= [0,0,0,0,1]               # change focus to i = 1
        self.actions[7] = [0,0,0,0,2]              # change focus to i = 2
        self.actions[8] = [0,0,0,0,3]              # change focus to i = 3
        self.actions[9]  = [0,0,0,0,4]              # change focus to i = 4
        self.actions[10] = [0,0,0,0,5]              # change focus to i = 5
        self.actions[11] = [0,0,0,0,6]              # change focus to i = 6
        self.actions[12] = [0,0,0,0,7]              # change focus to i = 7
        self.actions[13] = [0,0,0,1,0]               #cast ability 1
        #self.actions[14] = [0,0,0,2,0]               #cast ability 2
        #self.actions[15] = [0,0,0,3,0]               #cast ability 3
        # with i:   1=focus home statue. 2-3=focus teammates, 4=focus enemy statue, 5-7=focus enemy'''
    
    def sample(self):
        keys = random.sample(range(0, self.count-1), self.n_agents)
        actions = [self.actions[k] for k in keys]
        
        return [keys,actions]

    def actions_computation(self):
        self.actions[0] = [0,0,0,0,0]               #do nothing
        self.actions[1] = [self.dx,0,0.1,0,0]         #move +
        self.actions[2] = [-self.dx,0,0.1,0,0]        #move -
        self.actions[3] = [0,self.dr,0.1,0,0]         #rotate +
        self.actions[4] = [0,-self.dr,0.1,0,0]        #rotate -
        self.actions[5]= [0,0,0,1,1]                # cast ability on i = 1
        self.actions[6] = [0,0,0,1,2]               # cast ability on i = 2
        self.actions[7] = [0,0,0,1,3]               # cast ability on i = 3
        self.actions[8]  = [0,0,0,1,4]              # cast ability on i = 4
        self.actions[9] = [0,0,0,1,5]              # cast ability on i = 5
        self.actions[10] = [0,0,0,1,6]              # cast ability on i = 6
        self.actions[11] = [0,0,0,1,7]              # cast ability on i = 7
        self.actions[12] = [0,0,1,0,0]               #chase focus
        #with i:   1=focus home statue. 2-3=focus teammates, 4=focus enemy statue, 5-7=focus enemy'''




