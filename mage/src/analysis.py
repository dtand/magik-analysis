from mage.src.Services.AnalysisJsonParser import AnalysisJsonParser
from mage.src.Services.AnalysisEngine import AnalysisEngine
from mage.src.Analysis.AnalysisSimulator import AnalysisSimulator
from Analysis import Analysis
from mage.src.Services.DataPrepService import DataPrepService
from datetime import datetime, timezone

ANALYSIS_FILE = "Test.json"

def main():
    #symbols = ['BTC.FUT', , , ]
    #symbols = ['6A.FUT', '6B.FUT', '6C.FUT', '6E.FUT', '6J.FUT', '6M.FUT', '6N.FUT', '6S.FUT']
    #symbols = ['ES.FUT']
    #symbols = []
    symbols_equities    = ['ES.FUT','NQ.FUT', 'RTY.FUT']
    #symbols_currency    = ['6A.FUT', '6B.FUT', '6C.FUT', '6E.FUT', '6J.FUT', '6M.FUT', '6N.FUT', '6S.FUT']
    symbols_currency    = ['6B.FUT']
    symbols_metals      = ['GC.FUT', 'HG.FUT', 'PA.FUT', 'SI.FUT']
    symbols_energy      = ['NG.FUT', 'MCL.FUT']
    symbols_treasuries  = ['ZB.FUT', 'TN.FUT']
    symbols_crypto      = ['BTC.FUT']
    #print(ANALYSIS_FILE)
    #print("\n")
    #analyze(symbols_equities, 'CME Equities Futures')
    #analyze(symbols_currency, 'CME Currency Futures')
    #analyze(symbols_metals, 'CME Metals Futures')
    #analyze(symbols_energy, 'CME Energy Futures')
    #analyze(symbols_treasuries, 'CME Treasuries Futures')
    analyze(symbols_crypto, 'CME Crypto Futures')
    #multi_symbols()
    #analysis = AnalysisJsonParser.do_parse(ANALYSIS_FILE, ['BTC.FUT'])
    #rsi_analysis(analysis, ['BTC.FUT'])

def rsi_analysis(analysis, symbols):
        print("RSI, CORR(RSI, OTC), CORR(DELTA_RSI, OTC), SAMPLE SIZE, PROBABILITY")
        for rsi in range(45, 81, 5):
            analysis.analysis_specification.criteria.and_ops[0].var2.var = rsi
            analysis_engine = AnalysisEngine()
            analysis_engine.prepare(analysis, symbols)
            result = analysis_engine.execute()
            #AnalysisSimulator.perform(analysis_engine, rsi, result)
            print("{},{},{},{}".format(result.count_assessed, result.count_predict, result.probability, rsi))

def analyze(symbols, category):
    print("===== Category: {} =====".format(category))
    for symbol in symbols:
        analysis = AnalysisJsonParser.do_parse(ANALYSIS_FILE, [symbol])
        analysis_engine = AnalysisEngine()
        analysis_engine.prepare(analysis, [symbol])
        result = analysis_engine.execute()
        print("{}: {},{},{}".format(symbol, result.count_assessed, result.count_predict, result.probability))
    print("\n")

def multi_symbols():
    print("===== Category: CME FOREX -> CME US Equities  =====")
    symbols_equities    = ['RTY.FUT']
    symbols_currency    = ['6E.FUT']
    for e in symbols_equities:
        for c in symbols_currency:
            symbols = [c, e]
            analysis = AnalysisEngine()
            analysis.prepare(ANALYSIS_FILE, symbols)
            count_criteria, count_predict, probability = analysis.execute()
            print("{}, {}: {}/{} = {}".format(symbols[0], symbols[1], count_predict, count_criteria, probability))

if __name__ == '__main__':
    main()