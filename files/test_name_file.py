import datetime

def generate_result_string():
    current_datetime = datetime.datetime.now()
    result_string = f"Result{current_datetime.year}{current_datetime.month:02d}{current_datetime.day:02d}{current_datetime.hour:02d}{current_datetime.minute:02d}{current_datetime.second:02d}"
    return result_string

# result_string = generate_result_string()
# print(result_string)
