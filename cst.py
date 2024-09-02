from datetime import datetime

### Discord related constants ###
CHANNEL_ID = "PUT YOUR CHANNEL ID HERE"
"""The id of the private chat you want to poll for the call history"""

AUTH_KEY = "PUT YOUR TOKEN HERE"
"""Your authorization key for to do the API call. You can get it using F12 in a browser on the Discord website"""


### Time selection for the request ###
START_TIME: datetime = datetime.utcnow()
"""The start time, in UTC, to research, so the closest time you want to start the search or the end of the period of the search"""

END_TIME: datetime = datetime(2020, 7, 1, 0, 0, 0)
"""The end time, in UTC, to research, so the farthest time you want to end the search or the start of the period of the search"""

# Ex for start and end time:
#   if periode you wanna search is from june 6th 2021 to november 5 2023
#       START_TIME = datetime(2023, 11, 5, 0, 0, 0)
#       END_TIME = datetime(2021, 6, 6, 0, 0, 0)
