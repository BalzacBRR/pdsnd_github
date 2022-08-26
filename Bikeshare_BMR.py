import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington).
    city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
    # Checks if user has entered correctly from list of cities
    while city != 'chicago' and city != 'washington' and city != 'new york city':
            city = input('Please enter either "Chicago", "New York City", or "Washington"\n').lower()
        
    # get user input for month (all, january, february, ... , june)        
    response = input("Would you like to filter the data by month, day, or not at all?\n").lower()
          
    while response != 'month' and response != 'day' and response != 'not at all':
            response = input('Please enter either "month", "day", or "not at all"\n').lower()
    # get user input for month (all, january, february, ... , june)
    # Sets day to all    
    if response == 'month':
            day = 'all'
            month = input('Please enter the month for which to filter data - January, February, March, April, May, or June?\n').lower()
            while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june':
                month = input('Please enter either January, February, March, April, May, or June\n').lower()
    # get user input for day as integers 0 through 6 for Sunday through Saturday
    # Returns str of day of week based upon index from user input
    # Sets month to all            
    elif response == 'day':
            month = 'all'
            days_of_week = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
            day_num = int(input('Please enter the day for which to filter data. Please enter day as an integer (e.g. 0 = Sunday, 1 = Monday)\n'))
            # while loop to check return day of week str
            # while loop with try to check if user has entered a value greater than 6 and prompts for user to re-enter integer
            while True:
                try:
                    day = days_of_week[day_num]
                    break
                except:
                    day_num = int(input('Please enter the day for which to filter data. Please enter day as an integer between 0 and 6 (e.g. 0 = Sunday, 1 = Monday)\n'))
    # sets month and day to all when not at all is entered
    else:
        month = 'all'
        day = 'all'

    print('-'*40)
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('The most common month =', months[df['month'].mode()[0]-1].title())

    # display the most common day of week
    print('The most common day of the week =', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('The most common start hour =', df['start_hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station =', df['Start Station'].mode()[0].title())

    # display most commonly used end station
    print('The most commonly used end station =', df['End Station'].mode()[0].title())

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' going to ' + df['End Station']
    print('The most commonly used start and end stations =', df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total time travelled =', df['Trip Duration'].sum())

    # display mean travel time
    print('The mean travel time =', df['Trip Duration'].mean())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    # No data in washington checked
    if city == 'washington':
        print('\nNo gender data available.\n')
    else:
        gender = df['Gender'].value_counts()

        print(gender)

    # Display earliest, most recent, and most common year of birth
    # No data in washington checked
    if city == 'washington':
        print('No birth year data available.\n')
    else: 
        print('\nThe earliest birth year =', df['Birth Year'].astype('Int64').min())
        print('The most recent birth year =', df['Birth Year'].astype('Int64').max())
        print('The most common birth year =', df['Birth Year'].astype('Int64').mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def printing_data(df):
    """prints the database on a 5 line increment until completely shown or user opts out
    
    Args:
        Increment = set initialy at 5 - this can be seen as a max increment
    
        Total_printed = tracks how many lines have been printed thus far
    
        Remaining  = tracks how many lines have not yet been printed
    
        incrementa = checks to make sure if any remaining lines to be printed are less that increment
    
    Returns:
        Prompt if the user wants to see data
        Printed data on increments of 5 (or less if less lines available)
    
    """
    increment = 5 # Default and maximum increment for printing
    total_printed = 0 # Initial count of lines printed
    remaining = len(df) - total_printed # Reads length of datafile and tracks how many left to print
    incrementa = min(increment, remaining) # Adjusts printing increment if remaining lines thess than increment (i.e.5)
    # increment being checked for end of file or lines being less than 5
    while incrementa > 0:
            # asking if user wants to see data. Only prints if answer is yes
            print_opt = input('Would you like to print raw data 5 lines at a time (yes of no)?').lower()
            if print_opt != 'yes':
                break
            # prints at increments of 5 or less abd resets tracker arguments
            print(df.iloc[total_printed:total_printed + incrementa])
            total_printed += incrementa
            remaining -= incrementa
            incrementa = min(increment, remaining)
            # check if all lines have been printed
            if total_printed == len(df):
                print('All data has been printed.')
                break
   
while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        printing_data(df)
        #checks if user wants to analyse more of exit
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break

        
        
        
        
        