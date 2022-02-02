

class OLP():
    """Online Learning Platform Environment for Reinforcement Learning Agents"""
    def __init__(self) -> None:
        pass

        self.actions = ['enter', 'respond', 'submit', 'play_audio', 
                        'pause_audio', 'erase_choice', 'quit', 'pay', 
                        'play_video', 'pause_video', 'undo_erase_choice', 
                        'refund' ]

        self.state = ['action_type', 'item_id', 'user_answer', 'time_spent']