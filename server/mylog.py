import logging

class MyLog:
    def getLogger(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logger = logging.getLogger('MyLog')
        logger.setLevel(logging.DEBUG)
        
        if len(logger.handlers) > 0:
            return logger
        
        ch = logging.StreamHandler()
        fh = logging.FileHandler(filename="MyLog.log")
        
        logger.addHandler(ch)
        logger.addHandler(fh)
        
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        
        return logger
        

        
    

