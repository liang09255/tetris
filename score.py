import string
import time

default_name = "Unknown"
default_score = 0


class Score:
    file_path = "resources/local/score.csv"

    def __init__(self, score: int = default_score, name: str = default_name, t: int = 0, tt: int = int(time.time())):
        self.score = score
        self.name = name
        self.t = t  # 游戏用时
        self.tt = tt  # 记录生成时间

    def record(self):
        with open(self.file_path, "a") as f:
            s = ",".join([self.name, str(self.score), str(self.t), str(self.tt)])
            f.writelines(s + "\n")


def get_max_score() -> Score:
    max_score = Score()
    try:
        with open("resources/local/score.csv", "r") as f:
            for line in f.readlines():
                n, s, t, tt = line.split(",")
                now_score = Score(int(s), n, t, tt)
                if now_score.score > max_score.score:
                    max_score = now_score
            return max_score
    except FileNotFoundError:
        return Score()
