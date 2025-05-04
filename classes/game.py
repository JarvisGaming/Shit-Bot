class Game:
    discord_id: int
    points_to_win: int
    player_score: int
    bot_score: int
    prompt: str
    player_response: str
    bot_response: str
    
    def __init__(self, discord_id: int, points_to_win: int, prompt: str):
        self.discord_id = discord_id
        self.points_to_win = points_to_win
        self.player_score = 0
        self.bot_score = 0
        self.prompt = prompt
        self.player_response = ""
        self.bot_response = ""
    
    def has_winner(self) -> bool:
        return max(self.player_score, self.bot_score) >= self.points_to_win