from datetime import date,datetime, timedelta

def week_start_stop():
    today = date.today()
    monday = today - timedelta(days=today.weekday()) # monday
    friday = monday + timedelta(days=4) # friday
    return monday, friday



if __name__ == '__main__':
    print (str(week_start_stop()[0]))