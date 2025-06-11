from mage.src.Services.AnalysisEngine import AnalysisEngine
import numpy as np

class AnalysisSimulator:

    def perform(analysis_engine, rsi_threshold, result):
        rows = analysis_engine.results

        hit_x = []
        hit_y = []
        hit_z = []
        hit_v = []

        for row in rows:
            if 'HIT' in row:
                hit_x.append(row['DELTA_RSI'])
                hit_y.append(row['SBOTH.both'])
                hit_z.append(row['RSI'])
                hit_v.append(row['DELTA_OBV'])


        x = np.array(hit_x)
        y = np.array(hit_y)
        z = np.array(hit_z)
        v = np.array(hit_v)

        corr_rsi = np.corrcoef(z, y)[0, 1]
        corr_delta = np.corrcoef(x, y)[0, 1]
        corr_dobv = np.corrcoef(v, y)[0,1]

        #print("RSI + OTC: {}".format(corr_rsi))
        #print("RSI DELTA + OTC: {}".format(corr_delta))
        print("{},{},{},{},{},{}".format(rsi_threshold, corr_rsi, corr_delta, len(x), corr_dobv, result.probability))

