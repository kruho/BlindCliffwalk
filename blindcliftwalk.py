import numpy as np


    
    
class BlindCliftwalk(object):
    def __init__(self, nb_step, nb_goals):
        self.nb_step = nb_step
        self.nb_goals = nb_goals
        self.fall_marker = 0
        self.ontheway_marker = 1
        self.start_marker = 2
        self.goal_marker = 3
    
    
    def random_action(self):
        '''
            ランダムな行動
              [1,0] : 下に進む
              [0,1] : 右に進む
            '''
        rand = np.random.random(1)
        return np.eye(2)[int(np.floor(rand+0.5))].astype(int)


    def transition(self, s, a):
        return s + a
    
    
    def set_ground_truth(self):
        # 答えの初期化
        self.ground_truth = np.ones((self.nb_step, self.nb_step), dtype=int)
        self.ground_truth = self.ground_truth * self.fall_marker

        for _ in range(self.nb_goals):
            # 初期状態は座標(0,0)とする。
            state = np.zeros(2, dtype=int)

            # 開始位置の値は2にする（色分けのため）。
            self.ground_truth[state[0], state[1]] = self.start_marker

            # ゴールまでの道中を1にする。
            for i in range(self.nb_step):
                state = self.transition(state, self.random_action())
                self.ground_truth[state[0], state[1]] = self.ontheway_marker

            # ゴールの値は3。state=3で報酬が+1される。
            self.ground_truth[state[0], state[1]] = self.goal_marker
            
           
    def get_reward(self, state):
        if self.ground_truth[state[0], state[1]]==self.goal_marker:
            # ゴールにたどり着いたら報酬は+1
            reward = 1
            status = 1
        elif self.ground_truth[state[0], state[1]]==self.fall_marker:
            # 落とし穴に落ちたら報酬は0
            reward = 0
            status = -1
        else:
            # 道中の報酬は0
            reward = 0
            status = 0
        return reward, status
        