import argparse
import multiprocessing
import logging
import os
import sys

from web_service import run
from mailer import mailer_service


logger = logging.getLogger(__name__)

def get_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--port', nargs='?', default=9999, type=int,
        help="port for http server to bind to"
    )
    parser.add_argument(
        '-qd', '--queue-delay', nargs='?', default=3, type=int,
        help="Delay between picking up queued mail items"
    )
    parser.add_argument(
        '-ld', '--logs-directory', nargs='?', type=str,
        help="Custom Logs Directory that should be passed to write the logs to that location "
    )
    parser.add_argument(
        '-fc', '--file-conf', nargs='?', type=str,
        help="File Configurations containing mailing service parameters. Takes precedence over environment variables."
    )
    return parser.parse_args()

if __name__ == '__main__':

    args = get_arguments()

    logger.setLevel(logging.INFO)

    if not args.logs_directory:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    else:
        log_path = os.path.join(args.logs_directory, "master.log")
        logger.addHandler(logging.FileHandler(log_path))

    q = multiprocessing.Queue()

    web_service = multiprocessing.Process(
        target=run, args=(q, args.port, args.logs_directory)
    )
    web_service.start()
    logger.info("Starting web service")

    mailer_p = multiprocessing.Process(
        target=mailer_service, args=(q, args.queue_delay, args.logs_directory, args.file_conf)
    )
    mailer_p.start()
    logger.info("Starting mailer service")
