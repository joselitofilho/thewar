import logging

if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('Started')
    logging.info('Finished')

    try:
        a = 1 / 0
    except Exception:
        logging.exception("IEI")
