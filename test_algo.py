from datetime import datetime, timedelta


file_path = "dataset/cam_data/test.txt"

# Read the contents of the text file
with open(file_path, "r") as file:
    data = file.read()

lines = data.strip().split('\n')

events = []

for line in lines:
    parts = line.split()
    timestamp = parts[0]
    distance = int(parts[1])  # meter
    speed = int(parts[2])  # km/h
    latitude = float(parts[3])
    longitude = float(parts[4])

    event_time = datetime.strptime(timestamp, "%H:%M:%S")
    formatted_latitude = "{:.8f}".format(latitude)
    formatted_longitude = "{:.8f}".format(longitude)

    events.append((event_time, distance, speed,
                    formatted_latitude, formatted_longitude))

near_crash_events = []
crash_events = []

# Time threshold for grouping events (5 seconds)
time_threshold = timedelta(seconds=5)

prev_event_group = []

for event in events:
    event_time, distance, speed, formatted_latitude, formatted_longitude = event

    current_event_group = prev_event_group.copy()

    # Check if current event is within the time threshold of the previous event group
    if len(prev_event_group) > 0 and event_time - prev_event_group[-1][0] <= time_threshold:
        current_event_group.append(event)
    else:
        # Process the previous event group
        if len(current_event_group) > 0:
            # Check if the current event group contains a near crash event
            if any(distance == 1 and speed >= 10 for _, distance, speed, _, _ in current_event_group):
                # Extend the event group backward and forward until reaching the time threshold or encountering a crash event
                backward_index = len(current_event_group) - 1
                forward_index = 0

                while backward_index >= 0 or forward_index < len(current_event_group):
                    if backward_index >= 0:
                        backward_event = current_event_group[backward_index]
                        backward_time, _, _, _, _ = backward_event

                        backward_diff = event_time - backward_time

                        if backward_diff <= time_threshold and not any(distance == 0 and speed >= 10 for _, distance, speed, _, _ in current_event_group[:backward_index]):
                            current_event_group.insert(
                                0, backward_event)
                            backward_index -= 1
                        else:
                            break

                    if forward_index < len(current_event_group):
                        forward_event = current_event_group[forward_index]
                        forward_time, _, _, _, _ = forward_event

                        forward_diff = forward_time - event_time

                        if forward_diff <= time_threshold and not any(distance == 0 and speed >= 10 for _, distance, speed, _, _ in current_event_group[forward_index + 1:]):
                            current_event_group.append(forward_event)
                            forward_index += 1
                        else:
                            break

                # Add the extended event group to the corresponding list
                if any(distance == 0 and speed >= 10 for _, distance, speed, _, _ in current_event_group):
                    crash_events.append(current_event_group)
                else:
                    near_crash_events.append(current_event_group)

        # Start a new event group
        current_event_group = [event]

    # Update previous event group
    prev_event_group = current_event_group

# Process the last event group
if len(prev_event_group) > 0:
    if any(distance == 1 and speed >= 10 for _, distance, speed, _, _ in prev_event_group):
        if any(distance == 0 and speed >= 10 for _, distance, speed, _, _ in prev_event_group):
            crash_events.append(prev_event_group)
        else:
            near_crash_events.append(prev_event_group)

# Print the categorized events
print("Near Crash Events:")
for event_group in near_crash_events:
    for event in event_group:
        event_time, distance, speed, formatted_latitude, formatted_longitude = event
        print(event_time.strftime("%H:%M:%S"), distance,
            speed, formatted_latitude, formatted_longitude)
    print()

print("Crash Events:")
for event_group in crash_events:
    for event in event_group:
        event_time, distance, speed, formatted_latitude, formatted_longitude = event
        print(event_time.strftime("%H:%M:%S"), distance,
            speed, formatted_latitude, formatted_longitude)
    print()
