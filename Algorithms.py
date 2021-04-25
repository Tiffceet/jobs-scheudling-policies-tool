
import re
import copy


class Algorithms:
    # samples
    g_data = [{"job": "A", "len": 2}, {"job": "B", "len": 1}]
    t_data = [

        {"Job": "A", "Arrival Time": 2, "CPU Cycle": 3,
         "Finish Time": 4, "Turnaround Time": 2, "Wait Time": 4},

        {"Job": "B", "Arrival Time": 5, "CPU Cycle": 3,
         "Finish Time": 12, "Turnaround Time": 9, "Wait Time": 4}

    ]

    @staticmethod
    def make_t_data_from_g_data(raw_job_data, g_data):
        t_data = []
        for job in raw_job_data:
            insert_obj = {
                "Job": job[0],
                "Arrival Time": job[1],
                "CPU Cycle": job[2],
                "Finish Time": -1,
                "Turnaround Time": -1,
                "Wait Time": -1}
            for g_idx in range(len(g_data)-1, -1, -1):
                if g_data[g_idx]["job"] == insert_obj["Job"]:
                    insert_obj["Finish Time"] = sum(
                        [int(g_data_inner['len']) for g_data_inner in g_data[0:g_idx+1]])
                    break
            insert_obj["Turnaround Time"] = insert_obj["Finish Time"] - \
                insert_obj["Arrival Time"]
            insert_obj["Wait Time"] = insert_obj["Finish Time"] - \
                insert_obj["Arrival Time"] - insert_obj["CPU Cycle"]
            t_data.append(insert_obj)
        return t_data

    @staticmethod
    def FCFS(job_data):
        """
        FCFS Simulation

        Parameters:
            `job_data`: list - "input" of user provided json
        """
        raw_job_data = copy.deepcopy(job_data[1:])
        job_data = job_data[1:]
        queue = []
        g_data = []
        t_data = []
        time_now = 0
        selected_queue_idx = 0
        running_job = "-"
        # First come first serve
        while True:
            # If job arivval time reached, insert into queue
            for idx, job in enumerate(job_data):
                if job[1] == time_now:
                    queue.append(job)

            # Queue selection method
            # FCFS, always select 1st in queue
            selected_queue_idx = 0

            # if last running job doesnt match, append
            if running_job != queue[selected_queue_idx][0]:
                running_job = queue[selected_queue_idx][0]
                g_data.append({"job": queue[selected_queue_idx][0], "len": 0})

            # queue cpu cycle -1
            queue[selected_queue_idx][2] = queue[selected_queue_idx][2] - 1

            # CPU cycle -1 then gant chart +1
            g_data[-1]['len'] = g_data[-1]['len'] + 1
            time_now = time_now + 1

            # If cpu cycle reached 0, remove from queue
            for idx, queue_item in enumerate(queue):
                if queue_item[2] <= 0:
                    del queue[idx]
            if len(queue) == 0:
                break

        # Construct t_data from g_data
        t_data = Algorithms.make_t_data_from_g_data(raw_job_data, g_data)

        return g_data, t_data

    @staticmethod
    def SJN(job_data):
        """
        SJN Simulation

        Parameters:
            `job_data`: list - "input" of user provided json
        """
        raw_job_data = copy.deepcopy(job_data[1:])
        job_data = job_data[1:]
        queue = []
        g_data = []
        t_data = []
        time_now = 0
        dont_interrupt = False
        selected_queue_idx = 0
        running_job = '-'
        # Shortest Job Next
        while True:
            # If job arivval time reached, insert into queue
            for idx, job in enumerate(job_data):
                if job[1] == time_now:
                    queue.append(job)

            # Queue selection method
            # SJN, select the shortest cpu cycle in queue
            if not dont_interrupt:
                selected_queue_idx = 0
                lowest_cpu_cycle_idx = -1
                lowest_cpu_cycle = 999999
                for queue_idx in range(len(queue)):
                    if queue[queue_idx][2] < lowest_cpu_cycle:
                        lowest_cpu_cycle_idx, lowest_cpu_cycle = queue_idx, queue[queue_idx][2]
                selected_queue_idx = lowest_cpu_cycle_idx
                dont_interrupt = True

            # if last running job doesnt match, append
            if running_job != queue[selected_queue_idx][0]:
                running_job = queue[selected_queue_idx][0]
                g_data.append({"job": queue[selected_queue_idx][0], "len": 0})

            # queue cpu cycle -1
            queue[selected_queue_idx][2] = queue[selected_queue_idx][2] - 1

            # If this cycle is the last cycle then allow interrupt
            if queue[selected_queue_idx][2] <= 0:
                dont_interrupt = False

            # CPU cycle -1 then gant chart +1
            g_data[-1]['len'] = g_data[-1]['len'] + 1
            time_now = time_now + 1

            # If cpu cycle reached 0, remove from queue
            for idx, queue_item in enumerate(queue):
                if queue_item[2] <= 0:
                    del queue[idx]
            if len(queue) == 0:
                break

        # Construct t_data from g_data
        t_data = Algorithms.make_t_data_from_g_data(raw_job_data, g_data)

        return g_data, t_data

    @staticmethod
    def SRT(job_data):
        """
        SRT Simulation

        Parameters:
            `job_data`: list - "input" of user provided json
        """
        raw_job_data = copy.deepcopy(job_data[1:])
        job_data = job_data[1:]
        queue = []
        g_data = []
        t_data = []
        time_now = 0
        selected_queue_idx = 0
        running_job = '-'

        # Shortest Job Next
        while True:
            # If job arivval time reached, insert into queue
            for idx, job in enumerate(job_data):
                if job[1] == time_now:
                    queue.append(job)

            # Queue selection method
            # SJN, select the shortest cpu cycle in queue
            selected_queue_idx = 0
            lowest_cpu_cycle_idx = -1
            lowest_cpu_cycle = 999999
            for queue_idx in range(len(queue)):
                if queue[queue_idx][2] < lowest_cpu_cycle:
                    lowest_cpu_cycle_idx, lowest_cpu_cycle = queue_idx, queue[queue_idx][2]
            selected_queue_idx = lowest_cpu_cycle_idx

            # if last running job doesnt match, append
            if running_job != queue[selected_queue_idx][0]:
                running_job = queue[selected_queue_idx][0]
                g_data.append({"job": queue[selected_queue_idx][0], "len": 0})

            # queue cpu cycle -1
            queue[selected_queue_idx][2] = queue[selected_queue_idx][2] - 1

            # CPU cycle -1 then gant chart +1
            g_data[-1]['len'] = g_data[-1]['len'] + 1
            time_now = time_now + 1

            # If cpu cycle reached 0, remove from queue
            for idx, queue_item in enumerate(queue):
                if queue_item[2] <= 0:
                    del queue[idx]
            if len(queue) == 0:
                break

        # Construct t_data from g_data
        t_data = Algorithms.make_t_data_from_g_data(raw_job_data, g_data)

        return g_data, t_data

    @staticmethod
    def RR(job_data):
        """
        RR Simulation

        Parameters:
            `job_data`: list - "input" of user provided json
        """
        # g_data = []
        # t_data = []
        time_quantum = -1

        for header in job_data[0]:
            try:
                if header.startswith('time_quantum='):
                    time_quantum = int(re.search(r'=(\d)', header).group(1))
                    break
            except:
                raise Exception("Invalid time quantum value for Round Robin algorithm")
        else:
            raise Exception("Missing time quantum for Round Robin algorithm")

        raw_job_data = copy.deepcopy(job_data[1:])
        job_data = job_data[1:]
        queue = []
        g_data = []
        t_data = []
        time_now = 0
        selected_queue_idx = 0
        time_slice_counter = 0
        running_job = '-'
        # RR(time_quantum)
        while True:
            # If job arivval time reached, insert into queue
            for idx, job in enumerate(job_data):
                if job[1] == time_now:
                    queue.append(job)

            if time_slice_counter == time_quantum:
                queue.append(queue.pop(0))
                time_slice_counter = 0

            # Queue selection method
            # RR, dont interrupt if the time slice is still valid
            selected_queue_idx = 0

            # if last running job doesnt match, append
            if running_job != queue[selected_queue_idx][0]:
                running_job = queue[selected_queue_idx][0]
                g_data.append({"job": queue[selected_queue_idx][0], "len": 0})

            # queue cpu cycle -1
            queue[selected_queue_idx][2] = queue[selected_queue_idx][2] - 1

            # CPU cycle -1 then gant chart +1
            g_data[-1]['len'] = g_data[-1]['len'] + 1
            time_now = time_now + 1

            time_slice_counter = time_slice_counter + 1

            if queue[selected_queue_idx][2] <= 0:
                time_slice_counter = 0

            # If cpu cycle reached 0, remove from queue
            for idx, queue_item in enumerate(queue):
                if queue_item[2] <= 0:
                    del queue[idx]
            if len(queue) == 0:
                break

        # Construct t_data from g_data
        t_data = Algorithms.make_t_data_from_g_data(raw_job_data, g_data)

        return g_data, t_data

    @staticmethod
    def PreemptivePriority(job_data):
        """
        PreemptivePriority Simulation

        Parameters:
            `job_data`: list - "input" of user provided json
        """
        raw_job_data = copy.deepcopy(job_data[1:])
        job_data = job_data[1:]
        queue = []
        g_data = []
        t_data = []
        time_now = 0
        selected_queue_idx = 0
        running_job = "-"
        # PreemptivePriority
        while True:
            # If job arivval time reached, insert into queue
            for idx, job in enumerate(job_data):
                if job[1] == time_now:
                    queue.append(job)

            # Queue selection method
            # PreemptivePriority, always select highest priority in queue
            selected_queue_idx = 0
            highest_priority_idx = -1
            highest_priority = 999999
            for queue_idx, queue_item in enumerate(queue):
                if queue_item[3] < highest_priority:
                    highest_priority_idx, highest_priority = queue_idx, queue_item[3]

            selected_queue_idx = highest_priority_idx

            # if last running job doesnt match, append
            if running_job != queue[selected_queue_idx][0]:
                running_job = queue[selected_queue_idx][0]
                g_data.append({"job": queue[selected_queue_idx][0], "len": 0})

            # queue cpu cycle -1
            queue[selected_queue_idx][2] = queue[selected_queue_idx][2] - 1

            # CPU cycle -1 then gant chart +1
            g_data[-1]['len'] = g_data[-1]['len'] + 1
            time_now = time_now + 1

            # If cpu cycle reached 0, remove from queue
            for idx, queue_item in enumerate(queue):
                if queue_item[2] <= 0:
                    del queue[idx]
            if len(queue) == 0:
                break

        # Construct t_data from g_data
        t_data = Algorithms.make_t_data_from_g_data(raw_job_data, g_data)

        return g_data, t_data

    @staticmethod
    def NonPreemptivePriority(job_data):
        """
        NonPreemptivePriority Simulation

        Parameters:
            `job_data`: list - "input" of user provided json
        """
        raw_job_data = copy.deepcopy(job_data[1:])
        job_data = job_data[1:]
        queue = []
        g_data = []
        t_data = []
        time_now = 0
        selected_queue_idx = 0
        running_job = "-"
        dont_interrupt = False
        # PreemptivePriority
        while True:
            # If job arivval time reached, insert into queue
            for idx, job in enumerate(job_data):
                if job[1] == time_now:
                    queue.append(job)

            # Queue selection method
            # PreemptivePriority, always select highest priority in queue
            if not dont_interrupt:
                selected_queue_idx = 0
                highest_priority_idx = -1
                highest_priority = 999999
                for queue_idx, queue_item in enumerate(queue):
                    if queue_item[3] < highest_priority:
                        highest_priority_idx, highest_priority = queue_idx, queue_item[3]

                selected_queue_idx = highest_priority_idx
                dont_interrupt = True

            # if last running job doesnt match, append
            if running_job != queue[selected_queue_idx][0]:
                running_job = queue[selected_queue_idx][0]
                g_data.append({"job": queue[selected_queue_idx][0], "len": 0})

            # queue cpu cycle -1
            queue[selected_queue_idx][2] = queue[selected_queue_idx][2] - 1

            if queue[selected_queue_idx][2] <= 0:
                dont_interrupt = False

            # CPU cycle -1 then gant chart +1
            g_data[-1]['len'] = g_data[-1]['len'] + 1
            time_now = time_now + 1

            # If cpu cycle reached 0, remove from queue
            for idx, queue_item in enumerate(queue):
                if queue_item[2] <= 0:
                    del queue[idx]
            if len(queue) == 0:
                break

        # Construct t_data from g_data
        t_data = Algorithms.make_t_data_from_g_data(raw_job_data, g_data)

        return g_data, t_data
