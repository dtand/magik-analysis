import numpy as np

class Volume:

    def VWAP(closes, highs, lows, volumes, period):
        vwaps = [np.nan] * period
        vprices = []
        vpsum = 0
        vsum = 0

        for i in range(0, len(closes)):
            real = (closes[i] + highs[i] + lows[i]) / 3
            real_v = real * volumes[i]
            vprices.append(real_v)
            vsum = vsum + volumes[i]
            vpsum = vpsum + vprices[i]

            if i >= period:
                vsum = vsum - volumes[i-period]
                vpsum = vpsum - vprices[i-period]
                vwap = vpsum / vsum
                vwaps.append(vwap)

        return np.array(vwaps)
