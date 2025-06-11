import csv
import numpy as np
from datetime import datetime, timezone
from mage.src.Services.CSVService import CSVService

'''
    Analysis Name: Time Boxed High Low Probabilities

    Description:
        This analysis looks at hourly ohlcv data one day at a time.  For a given
        day, defined as UTC hours 0-24, two time windows are defined.  These
        time windows are referred to as Session A and Session B, where the time
        prior to Sesson A is referred to as the pre-session.  If a new high or low
        is detected during Session A compared to the pre-session, then the analysis
        will look for the probability that Session B trades higher than Session A at
        any point in time for a given symbol.

    Parameters:
        time_box_a - array of two integers representing Session A hourly range, ie [6,12] (London session)
        time_box_b - array of two integers representing Session B hourly range, ie [12,20] (US session)

    Result:
'''


csv_service = CSVService()
DATA_SET = './Resources/downloads/glbx-mdp3-20100606-20250425.ohlcv-1h.csv'
DEFAULT_HIGH = -9999999999
DEFAULT_LOW = 9999999999

def parse_futures_data(file):
    print("Preparing data...")
    data = {}
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader, None)
        for row in csvreader:
            symbol = row[9]
            if '-' in symbol or ':' in symbol:
                continue
            if symbol not in data:
                data[symbol] = {
                    'open': np.array([]),
                    'low': np.array([]),
                    'high': np.array([]), 
                    'close': np.array([]), 
                    'volume': np.array([]),
                    'timestamp': np.array([])
                }
            if float(row[8]) < 10:
                continue
            data[symbol]['open'] = np.append(data[symbol]['open'], float(row[4]))
            data[symbol]['low'] = np.append(data[symbol]['low'], float(row[6]))
            data[symbol]['high'] = np.append(data[symbol]['high'], float(row[5]))
            data[symbol]['close']= np.append(data[symbol]['close'], float(row[7]))
            data[symbol]['volume'] = np.append(data[symbol]['volume'], float(row[8]))
            data[symbol]['timestamp'] = np.append(datetime.fromisoformat(data[symbol]['timestamp']), row[0])
    empty_symbols = []
    for symbol in data:
        if len(data[symbol]['timestamp']) < 24:
            empty_symbols.append(symbol)
    for symbol in empty_symbols:
        del data[symbol]
    return data 

