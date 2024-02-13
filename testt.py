


import datetime


def convert_date(date_str, date_format="%Y-%m-%d"):
    """
    Takes a date string, goes one day back, and returns the date in 'yyyymmdd' format.

    :param date_str: Date string in the format specified by date_format.
    :param date_format: Format of the input date string. Default is '%Y-%m-%d'.
    :return: String representing the date one day before date_str in 'yyyymmdd' format.
    """
    # Convert the string to a datetime object
    date_obj = datetime.datetime.strptime(date_str, date_format)
    
    # Subtract one day
    one_day_back = date_obj - datetime.timedelta(days=1)
    
    # Convert back to string in 'yyyymmdd' format
    one_day_back_str = one_day_back.strftime("%Y%m%d")
    
    return one_day_back_str
date_str = "2024-02-13" # Example input
converted_date = convert_date(date_str)
print(converted_date)
# current_date = '2022-01-01'
# current_date+= datetime.timedelta(days=1)
# print(current_date)