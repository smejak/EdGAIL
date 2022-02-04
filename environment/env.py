import numpy as np
import random

class OLP():
    """Online Learning Platform Environment for Reinforcement Learning Agents"""
    def __init__(self) -> None:
        pass

        self.actions = ['enter', 'respond', 'submit', 'play_audio', 
                        'pause_audio', 'erase_choice', 'quit', 'pay', 
                        'play_video', 'pause_video', 'undo_erase_choice', 
                        'refund']
        self.answers = ['n', 'a', 'b', 'c', 'd']
        self.items = np.load('item_ids.npy')

        self.state = {'action_type': '', 'item_id': '', 'user_answer': 'n', 'time_spent': 0}
        self.current_state = {'action_type': '', 'item_id': '', 'user_answer': 'n', 'time_spent': 0}
        self.states = []
    
    def init_state(self) -> list:
        """Get the initial random state"""
        action = random.choice(self.actions)
        item = random.choice(self.items)
        
        self.current_state['action_type'] = action
        self.current_state['item_id'] = item
        self.states.append(current_state)
    
    def step(self, agent):
        self.current_state['time_spent'] += 1
        self.current_state['item_id'] = agent.choose_item(self.current_state)
        self.current_state['action_type'] = agent.choose_action(self.current_state)
        if self.current_state['action_type'] == 'respond':
            self.current_state['user_answer'] = agent.choose_answer(self.current_state)
        else:
            self.current_state['user_answer'] = 'n'
        
        self.states.append(current_state)