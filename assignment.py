"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/


The assignment is due 25/10/2021 at 9:00 am, Canberra time

Collaborators: <list the UIDs of ALL members of your project group here>
u7237249
u7272824
u7190768
"""
import os
import csv
import numpy as np
import pandas as pd
import glob


def analyse(path_to_files):
    """
    Call all functions to answer Q1-Q4
    :param path_to_files: The path to the folder where the data is stored
    """
    print("Analysing data from folder " + path_to_files)
    print("Question 1:")
    print("Most recent data is in file " + "'" + find_most_recent_data(path_to_files) + "'")
    print("Last updated at " + find_last_updated_record(path_to_files))
    print("Total worldwide cases: " + str(get_total_worldwide_cases(path_to_files)) + " , " + "Total worldwide deaths:"
          + str(get_total_worldwide_deaths(path_to_files)))
    print("Question 2:")
    # Invoke function get_top10_countries_data to print the top 10 countries
    # with total cases, deaths, new cases and active cases
    get_top10_countries_data(path_to_files)
    print("Question 3:")
    daily_death_and_new_cases()
    print("Question 4:")
    get_incident_rate_and_case_fatality_ratio(path_to_files)


def find_most_recent_data(path_to_files):
    """
    Find file with the most recent date from the given file path.
    Assume that the file path exists.
    Assume that the folder of the path is not empty.
    :param path_to_files: The path to the folder where the data is stored
    :return: The name of file that is the most recent
    """

    # Initialize files to be a list of all files in the given path
    files = os.listdir(path_to_files)
    # Initialize most_recent_year, most_recent_month, most_recent_day to be 0
    # and most_recent_date to be an empty string
    most_recent_year, most_recent_month, most_recent_day = 0, 0, 0
    most_recent_date = ""

    # This loop iterate through files to find the most recent file
    for file in files:
        # Files with incorrectly formatted filenames will not be considered
        if file.endswith("csv"):
            # Initialize day, month, year with the name of file
            day = int(file[3:5])
            month = int(file[0:2])
            year = int(file[6:10])

            # Compare year, month and day to get the most recent file
            # When the upper level is the same,
            # if the lower level is larger, the time is later
            if year > most_recent_year:
                most_recent_year, most_recent_month, most_recent_day = year, month, day
                most_recent_date = file
            elif (year == most_recent_year) and (month > most_recent_month):
                most_recent_year, most_recent_month, most_recent_day = year, month, day
                most_recent_date = file
            elif (month == most_recent_month) and (day > most_recent_day):
                most_recent_year, most_recent_month, most_recent_day = year, month, day
                most_recent_date = file
    return most_recent_date


def find_last_updated_record(path_to_files):
    """
    From the most recent file find out the exact timestamp of the last record being updated.
    Assume that last update time might be different for different rows
    and that the last update time may not be from last row of the data file
    :param path_to_files: The path to the folder where the data is stored
    :return: The time of last updated record
    """
    # Initialize file to be the data file
    file = path_to_files + "/" + find_most_recent_data(path_to_files)
    # Initialize col_Last_Update to be a list of the time of last updated record
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        table = [row for row in reader][1:]
        col_last_update = [row[4] for row in table]

    # Initialize most_recent_year, most_recent_year, most_recent_day, last_hour, last_min, last_sec to be 0
    # and last_time to be an empty string
    most_recent_year = 0
    most_recent_month = 0
    most_recent_day = 0
    last_hour = 0
    last_min = 0
    last_sec = 0
    last_time = ""

    # This loop iterate through col_Last_Update to find the last time
    for time in col_last_update:
        # Initialize hour, min, sec, day, month, year to be the time in col_Last_Update
        hour = int(time[11:13])
        minute = int(time[14:16])
        sec = int(time[17:19])
        day = int(time[9:11])
        month = int(time[5:7])
        year = int(time[0:4])

        # Compare year, month, day, hour, minute, sec to get the last updated time
        # When the upper level is the same,
        # if the lower level is larger, the time is later
        if year > most_recent_year:
            most_recent_year, most_recent_month, most_recent_day = year, month, day
            last_time = time
        elif (year == most_recent_year) and (month > most_recent_month):
            most_recent_year, most_recent_month, most_recent_day = year, month, day
            last_time = time
        elif (month == most_recent_month) and (day > most_recent_day):
            most_recent_year, most_recent_month, most_recent_day = year, month, day
            last_time = time
        elif (day == most_recent_day) and (hour > last_hour):
            last_hour, last_min, last_sec = hour, minute, sec
            last_time = time
        elif (hour == last_hour) and (minute > last_min):
            last_hour, last_min, last_sec = hour, minute, sec
            last_time = time
        elif (minute == last_min) and (sec > last_sec):
            last_hour, last_min, last_sec = hour, minute, sec
            last_time = time

    return last_time


def get_total_worldwide_cases(path_to_files):
    """
    From this most recent file, report the total number of cases worldwide.
    Assume the data of cases does not have empty data
    :param path_to_files: The path to the folder where the data is stored
    :return: the number of total worldwide cases
    """
    # Initialize file to be the data file
    file = path_to_files + "/" + find_most_recent_data(path_to_files)
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        table = [row for row in reader][1:]
        # Initialize col_Confirmed to be empty
        col_confirmed = []
        # This loop iterate through data table to initialize col_Confirmed to be a list of the number of cases
        for row in table:
            col_confirmed.append(int(row[7]))

    # Sum the numbers in the list to to get total worldwide cases
    num_cases = sum(col_confirmed)
    return num_cases


def get_total_worldwide_deaths(path_to_files):
    """
    From this most recent file, report the total number of deaths worldwide.
    Assume the data of deaths does not have empty data
    :param path_to_files: The path to the folder where the data is stored
    :return: the number of total worldwide deaths
    """
    # Initialize file to be the data file
    file = path_to_files + "/" + find_most_recent_data(path_to_files)
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        table = [row for row in reader][1:]
        # Initialize col_Deaths to be empty
        col_deaths = []
        # This loop iterate through data table to initialize col_Deaths to be a list of the number of deaths
        for row in table:
            col_deaths.append(int(row[8]))

    # Sum the numbers in the list to to get total worldwide deaths
    num_deaths = sum(col_deaths)
    return num_deaths


def get_top10_countries_data(path_to_files):
    """
    Sort the countries in descending order of number of cases
    And report the top 10 countries with total cases, deaths, new cases and active cases
    """
    # Initialize today_file to be the most recent file
    today_file = path_to_files + "/" + find_most_recent_data(path_to_files)
    files = os.listdir(path_to_files)
    # Initialize yestoday_file to be the file of the one day immediately before the last update
    yesterday_file = path_to_files + "/" + files[files.index(find_most_recent_data(path_to_files)) - 1]
    # Initialize today_table to be the data of today_file
    # and yesterday_table to be the data of yesterday_file
    today_table = pd.read_csv(today_file)
    yesterday_table = pd.read_csv(yesterday_file)

    """
    Merge data tables to eliminate duplicate countries. 
    Add up the data for the confirmed and deaths columns in same country to record them only once. 
    Record them as today_duplicate_data_sum and yesterday_duplicate_data_sum respectively by the time. 
    """
    today_table_grouped = today_table.groupby(by=['Country_Region'])
    today_duplicate_data_sum = today_table_grouped.aggregate(np.sum).loc[:, ['Confirmed', 'Deaths']]
    yesterday_table_grouped = yesterday_table.groupby(by=['Country_Region'])
    yesterday_duplicate_data_sum = yesterday_table_grouped.aggregate(np.sum).loc[:, ['Confirmed', 'Deaths']]
    """
    Sort the countries in descending order of number of cases.
    Take out the top 10 and assign their data to today_top_10_countries_data 
    and yesterday_top_10_countries_data respectively by the time.
    """
    today_countries_data_sorted = today_duplicate_data_sum.sort_values(by=['Confirmed', 'Deaths'], ascending=False)
    today_top_10_countries_data = today_countries_data_sorted.head(10).reset_index()
    today_top_10_countries_data = np.array(today_top_10_countries_data[['Country_Region', 'Confirmed', 'Deaths']])
    yesterday_data_sorted = yesterday_duplicate_data_sum.sort_values(by=['Confirmed', 'Deaths'], ascending=False)
    yester_top_10_countries_data = yesterday_data_sorted.head(10).reset_index()
    yester_top_10_countries_data = np.array(yester_top_10_countries_data[['Country_Region', 'Confirmed', 'Deaths']])

    # Initialize new_cases to be the difference of today_top_10_countries_data
    # and yesterday_top_10_countries_data in Confirmed column.
    new_cases = today_top_10_countries_data[:, 1] - yester_top_10_countries_data[:, 1]
    # Initialize output_data to be the new data table with countries' cases, deaths and new cases
    output_data = np.c_[today_top_10_countries_data, new_cases]
    """
    The recovery rate is obtained by looking up the latest data 
    and dividing the total number of cases by the number of recovery patients.
    Then multiply the recovery rate by the number of current cases to get the number of people recovered.
    Assume that the recovery rate here is the same as the recovery rate in the website.  
    Reference : https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?%22%20%5Cl%20%22countries
    """
    recovery_rate = np.array([0.77637, 0.98150, 0.96184, 0.81861, 0.87342, 0.97108, 0.92601, 0.92039, 0.97469, 0.96883])
    recovered_num = output_data[:, 1] * recovery_rate
    # Cases = deaths + active cases + recovery
    # Initialize the active num to be cases subtract deaths then subtract recovery
    active_num = output_data[:, 1] - output_data[:, 2] - recovered_num.astype(int)
    # Make output_data to be the new data table with countries' cases, deaths, new cases and active cases
    output_data = np.c_[output_data, active_num]
    # This loop iterate through the top 10 countries data, and print them in different lines
    for i in range(10):
        print(str(output_data[i, 0]) + " - " + "total cases:" + str(output_data[i, 1])
              + " deaths:" + str(output_data[i, 2]) + " new:" + str(output_data[i, 3])
              + " active:" + str(output_data[i, 4]))


def daily_death_and_new_cases():
    """
    Sort the Data in descending order of the date
    report the daily new cases and new death
    the report the weekly new cases and new death
    because we only have 8.16' data we can't know the earlier data,we can't calculate newly increased data of 8.16,
    So I didn't include 8.16 in daily and weekly report
    """
    # use glob to load the filename list
    files = glob.glob("covid-data\*.csv")
    # sort filelist in descending order of the date
    files_sort = sorted(files, reverse=True)
    # Initialize the death and cases num
    previous_death = 0
    previous_newcase = 0
    # Initialize the newdeath and newcases num
    new_death = []
    new_cases = []
    date = []
    # for every file name
    for i in range(len(files_sort)):
        # Get date information
        yy = (files_sort[i][17:21])
        dd = (files_sort[i][14:16])
        mm = (files_sort[i][11:13])
        # read the file use pd
        data = pd.read_csv(files_sort[i])
        # load data to list
        data_lists = data.values.tolist()
        cur_death = 0
        cur_newcase = 0
        # for each file
        for j in range(len(data_lists)):
            # Sum the sum of data in column 7 and sum of  data in column 8
            cur_death += data_lists[j][8]
            cur_newcase += data_lists[j][7]
        # save date
        date.append(yy + "-" + mm + "-" + dd)
        # first day can't get newly increased data
        if i != 0:
            # Subtract yesterday's data from today's data to get the new data
            new_death.append(-cur_death+previous_death)
            new_cases.append(-cur_newcase+previous_newcase)
            # updata data
        previous_death = cur_death

        previous_newcase = cur_newcase
    # print data as the format
    for ik in range(len(date)-1):
        print(date[ik] + " : new cases: " + str(new_cases[ik]) + " new deaths: " + str(new_death[ik]))
    print()
    # first week data
    print("Week "+date[1]+" to "+date[0]+" : new cases: "+str(sum(new_cases[0:2]))+" new deaths: "
          + str(sum(new_death[0:2])))
    iw = 2
    # if the data is in the range, Print a week's  data
    while iw+7 < len(new_death):
        print("Week " + date[iw+6] + " to " + date[iw] + " : new cases: " + str(sum(new_cases[iw:iw+7]))
              + " new deaths: " + str(sum(new_death[iw:iw+7])))
        iw += 7
    # print remain data
    print("Week "+date[iw+5]+" to "+date[iw]+" : new cases: "+str(sum(new_cases[iw:iw+6]))+" new deaths: "
          + str(sum(new_death[iw:iw+6])))


def get_incident_rate_and_case_fatality_ratio(path_to_files):
    """
    This function have the path of file as input, from the most recent file to 
    report the incident rate and case fatality ratio of the top 10 country region 
    with the highest incident rate. Assume all the region and province in the same 
    country region have almost the same population.
    """
    # call the find_most_recent_data function to get the most recent file
    most_recent = find_most_recent_data(path_to_files)
    file = os.path.join(path_to_files, most_recent)

    df = pd.read_csv(file)
    # use groupby to build a new dataframe by calculating the mean incident rate for
    # each Country Region (assume all the region in the same country have similar amount of people)
    incident_rate_df = df.groupby('Country_Region').agg({'Incident_Rate': 'mean'})
    sum_of_death_df = df.iloc[:, [3, 8]].groupby('Country_Region').sum()
    sum_of_confirmed_df = df.iloc[:, [3, 7]].groupby('Country_Region').sum()
    # calculating the case fatality ration and add it to the origin dataframe
    case_fatality_ratio_df = 100*(sum_of_death_df['Deaths']/sum_of_confirmed_df['Confirmed'])
    incident_rate_df['Case_Fatality_Ratio'] = case_fatality_ratio_df
    # sorting the result fataframe by descending order of incident rate and list the top 10 country region
    result_df = incident_rate_df.sort_values('Incident_Rate', ascending=False).head(10)
    for index in result_df.itertuples():
        print('{} : {} cases per 100,000 people and case-fatality ratio: {} %'.format(index[0], index[1], index[2]))

# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.


if __name__ == '__main__':
    # test on folder containg all CSV files
    analyse('./covid-data')