def do_analysis(data, time_box_a, time_box_b, symbol):

    ## Values which are reset daily
    daily_hl = [DEFAULT_HIGH, DEFAULT_LOW]
    pre_session_hl = [DEFAULT_HIGH, DEFAULT_LOW]
    session_a_hl = [DEFAULT_HIGH, DEFAULT_LOW]
    session_b_hl = [DEFAULT_HIGH, DEFAULT_LOW]
    session_b_dd = [DEFAULT_HIGH, DEFAULT_HIGH]
    session_b_open = None
    drawdown_session_b = DEFAULT_HIGH
    drawup_session_b = DEFAULT_HIGH

    ## Trackable statistics
    session_a_highs = 0
    session_a_lows = 0
    session_b_highs = 0
    session_b_lows = 0
    drawdown_sum = 0
    drawup_sum = 0
    total_days = 0

    ts_start = data['timestamp'][0]
    ts_end = data['timestamp'][-1]

    csv_service.add_row(symbol, ['Day', 'Criteria Met', 'Daily High', 'Daily Low', 'Pre Session High', 'Pre Session Low','Session A High', 'Session A Low', 'Session B High', 'Session B Low', 'A-B High Change', 'A-B Low Change', 'Max DD B', 'Max DU B'])
    current_day = None
    current_hour = -1

    for i in range(0,len(data['timestamp'])):
        unix_time = data['timestamp'][i]
        high = data['high'][i]
        low = data['low'][i]
        hour = int(unix_time.hour)

        ## Rollover to next day and assess results from previous day
        ## reset all defaults
        if hour < current_hour or hour == 0:
            current_hour = hour
            if current_day != None:
                total_days = total_days + 1
                p_diff_h = 0
                p_diff_l = 0
                criteria_met_high = False
                criteria_met_low = False
                
                ## Session a made new high
                if session_a_hl[0] > pre_session_hl[0]:
                    session_a_highs = session_a_highs + 1
                    
                    ## Session b traded higher than session a
                    if session_b_hl[0] > session_a_hl[0]:
                        p_diff_h = percentage_difference(session_b_hl[0], session_a_hl[0])
                        session_b_highs = session_b_highs + 1
                        criteria_met_high = True

                ## Seession a made new low
                if session_a_hl[1] < pre_session_hl[1]:
                    session_a_lows = session_a_lows + 1
                    
                    ## Session b traded lower than session a
                    if session_b_hl[1] < session_a_hl[1]:
                        p_diff_l = percentage_difference(session_b_hl[1], session_a_hl[1])
                        session_b_lows = session_b_lows + 1
                        criteria_met_low = True
                
                criteria_met = "NONE"

                if criteria_met_high and criteria_met_low:
                    criteria_met = "HIGH,LOW"
                elif criteria_met_high:
                    criteria_met = "HIGH"
                elif criteria_met_low:
                    criteria_met_low = "LOW"
                
                drawdown_sum = drawdown_sum + session_b_dd[0]
                drawup_sum = drawup_sum + session_b_dd[1]
                csv_service.add_row(symbol, [current_day, str(criteria_met), daily_hl[0], daily_hl[1], pre_session_hl[0], pre_session_hl[1], session_a_hl[0], session_a_hl[1], session_b_hl[0], session_b_hl[1],  str(round(p_diff_h,2)) + "%", str(round(p_diff_l,2)) + "%", str(round(session_b_dd[0],2)) + "%", str(round(session_b_dd[1],2)) + "%"])
            
            daily_hl = [DEFAULT_HIGH, DEFAULT_LOW]
            pre_session_hl = [DEFAULT_HIGH, DEFAULT_LOW]
            session_a_hl = [DEFAULT_HIGH, DEFAULT_LOW]
            session_b_hl = [DEFAULT_HIGH, DEFAULT_LOW]
            session_b_dd = [DEFAULT_HIGH, DEFAULT_HIGH]
            session_b_open = None
            drawdown_session_b = DEFAULT_HIGH
            drawup_session_b = DEFAULT_HIGH
            current_day = str(unix_time.year) + '-' + str(unix_time.month) + '-' + str(unix_time.day)

        ## Data started mid day, don't count this sample
        if current_day == None:
            continue

        ## Always get max and min over entire day
        daily_hl[0] = max(daily_hl[0], high)
        daily_hl[1] = min(daily_hl[1], low)

        ## Pre Session Trading
        if hour < time_box_a[0]:
            pre_session_hl[0] = max(pre_session_hl[0], high)
            pre_session_hl[1] = min(pre_session_hl[1], low)

        if hour == time_box_b[0]:
            session_b_open = data['open'][i]

        ## Session A Trading
        elif hour >= time_box_a[0] and hour <= time_box_a[1]:
            session_a_hl[0] = max(session_a_hl[0], high)
            session_a_hl[1] = min(session_a_hl[1], low)

        ## Session B Trading
        elif hour >= time_box_b[0] and hour <= time_box_b[1]:   

            if session_b_open == None:
                session_b_open = data['open'][i]

            # Update current drawdowns for period based on period open
            drawdown_session_b = max(drawdown_session_b, percentage_difference(low, session_b_open))
            drawup_session_b = max(drawup_session_b, percentage_difference(high, session_b_open))

            # A new high will be observed - capture drawdown up to this point
            if high > session_b_hl[0]:
                session_b_dd[0] = drawdown_session_b

            # A new low will be observed - capture the drawup to this point
            if low < session_b_hl[1]:
                session_b_dd[1] = drawup_session_b           

            session_b_hl[0] = max(session_b_hl[0], high)
            session_b_hl[1] = min(session_b_hl[1], low)

    probability_highs = 0
    probability_lows = 0

    if session_a_highs != 0:
        probability_highs = (float(session_b_highs) / float(session_a_highs))
    if session_a_lows != 0:
        probability_lows = (float(session_b_lows) / float(session_a_lows))

    avg_dd = drawdown_sum / float(total_days)
    avg_du  = drawup_sum / float(total_days)

    csv_service.add_row('Results', [symbol, ts_start, ts_end, total_days, session_a_highs, session_b_highs,  str(round(probability_highs,2)) + "%", session_a_lows, session_b_lows,  str(round(probability_lows,2)) + "%",  str(round(avg_dd,2)) + "%",  str(round(avg_du,2)) + "%"])


def percentage_difference(num1, num2):
    try:
        return abs(num1 - num2) / ((num1 + num2) / 2) * 100
    except ZeroDivisionError:
        return "Cannot calculate percentage difference when the average is zero."
    
def has_complete_day(i, data):
    for x in range(0,24):
        if x+i >= len(data['timestamp']):
            return False
        ts = data['timestamp'][x+i]
        if ts.hour != x:
            return False
    return True

    
def run(data):
    csv_service.add_page("Results")
    csv_service.add_row('Results', ['Symbol', 'Start Time', 'End Time', 'Total Days', 'Session A Total Highs', 'Session B Total Highs', 'Probability of B High', 'Session A Total Lows', 'Session B Total Lows', 'Probability of B Low', 'Avg DD', 'Avg DU'])
    for symbol in data:
        print("Analyzing symbol: {}".format(symbol))
        csv_service.add_page(symbol)
        do_analysis(data[symbol], [6,11], [12,20], symbol)
    csv_service.write_to_folder('./results')
    csv_service.to_workbook('./results', './results/RESULTS.xlsx')