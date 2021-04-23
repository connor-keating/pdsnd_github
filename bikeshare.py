import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv' }
ACCEPTABLE_MONTHS = ['January',
                'February',
                'March',
                'April',
                'May',
                'June',
                'All']
WEEKDAYS = ['Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
            'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city, month, day = '', '', ''
    good_city, good_month, good_day = False, False, False
    while not good_city:
        if city in CITY_DATA.keys():
            good_city = True
        else:
            for name in CITY_DATA.keys():
                print(name.title())
            city = input('\nPlease enter one of the above cities.\n').lower()

    # get user input for month (All, january, february, ... , june)
    while not good_month:
        if month in ACCEPTABLE_MONTHS:
            good_month = True
        else:
            print('\n')
            for element in ACCEPTABLE_MONTHS:
                print(element)
            month = input('\nPlease enter one of the above options for which month to examine.\n').title()

    # get user input for day of week (All, monday, tuesday, ... sunday)
    while not good_day:
        if day in WEEKDAYS:
            good_day = True
        else:
            print('\n')
            for element in WEEKDAYS:
                print(element)
            day = input('\nPlease enter one of the above options for which day to examine.\n').title()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "All" to apply no month filter
        (str) day - name of the day of week to filter by, or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # reading csv file
    data_file = CITY_DATA[city]
    df = pd.read_csv(data_file)
    
    # Cleaning time column
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Weekday'] = df['Start Time'].dt.day_name()

    # filter by month of the year is applicable
    if month != 'All':
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['Weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    create_most_common_output_string('month', popular_month)

    # display the most common day of week
    popular_day = df['Weekday'].mode()[0]
    create_most_common_output_string('weekday', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    create_most_common_output_string('hour', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    create_most_common_output_string('Start Station', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    create_most_common_output_string('End Station', popular_end)

    # display most frequent combination of start station and end station trip
    df['Both Stations'] = 'From: ' + df['Start Station'] + ' To: ' + df['End Station']
    popular_trip = df['Both Stations'].mode()[0]
    create_most_common_output_string('trip', popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() // 60
    create_duration_output_string('total', total_travel_time)


    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean() // 60
    create_duration_output_string('average', avg_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    amt_users = df['User Type'].value_counts()
    types_out = 'The amount of {}s is {}'
    create_user_output_string(types_out, amt_users)

    # Display counts of gender
    if 'Gender' in df.columns:
        amt_gender = df['Gender'].value_counts()
        gender_out = 'There amount of {} users is {}'
        create_user_output_string(gender_out, amt_gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        latest_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        birth_out = 'The {} is {}'
        birth_data = {
            'earliest year of birth':earliest_birth_year,
            'most recent year of birth':latest_birth_year,
            'most common year of birth':common_birth_year
        }
        create_user_output_string(birth_out, birth_data)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df, position):
    counter = 5
    try:
        display = df.iloc[position:position+5]
        for row in range(position,position+5):
            print(df.iloc[row])
            counter -= 1
    except IndexError:
        for row in range(0, counter):
            print(df.iloc[row])

def create_most_common_output_string(target, answer):
    """Create and print string to be printed to screen for most common things"""
    print('The most common {} is: {}'.format(target, answer))


def create_duration_output_string(calculation, answer):
    """Create and print string to terminal for calculated duration statistics"""
    print('The {} travel time is {} minutes'.format(calculation, answer))


def create_user_output_string(in_string, data):
    """Create and print string to terminal for user information"""
    for index, value in data.items():
        print(in_string.format(index, value))


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        data_position = 0
        while True:
            show_raw = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if show_raw.lower() == 'yes':
                show_raw_data(df, data_position)
                data_position += 5
            elif show_raw == 'no':
                break
            else:
                print('Invalid command')
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
