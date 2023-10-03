default_name = "Unknown"
default_score = 0


class Score:
    file_path = "resources/local/score.csv"

    def __init__(self, score: int = default_score, name: str = default_name):
        self.score = score
        self.name = name

    def __str__(self):
        return str(self.score) + "  " + self.name

    def record(self):
        with open(self.file_path, "a") as f:
            f.writelines(self.name + "," + str(self.score) + "\n")


def get_max_score() -> Score:
    max_score = Score()
    try:
        with open("resources/local/score.csv", "r") as f:
            for line in f.readlines():
                n, s = line.split(",")
                now_score = Score(int(s), n)
                if now_score.score > max_score.score:
                    max_score = now_score
            return max_score
    except FileNotFoundError:
        return Score()
