class TradingReport:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.headers = ['Timestamp', 'Symbol', 'Action', 'Open/Close/Add', 'Cost basis', 'Quantity', 'PnL']
        self.rows = []
        self.pnl = 0
        self.wins = 0
        self.losses = 0
        self.win_streak = 0
        self.lose_streak = 0
        self.max_win_streak = 0
        self.max_lose_streak = 0
        self.max_win = -1
        self.max_loss = 0
        self.win_pnl = 0
        self.loss_pnl = 0
        self.buys = 0
        self.sells = 0

    def update_info(self, pnl):
        if pnl > 0:
            self.wins = self.wins + 1
            self.win_pnl = self.win_pnl + pnl
            self.win_streak = self.win_streak + 1
            self.max_win_streak = max(self.win_streak, self.max_win_streak)
            self.max_win = max(pnl, self.max_win)
            self.lose_streak = 0
        else:
            self.losses = self.losses + 1
            self.loss_pnl = self.loss_pnl + pnl
            self.lose_streak = self.lose_streak + 1
            self.max_lose_streak = max(self.lose_streak, self.max_lose_streak)
            self.max_loss = min(pnl, self.max_loss)
            self.win_streak = 0

        self.pnl = self.pnl + pnl

    def add_row(self, info):
        self.rows.append(info)

    def set_time_period(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def avg_win_loss(self):
        return round(self.win_pnl / self.wins,2), round(self.loss_pnl / self.losses, 2)
    
    def output_report(self):
        avg_win, avg_loss = self.avg_win_loss()
        print("========== Trading Report ==========")
        print("Period: {} - {}".format(self.start_time, self.end_time))
        print("Pnl: {}".format(self.pnl))
        print("Avg Win: {}".format(avg_win))
        print("Avg Loss: {}".format(avg_loss))
        print("Win / Loss: {}".format(round(self.wins/self.losses, 2)))
        print("Avg Win / Avg Loss: {}".format(round(avg_win/avg_loss, 2)))
        print("Max Win: {}".format(self.max_win))
        print("Max Loss: {}".format(self.max_loss))
        print("Max Win Streak: {}".format(self.max_win_streak))
        print("Max Lose Streak: {}".format(self.max_lose_streak))


