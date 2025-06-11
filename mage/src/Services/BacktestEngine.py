from mage.src.Services.TradingReport import TradingReport
from mage.src.Services.DataPrepService import DataPrepService
from mage.src.Services.LogicEngine import LogicEngine
from mage.src.Services.DTO.OpenPosition import OpenPosition
from mage.src.Services.VariableTable import VariableTable
from mage.src.Services.ActionManager import ActionManager
from mage.src.Strategies.DTO.Variable import Variable
from mage.src.Services.CSVService import CSVService
from mage.src.Services.Logger import Logger
from mage.src.Services.OrderBook import OrderBook
from mage.src.Services.Portfolio import Portfolio
from mage.src.Services.TestingDetails import TestingDetails
from mage.src.Utils import data_utils

class BacktestEngine:

    def __init__(self, capital=100000):
        
        ## Required objects
        self.portfolio = Portfolio()
        self.order_book = OrderBook()
        self.trading_report = TradingReport()
        self.testing_details = TestingDetails()
        self.variable_table = None
        
        ## Primitive members
        self.strategy = None
        self.data = None
        self.symbols = []
        self.capital = float(capital)
        self.curr_epoch = 0
        self.last_buy = 0
        self.buys = 0
        self.sells = 0
        self.winners = []
        self.losers = []
        self.pnl = 0

    def init(self, symbols, strategy, data):
        self.strategy = strategy
        self.data = data
        self.symbols = symbols
        self.variable_table = VariableTable.for_backtest(self, symbols)
        self.variable_table.globals['portfolio'] = self.portfolio
        self.trading_report.set_time_period(self.data[symbols[0]]['timestamp'][0], self.data[symbols[0]]['timestamp'][-1])
        self.testing_details.set_headers(data_utils.key_value_pairs_for_epoch(self.data[symbols[0]], self.curr_epoch).keys())

    def execute(self):
        core_symbol = self.strategy.data_specifications[0].symbol
        total_epochs = len(self.data[core_symbol]['open'])
        for i in range(0, total_epochs):
            self.curr_epoch = i
            self.epoch()
        return self.trading_report
    
    def epoch(self):
        self.update_variables()     ## Updates variable table with current state
        self.handle_signals()       ## Checks to see if any signals are triggered
        self.handle_orders()        ## Checks to see if any orders should be executed
        self.handle_actions()       ## Performs any actions if criteria is met
        self.update_testing_info()  ## Adds a row to the details testing info CSV report

    def update_variables(self):
        self.variable_table.epoch = self.curr_epoch
        ts = self.data[self.symbols[0]]['timestamp'][self.curr_epoch]
        self.portfolio.update(self.variable_table)
        # for key,value in self.portfolio.open_positions.items():
        #     Logger.LOG("{} -- OPEN POSITION - SYMBOL: {}, QUANTITY: {}, POSITION: {}, PNL: {}%".format(ts, key, value.quantity, value.position, round(value.open_pnl*100, 2)))

    def handle_signals(self):
        ts = self.data[self.symbols[0]]['timestamp'][self.curr_epoch]
        for signal in self.strategy.signals:
            result = LogicEngine.assess_statement(signal.criteria, self.variable_table)
            if result:
                if not self.variable_table.get(Variable(None, signal.identifier, 0)):
                    Logger.LOG("{} -- SIGNAL ACTIVE {}".format(ts, signal.identifier))
                    self.variable_table.set_global(signal.identifier, True)

    def handle_orders(self):
        ts = self.data[self.symbols[0]]['timestamp'][self.curr_epoch]
        action_results = self.order_book.check_orders(self.variable_table, self.portfolio)

        for result in action_results:
            action_result = result[0]
            order = result[1]

            if action_result.result == 'POSITION_CLOSED':   
                self.trading_report.add_row([ts, order.symbol, order.order_type, 'Close', action_result.cost_basis, action_result.size, action_result])
            
            elif action_result.result == 'POSITION_OPENED':
                self.trading_report.add_row([ts, order.symbol, order.order_type, 'Open', action_result.cost_basis, action_result.size, action_result.pnl])

            elif action_result.result == 'POSITION_ADD':
                self.trading_report.add_row([ts, order.symbol, order.order_type, 'Add', action_result.cost_basis, action_result.size, action_result.pnl])


    def handle_actions(self):
        actions_to_perform = self.assess_actions()
        ts = self.data[self.symbols[0]]['timestamp'][self.curr_epoch]

        for action in actions_to_perform:
            action_result = ActionManager.perform_action(action, self)

            if action_result.result == 'POSITION_CLOSED':   
                self.trading_report.add_row([ts, action.symbol, action.action.do, 'Close', action_result.cost_basis, action_result.size, action_result.pnl])
                self.trading_report.update_info(action_result.pnl)

            elif action_result.result == 'POSITION_OPENED':
                self.trading_report.add_row([ts, action.symbol, action.action.do, 'Open', action_result.cost_basis, action_result.size, action_result.pnl])

            elif action_result.result == 'POSITION_ADD':
                self.trading_report.add_row([ts, action.symbol, action.action.do, 'Add', action_result.cost_basis, action_result.size, action_result.pnl])

    def update_testing_info(self):
        key_values_for_epoch = data_utils.key_value_pairs_for_epoch(self.data[self.symbols[0]], self.curr_epoch)
        row = []
        for key, value in key_values_for_epoch.items():
            row.append(value)
        self.testing_details.add_row(row)

    def assess_actions(self):
        actions_to_perform = []
        for action_with_criteria in self.strategy.actions:
            result = LogicEngine.assess_statement(action_with_criteria.criteria, self.variable_table)
            if result:
                actions_to_perform.append(action_with_criteria)
                for follow_up in action_with_criteria.follow_up_actions:
                    actions_to_perform.append(follow_up)
        return actions_to_perform

    def write_report(self):
        csv_service = CSVService.from_report(self.trading_report, self.strategy.name + ' - Trades')
        csv_service.add_page_with_rows(self.strategy.name + ' - Data Log', self.testing_details.headers, self.testing_details.rows)
        win_loss = round(self.trading_report.wins / self.trading_report.losses, 2)
        avg_win, avg_loss = self.trading_report.avg_win_loss()
        pnl = self.trading_report.pnl
        rows = [
            ['PnL', pnl],
            ['Win / Loss', win_loss], 
            ['Avg Win', avg_win], 
            ['Avg Loss', avg_loss],
            ['Max Win', self.trading_report.max_win],
            ['Max Loss', self.trading_report.max_loss],
            ['Longest Win Streak', self.trading_report.max_win_streak],
            ['Longest Lose Streak', self.trading_report.max_lose_streak] 
        ]
        csv_service.add_page_with_rows(self.strategy.name + ' - Performance', [], rows)
        csv_service.write_to_folder('./Strategies/results')
        csv_service.to_workbook('./Strategies/results', './Strategies/results/{}.xlsx'.format(self.strategy.name))


