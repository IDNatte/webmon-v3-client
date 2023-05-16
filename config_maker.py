import toml
import os


def config_maker_main():
    base_config_folder = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config"
    )

    if not os.path.isdir(base_config_folder) or not os.path.isfile(
        os.path.join(base_config_folder, "config.toml")
    ):
        while True:
            try:
                app_logger_path = str(
                    input(
                        'Where do you want to put Application logger ? (E.g. "/var/log/webmon_app") : '
                    )
                )

                file_log_path = str(
                    input(
                        'Where do you want to put config output (E.g. "/var/log/server") : '
                    )
                )

                file_log_prefix = str(
                    input(
                        "Do you have any file log name prefix (E.g. Current Hostname) ? : "
                    )
                )

                url_reporter = str(
                    input(
                        'URL reporter endpoint (E.g. "https://reporter.host:5000/upload") : '
                    )
                )

                url_reporter_token = str(
                    input(
                        'Token reporter (E.g. "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9") : '
                    )
                )

                if app_logger_path:
                    app_log_path = app_logger_path

                if file_log_prefix:
                    log_prefix_1 = file_log_prefix

                if file_log_path:
                    log_path = file_log_path

                if url_reporter:
                    log_reporter = url_reporter

                if url_reporter_token:
                    reporter_token = url_reporter_token

                if not app_logger_path:
                    app_log_path = "/var/log/webmon_client/"

                if not file_log_path:
                    log_path = "/var/log/"

                if not file_log_prefix:
                    log_prefix_1 = "host"

                if not url_reporter:
                    log_reporter = "http://localhost:5000/upload"

                if not url_reporter_token:
                    reporter_token = None

                print("[*]Creating folder config...")
                if not os.path.isdir(base_config_folder):
                    os.mkdir(base_config_folder)
                print("[!]Folder config created...\n")

                print("[*]Writting config to file")
                with open(
                    os.path.join(base_config_folder, "config.toml"), "w"
                ) as c_write:
                    config = {
                        "app": {"app_log_path": app_log_path},
                        "log": {
                            "path": log_path,
                            "fileformat": "slg",
                            "filename_prefix_1": log_prefix_1,
                            "filename_prefix_2": "timestamp",
                        },
                        "reporter": {"url_link": log_reporter, "token": reporter_token},
                    }

                    toml.dump(config, c_write)
                print("[!]Config created, running next procedure")

                break

            except KeyboardInterrupt:
                print("\nconfig creation canceled !")
                break
    else:
        print("\n[!] Config already exists, exitting...!\n")


if __name__ == "__main__":
    config_maker_main()
