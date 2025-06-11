import numpy as np
from mage.src.Utils.math_utils import percentage_difference
DEFAULT_HIGH = -9999999999
DEFAULT_LOW = 9999999999

class SessionBased:

    def SBH(highs, timestamps, pre_session, session_a, session_b):
        
        first_day_start = SessionBased.find_first_day_start(timestamps)
        pre_high = DEFAULT_HIGH
        a_high = DEFAULT_HIGH
        b_high = DEFAULT_HIGH
        psh = [np.nan] * first_day_start 
        sah = [np.nan] * first_day_start
        sbh = [np.nan] * first_day_start
        
        for i in range(first_day_start, len(highs)):
            high = highs[i]
            hour = timestamps[i].hour

            if hour < pre_session[0]:
                psh.append(np.nan)
                sah.append(np.nan)
                sbh.append(np.nan)
            elif hour >= pre_session[0] and hour <= pre_session[1]:
                pre_high = max(pre_high, high)
                psh.append(pre_high)
                sah.append(np.nan)
                sbh.append(np.nan)
            elif hour >= session_a[0] and hour <= session_a[1]:
                a_high = max(a_high, high)
                psh.append(psh[-1])
                sah.append(a_high)
                sbh.append(np.nan)
            elif hour >= session_b[0] and hour <= session_b[1]:
                b_high = max(b_high, high)
                psh.append(psh[-1])
                sah.append(sah[-1])
                sbh.append(b_high)
            else:
                psh.append(psh[-1])
                sah.append(sah[-1])
                sbh.append(sbh[-1])
                pre_high = DEFAULT_HIGH
                a_high = DEFAULT_HIGH
                b_high = DEFAULT_HIGH
                
        return psh, sah, sbh
    
    def SBL(lows, timestamps, pre_session, session_a, session_b):
        
        first_day_start = SessionBased.find_first_day_start(timestamps)
        pre_low = DEFAULT_LOW
        a_low = DEFAULT_LOW
        b_low = DEFAULT_LOW
        psl = [np.nan] * first_day_start 
        sal = [np.nan] * first_day_start
        sbl = [np.nan] * first_day_start
        
        for i in range(first_day_start, len(lows)):
            low = lows[i]
            hour = timestamps[i].hour

            if hour < pre_session[0]:
                psl.append(np.nan)
                sal.append(np.nan)
                sbl.append(np.nan)
            elif hour >= pre_session[0] and hour <= pre_session[1]:
                pre_low = min(pre_low, low)
                psl.append(pre_low)
                sal.append(np.nan)
                sbl.append(np.nan)
            elif hour >= session_a[0] and hour <= session_a[1]:
                a_low = min(a_low, low)
                psl.append(psl[-1])
                sal.append(a_low)
                sbl.append(np.nan)
            elif hour >= session_b[0] and hour <= session_b[1]:
                b_low = min(b_low, low)
                psl.append(psl[-1])
                sal.append(sal[-1])
                sbl.append(b_low)
            else:
                psl.append(psl[-1])
                sal.append(sal[-1])
                sbl.append(sbl[-1])
                pre_low = DEFAULT_LOW
                a_low = DEFAULT_LOW
                b_low = DEFAULT_LOW

        return psl, sal, sbl
    
    def SBOTC(opens, closes, timestamps, pre_session, session_a, session_b):
         
        first_day_start = SessionBased.find_first_day_start(timestamps)
        popen = None
        aopen = None
        bopen = None
        psotc = [np.nan] * first_day_start 
        aotc = [np.nan] * first_day_start
        botc = [np.nan] * first_day_start
        
        for i in range(first_day_start, len(opens)):
            curr_open = opens[i]
            curr_close = closes[i]
            hour = timestamps[i].hour

            if hour < pre_session[0]:
                psotc.append(np.nan)
                aotc.append(np.nan)
                botc.append(np.nan)
            elif hour >= pre_session[0] and hour <= pre_session[1]:
                if popen == None:
                    popen = curr_open
                change = percentage_difference(popen, curr_close)
                psotc.append(change)
                aotc.append(np.nan)
                botc.append(np.nan)
            elif hour >= session_a[0] and hour <= session_a[1]:
                if aopen == None:
                    aopen = curr_open
                change = percentage_difference(aopen, curr_close)
                psotc.append(psotc[-1])
                aotc.append(change)
                botc.append(np.nan)
            elif hour >= session_b[0] and hour <= session_b[1]:
                if bopen == None:
                    bopen = curr_open
                change = percentage_difference(bopen, curr_close)
                psotc.append(psotc[-1])
                aotc.append(aotc[-1])
                botc.append(change)
            else:
                psotc.append(psotc[-1])
                aotc.append(aotc[-1])
                botc.append(aotc[-1])
                popen = None
                aopen = None
                bopen = None

        return psotc, aotc, botc 

    def SBOTH(opens, s_highs, timestamps, pre_session, session_a, session_b):
         
        first_day_start = SessionBased.find_first_day_start(timestamps)
        popen = None
        aopen = None
        bopen = None
        psoth = [np.nan] * first_day_start 
        aoth = [np.nan] * first_day_start
        both = [np.nan] * first_day_start
        
        for i in range(first_day_start, len(opens)):
            curr_open = opens[i]
            curr_high_p = s_highs['psh'][i]
            curr_high_a = s_highs['ash'][i]
            curr_high_b = s_highs['bsh'][i]
            hour = timestamps[i].hour

            if hour < pre_session[0]:
                psoth.append(np.nan)
                aoth.append(np.nan)
                both.append(np.nan)
            elif hour >= pre_session[0] and hour <= pre_session[1]:
                if popen == None:
                    popen = curr_open
                change = percentage_difference(popen, curr_high_p)
                psoth.append(change)
                aoth.append(np.nan)
                both.append(np.nan)
            elif hour >= session_a[0] and hour <= session_a[1]:
                if aopen == None:
                    aopen = curr_open
                change = percentage_difference(aopen, curr_high_a)
                psoth.append(psoth[-1])
                aoth.append(change)
                both.append(np.nan)
            elif hour >= session_b[0] and hour <= session_b[1]:
                if bopen == None:
                    bopen = curr_open
                change = percentage_difference(bopen, curr_high_b)
                psoth.append(psoth[-1])
                aoth.append(aoth[-1])
                both.append(change)
            else:
                psoth.append(psoth[-1])
                aoth.append(aoth[-1])
                both.append(aoth[-1])
                popen = None
                aopen = None
                bopen = None

        return psoth, aoth, both   

    def SBOTL(opens, s_lows, timestamps, pre_session, session_a, session_b):
         
        first_day_start = SessionBased.find_first_day_start(timestamps)
        popen = None
        aopen = None
        bopen = None
        psotl = [np.nan] * first_day_start 
        aotl = [np.nan] * first_day_start
        botl = [np.nan] * first_day_start
        
        for i in range(first_day_start, len(opens)):
            curr_open = opens[i]
            curr_low_p = s_lows['psl'][i]
            curr_low_a = s_lows['asl'][i]
            curr_low_b = s_lows['bsl'][i]
            hour = timestamps[i].hour

            if hour < pre_session[0]:
                psotl.append(np.nan)
                aotl.append(np.nan)
                botl.append(np.nan)
            elif hour >= pre_session[0] and hour <= pre_session[1]:
                if popen == None:
                    popen = curr_open
                change = abs(percentage_difference(popen, curr_low_p))
                psotl.append(change)
                aotl.append(np.nan)
                botl.append(np.nan)
            elif hour >= session_a[0] and hour <= session_a[1]:
                if aopen == None:
                    aopen = curr_open
                change = abs(percentage_difference(aopen, curr_low_a))
                psotl.append(psotl[-1])
                aotl.append(change)
                botl.append(np.nan)
            elif hour >= session_b[0] and hour <= session_b[1]:
                if bopen == None:
                    bopen = curr_open
                change = abs(percentage_difference(bopen, curr_low_b))
                psotl.append(psotl[-1])
                aotl.append(aotl[-1])
                botl.append(change)
            else:
                psotl.append(psotl[-1])
                aotl.append(aotl[-1])
                botl.append(botl[-1])
                popen = None
                aopen = None
                bopen = None

        return psotl, aotl, botl   
    
    def SBMAXDD(opens, lows, timestamps, pre_session, session_a, session_b):
         
        first_day_start = SessionBased.find_first_day_start(timestamps)
        popen = None
        aopen = None
        bopen = None
        psotc = [np.nan] * first_day_start 
        aotc = [np.nan] * first_day_start
        botc = [np.nan] * first_day_start
        
        for i in range(first_day_start, len(opens)):
            curr_open = opens[i]
            curr_low = lows[i]
            hour = timestamps[i].hour

            if hour < pre_session[0]:
                psotc.append(np.nan)
                aotc.append(np.nan)
                botc.append(np.nan)
            elif hour >= pre_session[0] and hour <= pre_session[1]:
                if popen == None:
                    popen = curr_open
                change = percentage_difference(popen, curr_low)
                psotc.append(change)
                aotc.append(np.nan)
                botc.append(np.nan)
            elif hour >= session_a[0] and hour <= session_a[1]:
                if aopen == None:
                    aopen = curr_open
                change = percentage_difference(aopen, curr_low)
                psotc.append(psotc[-1])
                aotc.append(change)
                botc.append(np.nan)
            elif hour >= session_b[0] and hour <= session_b[1]:
                if bopen == None:
                    bopen = curr_open
                change = percentage_difference(bopen, curr_low)
                psotc.append(psotc[-1])
                aotc.append(aotc[-1])
                botc.append(change)
            else:
                psotc.append(psotc[-1])
                aotc.append(aotc[-1])
                botc.append(aotc[-1])
                popen = None
                aopen = None
                bopen = None

        return psotc, aotc, botc     
    
    def find_first_day_start(timestamps):
        i = 0
        last_hour = timestamps[0].hour
        for timestamp in timestamps:
            if timestamp.hour < last_hour:
                return i
            else:
                last_hour = timestamp.hour
                i = i + 1
        return i


            

