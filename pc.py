#!/usr/bin/env python3
"""
pc - script to calculate pyramid cound stats
"""
import argparse
from datetime import datetime, timedelta
from os.path import exists


BANK_FILE = "bank.txt"


def read_bank_file():
    """
    read cached values from bank file
    """
    if exists(BANK_FILE):
        with open(BANK_FILE, 'r', encoding="UTF-8") as filehandle:
            bank = int(filehandle.readline())
            print(bank)
            rest_days_used = int(filehandle.readline())
            print(rest_days_used)
            start_day_str = filehandle.readline()
            if start_day_str:
                start_day = datetime.strptime(start_day_str, "%d/%m/%Y")
            else:
                start_day = None
            return bank, rest_days_used, start_day
    return 0, 0, None


def write_bank_file(bank, rest_days_used, start_day):
    """
    cache bank values to file
    """
    with open(BANK_FILE, 'w', encoding="UTF-8") as filehandle:
        filehandle.write('\n'.join((
            str(bank),
            str(rest_days_used),
            start_day.strftime('%d/%m/%Y')
        )))


def calc_days(start_day):
    """
    calculate days
    """
    now = datetime.now()
    delta = now - start_day
    return delta.days+1


def calc_rest_days(start_day):
    """
    calculate rest days
    """
    rest_days = 0
    day = start_day
    one_day = timedelta(days=1)
    now = datetime.now()
    while day <= now:
        if day.weekday() == 6:
            rest_days = rest_days+1
        day += one_day
    return rest_days


def main():
    """
    main
    """
    parser = argparse.ArgumentParser(description='PC stats', add_help=True)
    parser.add_argument(
        '--start_day',
        help='set the start day of this cycle (DD/MM/YYYY)'
    )
    parser.add_argument(
        '--bank',
        type=int,
        help='set the count in the bank (INT)'
    )
    parser.add_argument(
        '--count',
        type=int,
        help='set the count for today (INT)',
    )
    parser.add_argument(
        '--rest_day',
        action='store_true',
        help='resigster today as a rest day'
    )
    args = parser.parse_args()
    bank, rest_days_used, start_day = read_bank_file()
    if args.start_day:
        start_day = datetime.strptime(args.start_day, "%d/%m/%Y")
    assert start_day, "start day set"

    days = calc_days(start_day)
    rest_days = calc_rest_days(start_day)
    todo = days * 5
    count = args.count or 0
    credit = count - todo

    if args.bank is not None:
        bank = args.bank
    if args.rest_day:
        rest_days_used = rest_days_used + 1
    elif not args.start_day:
        bank = bank + credit
    rest_days_delta = rest_days - rest_days_used
    print(
        f'start_day={start_day},\
todo={todo},days={days},\
rest_days_delta={rest_days_delta},\
count={count},\
bank={bank}',
    )
    print('/'.join((str(todo), str(rest_days_delta), str(bank))))
    write_bank_file(bank, rest_days_used, start_day)


if __name__ == "__main__":
    main()
