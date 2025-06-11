class Logger:

    enabled = False
    
    def LOG(msg):
        if Logger.enabled:
            print(msg)