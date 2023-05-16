from prober.sys_prober import SystemProberThread
from uploader.uploader import UploaderThread

import datetime
import socket
import time
import toml
import sys
import os

import logging


def config_checker(fileconfig):
    checker = os.path.isfile(fileconfig)
    return checker


def job_run(log_out, config_base_path):
    config = os.path.join(config_base_path, "config")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M")

    with open(os.path.join(config, "config.toml"), "r") as settings:
        config_obj = toml.load(settings)

        if (
            config_obj.get("log").get("filename_prefix_1") == "host"
            and config_obj.get("log").get("filename_prefix_2") == "timestamp"
        ):
            filename_construct = f"{socket.gethostname()}_{timestamp}.{config_obj.get('log').get('fileformat')}"

        else:
            filename_construct = f"{config_obj.get('log').get('filename_prefix_1')}_{timestamp}.{config_obj.get('log').get('fileformat')}"

        token = config_obj.get("reporter").get("token")
        reporter_link = config_obj.get("reporter").get("url_link")
        filepath = os.path.abspath(config_obj.get("log").get("path"))
        filename = filename_construct

        log_out.info(f"running system prober and write to bin {filename}")

        sys_prober_thread = SystemProberThread(filepath, filename)
        sys_prober_thread.start()
        sys_prober_thread.stop()
        sys_prober_thread.join()

        log_out.info(f"running upload file {filename}")

        uploader_thread = UploaderThread(filepath, reporter_link, token)
        uploader_thread.start()
        uploader_thread.stop()
        uploader_thread.join()

        log_out.debug(uploader_thread.get_result())


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(base_path, "config")
    config_file = os.path.join(config, "config.toml")
    check = config_checker(config_file)

    try:
        logger = logging.getLogger(__file__)
        logger.setLevel(logging.DEBUG)

        with open(config_file, "r") as logger_config:
            app_logger = toml.load(logger_config)

            logger_path = os.path.abspath(app_logger.get("app").get("app_log_path"))

            if not os.path.isdir(logger_path):
                os.mkdir(logger_path)

        file_logger = logging.FileHandler(os.path.join(logger_path, "app_logger.log"))
        file_logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(name)s] [%(asctime)s] %(levelname)s : %(message)s"
        )
        file_logger.setFormatter(formatter)

        logger.addHandler(file_logger)

        logger.info("Running Application")

        while True:
            try:
                if check:
                    try:
                        time.sleep(60)
                        job_run(logger, base_path)

                    except KeyboardInterrupt:
                        logger.info("Closing application")
                        sys.exit()

                    except Exception as error:
                        logger.error(error)
                        sys.exit()
                else:
                    logger.warning("Please run config_maker first...")
                    break

            except Exception as err:
                logger.error(err)
                break

    except FileNotFoundError:
        print("\n[!] Please run config_maker first...!!\n")


if __name__ == "__main__":
    main()
