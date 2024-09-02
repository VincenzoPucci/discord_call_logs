import json
import math
import time
import requests
import snowflake  # py -3 -m pip install -U snowflake-util
from datetime import datetime

from cst import *


### YOU SHOULD NOT TOUCH THESE CONSTANTS ###
### The editable constants are in the cst.py file ###
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f+00:00"
DATETIME_FORMAT_2 = "%Y-%m-%dT%H:%M:%S+00:00"
DC_PATH = "./call_log.json"
CALL_MESSAGE_TYPE = 3

# Discord request url and header
DISCORD_URL = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
HEADER = {"authorization": AUTH_TOKEN}

# Setting up Snowflake to translate datetimes to snoflake timestamp that the API uses.
SnowClass = snowflake.Snowflake()

total_amount_of_call: int = 0
"""Total amount of individual calls between the 2 users"""

total_call_time_hours: float = 0.0
"""Total amount of time spend in calls between the 2 users in hours"""

total_call_time_days: float = 0.0
"""Total amount of time spend in calls between the 2 users in days"""

average_call_time_hours: float = 0.0
"""Average amount of time of calls between the 2 users in hours"""


def write_in_file(call_list: list):
    """Dumps the list of call in the json file after getting it all"""
    print(f"Writing the data in the JSON file")
    with open(DC_PATH, 'w') as f:
        json.dump(call_list, f)


def read_in_file() -> list[dict]:
    """Reads the call logs from the file"""
    call_data: list[dict] = []
    with open(DC_PATH, 'r') as f:
        call_data = json.load(f)
    return call_data


def get_snowflake_from_datetime(date: datetime) -> str:
    """Translate a datetime to a snowflake for the Discord API"""
    discord_snowflake = SnowClass.generate_discord_snowflake(worker=5, process=5, sequence=222, date=date)
    return discord_snowflake


def get_datetime_from_snowflake(discord_snowflake: str) -> datetime:
    """Translate a discord snowflake to a datetime in UTC"""
    return SnowClass.parse_discord_snowflake(discord_snowflake)[0]


def remove_not_needed(message: dict) -> dict:
    """Removes the part that aren't needed from the message to save memory"""
    message.pop("content")
    message.pop("mentions")
    message.pop("mention_roles")
    message.pop("attachments")
    message.pop("embeds")
    message.pop("edited_timestamp")
    message.pop("flags")
    message.pop("components")
    message.pop("pinned")
    message.pop("mention_everyone")
    message.pop("tts")
    return message


def convert_str_to_datetime(string_date: str) -> datetime:

    try:
        return datetime.strptime(string_date, DATETIME_FORMAT)
    except:
        return datetime.strptime(string_date, DATETIME_FORMAT_2)


def get_messages_for_period():
    """Gets the data from Discord for the period and saves it in the file"""
    # Setting up the variables needed
    call_list: list = []
    last_timestamp: datetime = datetime.utcnow()
    discord_snowflake = get_snowflake_from_datetime(START_TIME)

    print(f"Starting to get the data from Discord, this might take a while...")
    while last_timestamp > END_TIME:
        # Doing the call and getting the result list
        res = requests.get(DISCORD_URL, headers=HEADER, params={"before": discord_snowflake, "limit": 100})
        message_list: list[dict] = res.json()

        try:
            # Getting the next discord_snowflake for the search
            # The field "id" in the message is the snowflake for it so we take the last one in the list for next run
            discord_snowflake = message_list[-1]["id"]
            last_timestamp = get_datetime_from_snowflake(discord_snowflake)
        except:
            # Discord has rate limited our call so we wait a second and retry the same call
            print(f"Getting rate limited, waiting a second")
            time.sleep(1)
            continue  # this restart the loop with the timestamp that got rate limited

        # Going through all the messages and getting only "type == 3" messages (call related messages)
        for message in message_list:
            if message["type"] == CALL_MESSAGE_TYPE:
                message = remove_not_needed(message)
                call_list.append(message)

    # Saving the messages by writing them in a file
    write_in_file(call_list)


def calculate_data():
    """Gets all the data from the call log file"""
    # Getting data from file
    call_data: list[dict] = read_in_file()
    print("Starting to analyse the data")

    # Setting total call amount
    global total_amount_of_call, total_call_time_hours, total_call_time_days, average_call_time_hours
    total_amount_of_call = len(call_data)

    # Getting total call time
    total_time_seconds: float = 0.0
    for call in call_data:
        start_time = convert_str_to_datetime(call["timestamp"])
        end_time = convert_str_to_datetime(call["call"]["ended_timestamp"])
        delta = end_time-start_time
        total_time_seconds += delta.total_seconds()

    total_call_time_hours = (total_time_seconds/60)/60
    total_call_time_days = total_call_time_hours/24
    average_call_time_hours = total_call_time_hours/total_amount_of_call


def print_result():
    """Print the results in the console for easy reading"""
    global total_amount_of_call, total_call_time_hours, total_call_time_days, average_call_time_hours

    # Calculating the minutes for total_call_time_hours
    call_time_hours_floor: int = math.floor(total_call_time_hours)
    call_time_hours_min: int = int((total_call_time_hours - call_time_hours_floor) * 60)

    # Calculating the hours for total_call_time_days
    call_time_days_floor: int = math.floor(total_call_time_days)
    call_time_days_hours: int = int((total_call_time_days - call_time_days_floor) * 24)

    # Calculating the minutes for average_call_time_hours
    av_call_time_hours_floor: int = math.floor(average_call_time_hours)
    av_call_time_hours_min: int = int((average_call_time_hours - av_call_time_hours_floor) * 60)

    # Prints of the data collected
    print(f"The period analysed is from {END_TIME} UTC to {START_TIME} UTC")
    print(f"Total amount of calls they have had: {total_amount_of_call} calls")
    print(f"Total amount of time in hours spent in call together: {call_time_hours_floor}h {call_time_hours_min}min")
    print(f"Total amount of time in days spent in call together: {call_time_days_floor} days {call_time_days_hours}h")
    print(f"Average duration of the calls for the period: {av_call_time_hours_floor}h {av_call_time_hours_min}min")


def main():
    # get_messages_for_period()
    calculate_data()
    print_result()


if __name__ == '__main__':
    main()
