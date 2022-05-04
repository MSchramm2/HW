import re
import datetime

def sanity_check():
    """This test should always pass.
    The purpose is to make sure Github actions are functioning properly.
    """
    return True

def get_chat_message(row):
   # print(message)
   # return the second part of the split.
   # and join, just in case there is another '> ' in the message
    message = re.split(r'> ', row)
    return "> ".join(message[1:])


def get_current_date(dateline):
    """    Parse the IRC log date format to find the current date

    Return a POSIX (datetime) form date for midnight

    Args:
        dateline (str): Row that begins with `---`

    Returns:
        datetime: datetime object with the date from the row 
    """

    times = dateline.split()
    year = ""
    month = ""
    day = ""
    
    for time in times:
        if len(time) == 4:
            year = time
        if len(time) == 3:
            month = time
        if len(time) == 2:
            day = time
    month_number = datetime.datetime.strptime(month, "%b").month
    return datetime.datetime(int(year), month_number, int(day))
    
            


def get_hours_minutes(time_row):
    result = re.search(r'(\d{2}):(\d{2})', time_row)
    hours = result.group(1)
    minutes = result.group(2)
   
    time_dic ={
        'hour': int(hours),
        'minute': int(minutes)
        }
    return time_dic

def get_join_quit_type(row):
    """Returns if a row is a join or a quit,


    Args:
        row (str): join or quit row

    Returns:
        str: "join" or "quit"
    """
    join = re.search('join', row)
    if not(join == None) and join.group() == 'join':
        return 'join'
    quit = re.search('quit', row)
    if not(quit == None) and quit.group() == 'quit':
        return 'quit'
    left = re.search('left', row)
    if not(left == None) and left.group() == 'left':
        return 'quit'


def get_join_quit_username(row):
    """ Input a join/quit row, get a username back.

    Args:
        row (str): Must be a join/quit row. These
        have `-!-` after the timestamp.

    Returns:
        str: the username from the row.
    """
    joinQuitUser = re.search(r'(-!-)\s(.*) \[.*@', row)
    return joinQuitUser.group(2)
        

def get_user_name(row):
    """
    Find the username in a chat row.

    Parameters
    ----------
    row : str
        row that contains a message.

    Returns
    -------
    string
        string with username.

    """
    user_name = re.search(r'<.(.*?)>',row)
    return user_name.group(1)

def get_user_prefix(row):
    """ Gets the prefix of a username, if any.
    If there is not a prefix, return None.

    For example, '@' or '+'.

    Args:
        row (str): chat message row.

    Returns:
        str: the user prefix (if any)
    """
    name = get_user_name(row)
    sym = re.search(r'[a-zA-Z0-9]', name[0])
    if sym.group() == None:
        return name[0]

def is_date_row(row):
    """
    Check if row indicates date change.
    Row contains --- at the start

    Parameters
    ----------
    row : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    """
    if re.search(r'---', row):
      return True
    return False


def is_join_quit(row):
    """
    Check if message is a join/quit/metadata row.
    Row contains -!- at the start

    Parameters
    ----------
    row : str
        row that you want to check.
    

    Returns
    -------
    bool
        DESCRIPTION.

    """
    if re.search(r'(-!-)', row).group() == None:
        return False
    return True


def is_message(row):
    """
    Determine if a row contains a message.

    Parameters
    ----------
    row : str
        row from chat log.

    Returns
    -------
    bool
        True if row belongs to chat log.

    """
    if row[6] == '<':
       return True
    return False


def find_urls(text):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(text))
    return urls