class Game:
    discord_id: int
    points_to_win: int
    player_score: int
    bot_score: int
    prompt: str
    player_response: str
    bot_response: str
    evil_mode: bool
    
    def __init__(self, discord_id: int, points_to_win: int, evil_mode: bool):
        self.discord_id = discord_id
        self.points_to_win = points_to_win
        self.player_score = 0
        self.bot_score = 0
        self.prompt = ""
        self.player_response = ""
        self.bot_response = ""
        self.evil_mode = evil_mode
    
    def has_winner(self) -> bool:
        return max(self.player_score, self.bot_score) >= self.points_to_win