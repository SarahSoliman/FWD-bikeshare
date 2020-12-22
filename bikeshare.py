import time
import pandas as pd
from termcolor import colored
from tabulate import tabulate

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'All']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    trials = 0
    city = input(colored('Please choose one of these cities to view its data (Chicago, New York City, Washington):',
                         attrs=['bold']))
    city = city.lower()
    while city not in CITY_DATA.keys():
        city = input(
            colored('Invalid input!\n', 'red')
            + colored(
                'Please try again to choose one of these cities to view its data (chicago, new york city, washington):',
                attrs=['bold']))
        city = city.lower()
        trials += 1
        if trials == 5:
            raise Exception('Entered an invalid city too many times')

    trials = 0
    month = input(colored("Please choose a month to filter by {}:".format(MONTHS), attrs=['bold']))
    month = month.capitalize()
    while month not in MONTHS:
        month = input(
            colored('Invalid input!\n', 'red')
            + colored('Please try again to choose a month to filter by {}:'.format(MONTHS), attrs=['bold']))
        month = month.capitalize()
        trials += 1
        if trials == 5:
            raise Exception('Entered an invalid month too many times')

    trials = 0
    day = input(colored('Please choose a day to filter by {}:'.format(DAYS), attrs=['bold']))
    day = day.capitalize()
    while day not in DAYS:
        day = input(
            colored('Invalid input!\n', 'red')
            + colored('Please try again to choose a day to filter by {}:'.format(DAYS), attrs=['bold']))
        day = day.capitalize()
        trials += 1
        if trials == 5:
            raise Exception('Entered an invalid day too many times')

    print('-' * 40)
    return city, month, day


def validate_headers(df, headers):
    for header in headers:
        if header not in df:
            raise Exception('Missing header: {}'.format(header))


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    validate_headers(df, ['Start Time', 'Start Station', 'End Station', 'Trip Duration', 'User Type'])

    # extract month and day of week from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].apply(lambda x: x.hour)
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.weekday())

    if month != 'All':
        df = df[df['month'] == MONTHS.index(month)]

    if day != 'All':
        df = df[df['day_of_week'] == DAYS.index(day)]

    return df


def show_raw_data(df):
    """
    prompts the user if they want to see raw data and keeps displaying as much data as requested
    Args:
        df: Pandas DataFrame that holds the data to display
    """
    show_lines = input(colored('Do you want to see some raw data? Enter yes or no.\n', 'green'))
    index = 0
    while show_lines.lower() == 'yes':
        print(
            tabulate(df.iloc[index:index + 5].drop(['hour', 'month', 'day_of_week'], axis=1), headers=df.columns.values,
                     tablefmt="rst",
                     showindex=False))
        index += 5
        if index >= len(df):
            print(colored('You have reached the end of file!', 'blue'))
            break
        show_lines = input(colored('\nDo you want to see the next 5 lines? Enter yes or no.\n', 'green'))


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].mode().values.tolist()
    print(colored('Most common month(s): ', 'green') + ','.join([MONTHS[x] for x in most_common_month]))

    # Display the most common day of week
    most_common_day = df['day_of_week'].mode().values.tolist()
    print(colored('Most common day(s): ', 'green') + ','.join([DAYS[x] for x in most_common_day]))

    # Display the most common start hour
    most_common_hour = df['hour'].mode()
    most_common_hour = most_common_hour.values.tolist()
    print(colored('Most common hour(s): ', 'green') + ','.join([str(x) for x in most_common_hour]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start = df['Start Station'].mode().values.tolist()
    print(colored('Most common start station(s): ', 'green') + ','.join(most_common_start))

    # Display most commonly used end station
    most_common_end = df['End Station'].mode().values.tolist()
    print(colored('Most common end station(s): ', 'green') + ','.join(most_common_end))

    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' To ' + df['End Station']
    most_common_trip = df['trip'].mode().values.tolist()
    print(colored('Most common trip(s): ', 'green'))
    print('\n'.join(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def format_seconds(seconds):
    hours, rem = divmod(seconds, 120)
    minutes, seconds = divmod(rem, 60)
    return '{} hours, {} minutes, {} seconds'.format(int(hours), int(minutes), int(seconds))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(colored('Total travel time: ', 'green') + format_seconds(total_travel_time))

    # Display mean travel time
    print(colored('Mean travel time: ', 'green') + format_seconds(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def draw_bar_chart(data):
    max_value = float(data.max())
    increment = max_value / 25
    longest_label_length = max([len(x) for x in data.index.values])

    for label, count in data.items():
        count = int(count)
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)
        bar = '█' * bar_chunks
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))

        # If the bar is empty, add a left one-eighth block
        bar = bar or '▏'

        print(f'{label.rjust(longest_label_length)} ▏ {count:#4d} {bar}')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(colored('User types:', 'green'))
    draw_bar_chart(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df:
        print(colored('\nGender Stats:', 'green'))
        draw_bar_chart(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print(colored('\nEarliest Year of birth: ', 'green') + str(int(df['Birth Year'].min())))
        print(colored('Most Recent Year of birth: ', 'green') + str(int(df['Birth Year'].max())))
        print(colored('Most Common Year of birth: ', 'green') + str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    print(colored("Welcome to Bikeshare Project!\n\n", 'green', attrs=['bold']))

    try:
        while True:
            city, month, day = get_filters()

            df = load_data(city, month, day)

            if len(df) < 1:
                print(colored('Not enough data to continue processing, please try other filters', 'blue'))
                continue

            show_raw_data(df)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            restart = input(colored('\nWould you like to restart? Enter yes or no.\n', 'green', attrs=['bold']))
            if restart.lower() != 'yes':
                break

    except Exception as e:
        print(colored(e, 'red'))
        print(colored('Bye!', 'red'))


if __name__ == "__main__":
    main()
