import time
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger("consoleExample")


def auto_add_timestamp(logger):
    def wrapper(func):
        def decorate(*args, **kw):
            start = time.time()
            logger.info("function: {} starting".format(func.__name__))
            func(*args, **kw)
            logger.info("function: {} end , time: {}".format(func.__name__, time.time()-start))
        return decorate
    return wrapper



@auto_add_timestamp(logger)
def MyAdd(x, y, logger):
    logger.info("{} + {} = {}".format(x, y, x+y))
    time.sleep(10)
    return x+y


if __name__ == '__main__':
    MyAdd(1, 11, logger)