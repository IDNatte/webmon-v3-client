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
                    ).strip()
                    or "/var/log/webmon/webmon_client/"
                )

                file_log_path = str(
                    input(
                        'Where do you want to put config output (E.g. "/var/log/server") : '
                    ).strip()
                    or "/var/log/webmon/server"
                )

                file_log_prefix = str(
                    input(
                        "Do you have any file log name prefix (E.g. Current Hostname) ? : "
                    ).strip()
                    or "host"
                )

                url_reporter = str(
                    input(
                        'URL reporter endpoint (E.g. "https://reporter.host:5000/upload") : '
                    ).strip()
                    or "http://localhost:5000/upload"
                )

                url_reporter_token = str(
                    input(
                        'Token reporter (E.g. "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9") : '
                    ).strip()
                    or None
                )

                upload_retention = int(
                    input(
                        "Upload retention time, E.g 5 seconds (default 60 seconds) : "
                    ).strip()
                    or 60
                )

                print("[*]Creating folder config...")
                if not os.path.isdir(base_config_folder):
                    os.mkdir(base_config_folder)
                print("[!]Folder config created...\n")

                print("[*]Writting config to file")

                with open(
                    os.path.join(base_config_folder, "config.toml"), "w"
                ) as c_write:
                    config = {
                        "app": {"app_log_path": app_logger_path},
                        "log": {
                            "path": file_log_path,
                            "fileformat": "slg",
                            "filename_prefix_1": file_log_prefix,
                            "filename_prefix_2": "timestamp",
                        },
                        "reporter": {
                            "url_link": url_reporter,
                            "token": url_reporter_token,
                            "retention": upload_retention,
                        },
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
