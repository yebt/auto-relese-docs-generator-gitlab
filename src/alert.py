class Alert:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ORANGE = "\033[38;5;166m"
    PURPLE = "\033[38;5;201m"

    @staticmethod
    def info(msg: str, additional: str = "", padding: int = 0):
        if additional:
            additional = f"{Alert.WARNING}{additional}{Alert.ENDC}"

        prefix = f"{Alert.OKBLUE}{Alert.BOLD}[{Alert.ENDC}{Alert.BOLD}>>{Alert.OKBLUE}{Alert.BOLD}] "
        if padding > 0:
            print(" " * padding, end="")
            prefix = f"{Alert.PURPLE}{Alert.BOLD}~~ "

        print(f"{prefix}{Alert.ENDC}{Alert.OKBLUE}{msg}{Alert.ENDC}  {additional}")

    @staticmethod
    def error(msg: str, additional: str = ""):
        if additional:
            additional = f"{Alert.WARNING}{additional}{Alert.ENDC}"

        print(
            f"{Alert.FAIL}{Alert.BOLD}[{Alert.ENDC}{Alert.BOLD}!!{Alert.FAIL}{Alert.BOLD}] {Alert.ENDC}{Alert.FAIL}{msg}{Alert.ENDC}  {additional}"
        )

    @staticmethod
    def success(msg: str, additional: str = ""):
        if additional:
            additional = f"{Alert.WARNING}{additional}{Alert.ENDC}"

        print(
            f"{Alert.OKGREEN}{Alert.BOLD}[{Alert.ENDC}{Alert.BOLD}√√{Alert.OKGREEN}{Alert.BOLD}] {Alert.ENDC}{Alert.OKGREEN}{msg}{Alert.ENDC}  {additional}"
        )

    @staticmethod
    def warning(msg: str, additional: str = ""):
        if additional:
            additional = f"{Alert.OKCYAN}{additional}{Alert.ENDC}"

        print(
            f"{Alert.WARNING}{Alert.BOLD}[{Alert.ENDC}{Alert.BOLD}??{Alert.WARNING}{Alert.BOLD}] {Alert.ENDC}{Alert.WARNING}{msg}{Alert.ENDC}  {additional}"
        )

    @staticmethod
    def header(msg: str):
        print()
        print(f"{Alert.HEADER}{Alert.BOLD}{Alert.UNDERLINE}{msg}{Alert.ENDC}")
        print()

    @staticmethod
    def print_header():
        header = [
            "",
        ]
        print("\n\t\033[38;5;166m".join(header))
        print("\033[0m")

