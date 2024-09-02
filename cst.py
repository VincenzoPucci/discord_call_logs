from datetime import datetime

### Discord related constants ###
CHANNEL_ID = "PUT YOUR CHANNEL ID HERE"
"""The id of the private chat you want to poll for the call history"""

AUTH_TOKEN = "PUT YOUR TOKEN HERE"
"""Your authorization token for to do the API call. You can get it using F12 in a browser on the Discord website"""


### Time selection for the request ###
START_DATE: datetime = datetime(year=2024, month=9, day=1)
"""The start time, in UTC, to research, so the closest time you want to start the search or the end of the period of the search"""

END_DATE: datetime = datetime(year=2020, month=7, day=1)
"""The end time, in UTC, to research, so the farthest time you want to end the search or the start of the period of the search"""

# Ex for start and end time:
#   if periode you wanna search is from june 6th 2021 to november 5 2023
#       START_DATE = datetime(year=2023, month=11, day=5)
#       END_DATE = datetime(year=2021, month=6, day=6)
