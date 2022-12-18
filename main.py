import os
import time
from argparse import ArgumentParser, Namespace
from datetime import timedelta, datetime

import telegram
from dotenv import load_dotenv

from layer3.layer3 import Layer3API


class TelegramBot(object):

    def __init__(self) -> None:
        self.bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN", "TELEGRAM_TOKEN"))

    def send_message(self, text: str, chat_id: str) -> None:
        self.bot.send_message(chat_id=chat_id, text=text)


def run_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--time-window", "-t", type=int, default=3, help="Time window to check on new quest. Unit in minute")
    return parser.parse_args()


def main(args: Namespace) -> None:
    time_window = args.time_window

    bot = TelegramBot()
    api = Layer3API()

    while True:
        curr_time = datetime.now()
        curr_time_str = curr_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        tasks = api.get_tasks()
        new_tasks = [
            _task for _task in tasks
            if curr_time - _task.created_at <= timedelta(minutes=time_window)]

        if len(new_tasks) < 1:
            print(f"[{curr_time_str}] No new task...")
        else:
            bot.send_message(f"New Tasks Arrived 🔥")
            for _task in new_tasks:
                bot.send_message(_task.to_string)
        time.sleep(time_window * 60)


if __name__ == "__main__":
    load_dotenv()
    args = run_parser()
    main(args)
