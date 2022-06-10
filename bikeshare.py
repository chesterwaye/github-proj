import time
import pandas as pd
import numpy as np

#Cities for data collection
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
cities = ['chicago', 'new york city', 'washington']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs 
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in cities:
            break    
        else:
            print("\ninvalid city choosen.\n")
     
    while True:

        # get user input for month (all, january, february, ... , june)
        month = input("Please enter the month of january, february, march, april, may, or june\n").lower()
        if month in months:
             break
        else:
            print("\ninvalid month was choosen\n")

    while True:   
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input("Enter the day of week\n").lower()

        if day in days:
            break
        else:
            print("\ninvalid day choosen\n")

    print('*'*40)
    return city, month, day

    
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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    #df = np.nanmin(df['Birth Year'])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

 
    # extract month from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f"popular month {popular_month}")

     # extract day of week  from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #df['day_of_the_week'] = df['Start Time'].dt.weekday_name
    

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print(f"popular week {popular_day_of_week}")

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"popular hour {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    startStation = df['Start Station'].mode()[0]
    print(f"\nMost commonly used start station is {startStation}")


    # display most commonly used end station
    endStation = df['End Station'].mode()[0]
    print(f"\nMost commonly used end station is {endStation}")

    # display most commonly used start station
    print('\nmost common trip from start to end\n')
    commonUsedStartStation = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(commonUsedStartStation)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # display total travel time
    totalTravel = round(np.sum(df['Trip Duration']), 1)
    print(f"total travel time {totalTravel}" )


    # display mean travel time
    totalTravel = round(np.mean(df['Trip Duration']), 1)
    print(f"total travel mean {totalTravel}" )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"User counts are {user_types}")

    try:
        # Display counts of gender
        user_types = df['Gender'].value_counts()
        print(f"Gender counts:\n {user_types}")

        # Display earliest, most recent, and most common year of birth
        #df = df.fillna('', inplace=True)
        #df['Birth Year'].astype(int)
    

        earliestBirth = np.nanmin(df['Birth Year']).astype(int)
        recentBirth = np.nanmax(df['Birth Year']).astype(int)
        commonBirth = df['Birth Year'].mode()[0].astype(int)
        print(f"The earliest birth is {earliestBirth}")
        print(f"The most recent birth is {recentBirth}")
        print(f"The most common birth is {commonBirth}")

    except KeyError:
        print("Washington does not have any genders and Birth years.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Your docstring here """
    i = 0
    raw = input("Do you want to the first 5 rows of the raw data? Enter yes or no.\n").lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i: i + 5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("Would you like to see the next 5 rows? Enter yes or no.\n'").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()