import argparse
import sys
from sys import exit
import os
import json
import logging
from Algorithms import Algorithms

json_template = """{
    "algorithm_comment": "Possible algorithms: FCFS, SJN, SRT, RR, PreemptivePriority, NonPreemptivePriority",
    "algorithm": "FCFS",
    "input_comment": "If the algorithm do not support Priority/time_quantum, it can be excluded",
    "input_comment_2": "In PreemptivePriority, low number ALWAYS means high priority",
    "input": 
    [ 
        ["Job", "Arrival Time", "CPU Cycle", "Priority", "time_quantum=4"],
        ["A"  , 0             , 5          , 1],
        ["B"  , 2             , 6          , 3],
        ["C"  , 4             , 2          , 3],
        ["D"  , 5             , 3          , 4],
        ["E"  , 7             , 4          , 5],
        ["F"  , 7             , 1          , 2]
    ]
}"""


def parse_arg():
    """
    Parse command args for this program

    Returns:
        [dict] - dictionary of received arguments
    """
    parser = argparse.ArgumentParser(description="To cheese OS Chapter 2 algortihm related questions\n\nHow to use:\n\t1. run `algo -g > input.json & input.json`\n\t2. Fill in the algorithm and inputs\n\t3. Save the file\n\t4. run `algo -i input.json`", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-g', '--generate-json', action='store_true',
                        help="Print a sample of JSON needed for this program")
    parser.add_argument(
        '-i', '--input', metavar='input_json_filepath', help="input JSON file for the program to process")
    parser.add_argument(
        '-a', '--algorithm', metavar='algorithm_name', help="Override the algorithm to use\nAvailable algorithm_name: FCFS, SJN, SRT, RR, PreemptivePriority, NonPreemptivePriority")
    args = vars(parser.parse_args())
    if not len(sys.argv) > 1:
        parser.print_help()
    return args


def process_user_input(user_input, override_algorithm=None):
    """
    Process + Validate json data user provided

    Parameters:
        `user_input`: dict - user provided input in dictonary format
        `override_algorithm`: str - (Optional) override the algorithm to use

    """

    job_data = user_input['input']
    if override_algorithm:
        user_input['algorithm'] = override_algorithm
    eval_str = "Algorithms" + "." + user_input['algorithm'] + "(job_data)"
    try:
        g_data, timing_data = eval(eval_str)
    except AttributeError as e:
        print(f"Unknown algorithm '{user_input['algorithm']}'")
        # print("Debug: " + eval_str)
        exit()
    except Exception as e:
        print(e)
        # logging.exception(e)
        exit()
    draw_gantt_chart(g_data)
    draw_timing_table(timing_data)


def draw_gantt_chart(data):
    """
    Prints gantt chart based on provided data

    Parameters:
        `data`: list - data needed to draw the gantt chart

        Example: `[ { "job": "A", "len": 2 }, { "job": "B", "len": 1 } ]`

        Validation: 
            "len" must > 0
            "job" must not be empty; whitespace is allowed
    """
    chart = "|"
    chart_numbers = "0"
    prev_sum = 0

    for idx, job in enumerate(data):
        job_name = job["job"]
        job_length = job["len"]
        prev_sum_str_len = len(str(prev_sum))
        prev_sum = prev_sum + job_length
        if len(job_name) == 0:
            raise Exception(f"Job #{idx+1} have empty name")
        if job_length <= 0:
            raise Exception(f"Job #{idx+1} have length 0")
        chart = chart + job_name + " " + \
            ''.join(['-' for _ in range(job_length)]) + "|"
        chart_numbers = chart_numbers + \
            ''.join([' ' for _ in range(len(job_name) + 1 + job_length + 1 - prev_sum_str_len)]
                    ) + str(prev_sum)

    print(chart)
    print(chart_numbers)


def draw_timing_table(timing_data):
    """
    Prints the table containing Turnaround time and Wait Time of each jobs

    Parameters:
        `timing_data`: list - data needed to draw the table

        Example: [ 

            {"Job": "A", "Arrival Time": 2, "CPU Cycle": 3, "Finish Time": 4, "Turnaround Time": 2, "Wait Time": 4},

            {"Job": "B", "Arrival Time": 5, "CPU Cycle": 3, "Finish Time": 12, "Turnaround Time": 9, "Wait Time": 4}

        ]`
    """
    text = 'Job | Arrival Time | CPU Cycle | Finish Time | Turn. Time | Wait Time\n'
    text = text + '=====================================================================\n'
    total_cpu = 0
    total_ft = 0
    total_tt = 0
    total_wt = 0
    for row in timing_data:
        text += '%3s | %12s | %9s | %11s | %10s | %9s\n' % (
            row["Job"],
            row["Arrival Time"],
            row["CPU Cycle"],
            row["Finish Time"],
            row["Turnaround Time"],
            row["Wait Time"],
        )
        total_cpu = total_cpu + row["CPU Cycle"]
        total_ft = total_ft + row["Finish Time"]
        total_tt = total_tt + row["Turnaround Time"]
        total_wt = total_wt + row["Wait Time"]

    text = text + "---------------------------------------------------------------------\n"
    text = text + 'Total:               %9d | %11d | %10d | %9d\n' % (
        total_cpu,
        total_ft,
        total_tt,
        total_wt,
    )
    text = text + 'Average:             %9f | %11f | %10f | %9f\n' % (
        total_cpu / len(timing_data),
        total_ft / len(timing_data),
        total_tt / len(timing_data),
        total_wt / len(timing_data),
    )
    text = text + '=====================================================================\n'
    print(text)


if __name__ == "__main__":
    args = parse_arg()
    # print(args)

    if args['generate_json']:
        print(json_template)
        # pog = json.loads(json_template)
        exit()

    if args['input']:
        args['input'] = args['input'].replace("\\", "/").strip()
        # print("Debug: " + args['input'])
        try:
            with open(args['input']) as f:
                user_input = json.load(f)
                if args['algorithm']:
                    process_user_input(user_input, args['algorithm'])    
                else:
                    process_user_input(user_input)
        except FileNotFoundError:
            print("Invalid input filepath")
        except json.decoder.JSONDecodeError as e:
            print("Invalid json file provided")
            print(e)
        exit()