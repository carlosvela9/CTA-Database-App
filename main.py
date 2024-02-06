##################################
# Program 1: CTA Database app
# Course: CS 342, Spring 2024 UIC
# System: Codio
# Author: Carlos Velasquez, starter code provided by Ellen Kidane

import sqlite3
import matplotlib.pyplot as plt

###########################################
# Print Stats - Given a connection to the CTA 
# database, executes various SQL queries to 
# retrieve and output basic stats.
###########################################
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()
    dbCursor3 = dbConn.cursor()
    dbCursor4 = dbConn.cursor()
    dbCursor5 = dbConn.cursor()
    dbCursor6 = dbConn.cursor()
    
    print("General Statistics:")
    
    dbCursor.execute("Select count(*) From Stations")
    dbCursor2.execute("Select count(*) From Stops")
    dbCursor3.execute("Select count(*) From Ridership")
    dbCursor4.execute("Select Date(Ride_Date) From Ridership Order By Ride_Date Asc Limit 1")
    dbCursor5.execute("Select Date(Ride_Date) From Ridership Order By Ride_Date Desc Limit 1")
    dbCursor6.execute("Select Sum(Num_Riders) From Ridership")

    row = dbCursor.fetchone()
    row2 = dbCursor2.fetchone()
    row3 = dbCursor3.fetchone()
    row4 = dbCursor4.fetchone()
    row5 = dbCursor5.fetchone()
    row6 = dbCursor6.fetchone()

    print("  # of stations:", f"{row[0]:,}")
    print("  # of stops:", f"{row2[0]:,}")
    print("  # of ride entries:", f"{row3[0]:,}")
    print("  date range: " + row4[0] + " - " + row5[0])
    print("  Total ridership:", f"{row6[0]:,}")
    print()

###########################################
# Command 1 - Finds all the station names 
# that match the user input
###########################################
def command1(dbConn):
    dbCursor = dbConn.cursor()

    print()
    stationName = input("Enter partial station name (wildcards _ and %): ")

    sql = """
           SELECT Station_ID, Station_Name
           FROM Stations
           WHERE Station_Name LIKE ?
           ORDER BY Station_Name ASC
          """

    dbCursor.execute(sql, [stationName])
    result = dbCursor.fetchall()

    if result == []:
        print("**No stations found...")
    else:
        for row in result:
            print(row[0], ":", row[1])
    print()

###########################################
# Command 2 - Finds the percentage of riders
# on weekdays, Saturdays, and Sundays/holidays
# based on the station from user input
###########################################
def command2(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()
    dbCursor3 = dbConn.cursor()
    dbCursor4 = dbConn.cursor()
    dbCursor5 = dbConn.cursor()

    print()
    stationName = input("Enter the name of the station you would like to analyze: ")

    sql = """
           SELECT Station_Name
           FROM Stations
           WHERE Station_Name = ?
          """

    sql2 = """
           SELECT SUM(Num_Riders)
           FROM Ridership
           JOIN Stations ON Stations.Station_ID = Ridership.Station_ID
           WHERE Station_Name = ? AND Type_of_Day = 'W'
          """
    
    sql3 = """
            SELECT SUM(Num_Riders)
            FROM Ridership
            JOIN Stations ON Stations.Station_ID = Ridership.Station_ID
            WHERE Station_Name = ? AND Type_of_Day = 'A'
           """
    
    sql4 = """
            SELECT SUM(Num_Riders)
            FROM Ridership
            JOIN Stations ON Stations.Station_ID = Ridership.Station_ID
            WHERE Station_Name = ? AND Type_of_Day = 'U'
           """
    
    sql5 = """
            SELECT SUM(Num_Riders)
            FROM Ridership
            JOIN Stations ON Stations.Station_ID = Ridership.Station_ID
            WHERE Station_Name = ?
           """

    dbCursor.execute(sql, [stationName])
    result = dbCursor.fetchall()

    if result == []:
        print("**No data found...")
        print()
    else:
        dbCursor2.execute(sql2, [stationName])
        dbCursor3.execute(sql3, [stationName])
        dbCursor4.execute(sql4, [stationName])
        dbCursor5.execute(sql5, [stationName])

        result = dbCursor2.fetchone()
        result2 = dbCursor3.fetchone()
        result3 = dbCursor4.fetchone()
        result4 = dbCursor5.fetchone()

        #Calculate percentages for weekdays/Saturdays/Sundays and holidays
        percentage = result[0] / result4[0] * 100
        percentage2 = result2[0] / result4[0] * 100
        percentage3 = result3[0] / result4[0] * 100

        print("Percentage of ridership for the " + stationName +  " station: ")
        print("  Weekday ridership:", f"{result[0]:,}", f"({percentage:.2f}%)")
        print("  Saturday ridership:", f"{result2[0]:,}", f"({percentage2:.2f}%)")
        print("  Sunday/holiday ridership:", f"{result3[0]:,}", f"({percentage3:.2f}%)")
        print("  Total ridership:", f"{result4[0]:,}")
        print()

###########################################
# Command 3 - Outputs the total ridership
# on weekdays for each station
###########################################
def command3(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()
    
    sql = """
           SELECT Station_Name, SUM(Num_Riders) 
           FROM Ridership
           JOIN Stations ON Stations.Station_ID = Ridership.Station_ID
           WHERE Type_of_Day = 'W'
           GROUP BY Station_Name
           ORDER BY SUM(Num_Riders) DESC
          """

    sql2 = """
            SELECT SUM(Num_Riders)
            FROM Ridership
            WHERE Type_of_Day = 'W'
           """
    
    dbCursor.execute(sql)
    dbCursor2.execute(sql2)

    result = dbCursor.fetchall()
    result2 = dbCursor2.fetchone()

    print("Ridership on Weekdays for Each Station")
    for row in result:
        percentage = row[1] / result2[0] * 100 
        print(row[0], ":", f"{row[1]:,}", f"({percentage:.2f}%)")
    print()

###########################################
# Command 4 - Outputs all the stops and handicap
# accessibility for that stop based on line color
# and direction given from user input
###########################################
def command4(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()

    print()
    lineColor = input("Enter a line color (e.g. Red or Yellow): ")

    sql = """
           SELECT Color 
           FROM Lines
           WHERE Color LIKE ?
          """

    sql2 = """
            SELECT Stop_Name, Direction, ADA
            FROM Stops
            JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
            JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID
            WHERE Color LIKE ? AND Direction LIKE ?
            ORDER BY Stop_Name ASC
           """

    dbCursor.execute(sql, [lineColor])
    result = dbCursor.fetchall()

    if result == []:
        print("**No such line...")
    else:
        direction = input("Enter a direction (N/S/W/E): ")
        
        dbCursor2.execute(sql2, [lineColor, direction])
        result2 = dbCursor2.fetchall()

        if result2 == []:
            print("**That line does not run in the direction chosen...")
        else:
            #Determines handicap accessibility for each station
            for row in result2:
                if row[2] == 1:
                    print(row[0], ": direction =", row[1], "(handicap accessible)")
                else:
                    print(row[0], ": direction =", row[1], "(not handicap accessible)")
    print()

###########################################
# Command 5 - Outputs the number of stops 
# for each line color by direction
###########################################
def command5(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()

    sql = """
           SELECT Color, Direction, COUNT(*)
           FROM Stops
           JOIN StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
           JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID
           GROUP BY Color, Direction
           ORDER BY Color ASC, Direction ASC
          """

    sql2 = """
            SELECT COUNT(*)
            FROM Stops
           """
    
    dbCursor.execute(sql)
    dbCursor2.execute(sql2)

    result = dbCursor.fetchall()
    result2 = dbCursor2.fetchone()

    print("Number of Stops For Each Color By Direction")
    for row in result:
        percentage = row[2] / result2[0] * 100
        print(row[0], "going", row[1], ":", f"{row[2]:,}", f"({percentage:.2f}%)")
    print()

###########################################
# Command 6 - Outputs the total ridership
# for each year for that station provided
# by user input. Gives an option to plot
# the ridership for each year
###########################################
def command6(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()
    dbCursor3 = dbConn.cursor()

    print()
    stationName = input("Enter a station name (wildcards _ and %): ")

    sql = """
           SELECT Station_Name
           FROM Stations
           WHERE Station_Name LIKE ?
          """

    sql2 = """
            SELECT strftime('%Y', Ride_Date) AS Year, SUM(Num_Riders)
            FROM Ridership
            JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
            WHERE Station_Name LIKE ? 
            GROUP BY Year
            ORDER BY Year ASC
           """

    dbCursor.execute(sql, [stationName])
    result = dbCursor.fetchall()

    if result == []:
        print("**No station found...")
    elif len(result) > 1:
        print("**Multiple stations found...")
    else:
        dbCursor2.execute(sql2, [stationName])
        dbCursor3.execute(sql, [stationName])

        result2 = dbCursor2.fetchall()
        result3 = dbCursor3.fetchone()

        print("Yearly Ridership at " + result3[0])
        for row in result2:
            print(row[0], ":", f"{row[1]:,}")
        print()

        plot = input("Plot? (y/n) ") #Option to plot

        if plot == "y":
            #Empty arrays to populate x, y coordinates 
            x = []
            y = []

            for row in result2:
                x.append(row[0])
                y.append(row[1])

            plt.xlabel("Year")
            plt.ylabel("Number of Riders")
            plt.title("Yearly Ridership at " + result3[0] + " Station")
            plt.ioff()
            plt.plot(x, y)
            plt.show()
    print()

###########################################
# Command 7 - Outputs the total ridership
# for each month for a specified station
# and specified year given from user input.
# Gives an option to plot
###########################################
def command7(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()
    dbCursor3 = dbConn.cursor()
    
    print()
    stationName = input("Enter a station name (wildcards _ and %): ")
    
    sql = """
           SELECT Station_Name
           FROM Stations
           WHERE Station_Name LIKE ?
          """

    sql2 = """
            SELECT strftime('%m/%Y', Ride_Date) AS Month, strftime('%Y', Ride_Date) AS Year, SUM(Num_Riders), strftime('%m', Ride_Date)
            FROM Ridership
            JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
            WHERE Station_Name LIKE ? AND Year = ?
            GROUP BY Month
           """

    dbCursor.execute(sql, [stationName])
    result = dbCursor.fetchall()

    if result == []:
        print("**No station found...")
    elif len(result) > 1:
        print("**Multiple stations found...")
    else:
        year = input("Enter a year: ")

        dbCursor2.execute(sql2, [stationName, year])
        dbCursor3.execute(sql, [stationName])

        result2 = dbCursor2.fetchall()
        result3 = dbCursor3.fetchone()

        print("Monthly Ridership at " + result3[0] + " for " + year)
        for row in result2:
            print(row[0], ":", f"{row[2]:,}")
        print()

        plot = input("Plot? (y/n) ")

        if plot == "y":
            x = []
            y = []

            for row in result2:
                x.append(row[3])
                y.append(row[2])

            plt.xlabel("Month")
            plt.ylabel("Number of Riders")
            plt.title("Monthly Ridership at " + result3[0] + " Station " + "(" + year + ")")
            plt.ioff()
            plt.plot(x, y)
            plt.show()
    print()

###########################################
# Command 8 - Outputs the total ridership
# for the first 5 days and last 5 days of 
# a specified year for 2 specified stations
# given from user input. Gives an option to plot 
###########################################
def command8(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor2 = dbConn.cursor()
    dbCursor3 = dbConn.cursor()
    dbCursor4 = dbConn.cursor()
    dbCursor5 = dbConn.cursor()
    dbCursor6 = dbConn.cursor()
    dbCursor7 = dbConn.cursor()
    dbCursor8 = dbConn.cursor()
    dbCursor9 = dbConn.cursor()
    dbCursor10 = dbConn.cursor()
    
    print()
    year = input("Year to compare against? ")
    print()
    stationName = input("Enter station 1 (wildcards _ and %): ")

    sql = """
           SELECT Station_Name
           FROM Stations
           WHERE Station_Name LIKE ?
          """

    sql2 = """
            SELECT Station_ID, Station_Name
            FROM Stations
            WHERE Station_Name LIKE ?
           """

    sql3 = """
            SELECT DATE(Ride_Date), SUM(Num_Riders)
            FROM Ridership
            JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
            WHERE Station_Name LIKE ? AND strftime('%Y', Ride_Date) LIKE ?
            GROUP BY DATE(Ride_Date)
            ORDER BY DATE(Ride_Date) ASC
            LIMIT 5
           """

    sql4 = """
            SELECT DATE(Ride_Date), SUM(Num_Riders)
            FROM Ridership
            JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
            WHERE Station_Name LIKE ? AND strftime('%Y', Ride_Date) LIKE ?
            GROUP BY DATE(Ride_Date)
            ORDER BY DATE(Ride_Date) DESC
            LIMIT 5
           """

    sql5 = """
            SELECT DATE(Ride_Date), SUM(Num_Riders)
            FROM Ridership
            JOIN Stations ON Ridership.Station_ID = Stations.Station_ID
            WHERE Station_Name LIKE ? AND strftime('%Y', Ride_Date) LIKE ?
            GROUP BY DATE(Ride_Date)
            ORDER BY DATE(Ride_Date) ASC
           """

    dbCursor.execute(sql, [stationName])
    result = dbCursor.fetchall()

    if result == []:
        print("**No station found...")
    elif len(result) > 1:
        print("**Multiple stations found...")
    else:
        print()
        stationName2 = input("Enter station 2 (wildcards _ and %): ")

        dbCursor2.execute(sql, [stationName2])
        result2 = dbCursor2.fetchall()

        if result2 == []:
            print("**No station found...")
        elif len(result2) > 1:
            print("**Multiple stations found...")
        else:
            dbCursor3.execute(sql2, [stationName])
            dbCursor4.execute(sql3, [stationName, year])
            dbCursor5.execute(sql4, [stationName, year])
            dbCursor6.execute(sql2, [stationName2])
            dbCursor7.execute(sql3, [stationName2, year])
            dbCursor8.execute(sql4, [stationName2, year])
            dbCursor9.execute(sql5, [stationName, year])
            dbCursor10.execute(sql5, [stationName2, year])
            
            result3 = dbCursor3.fetchone()
            result4 = dbCursor4.fetchall()
            result5 = dbCursor5.fetchall()
            result6 = dbCursor6.fetchone()
            result7 = dbCursor7.fetchall()
            result8 = dbCursor8.fetchall()
            result9 = dbCursor9.fetchall()
            result10 = dbCursor10.fetchall()

            #Prints last 5 and first 5 days of total ridership for that day for station 1
            print("Station 1:", result3[0], result3[1])
            for row in result4:
                print(row[0], row[1])
            for row in reversed(result5):
                print(row[0], row[1])

            #Prints last 5 and first 5 days of total ridership for that day for station 2
            print("Station 2:", result6[0], result6[1])
            for row in result7:
                print(row[0], row[1])
            for row in reversed(result8):
                print(row[0], row[1])
            print()

            plot = input("Plot? (y/n) ")

            if plot == "y":
                ax = plt.axes() #Used to modify the x ticks of the graph

                x = []
                x2 = []
                y = []
                y2 = []

                #Coordinates for station 1
                for row in result9:
                    x.append(row[0])
                    y.append(row[1])
                #Coordinates for station 2
                for row in result10:
                    x2.append(row[0])
                    y2.append(row[1])

                plt.xlabel("Day")
                plt.ylabel("Number of Riders")
                plt.title("Ridership Each Day of " + year)
                plt.ioff()
                plt.plot(x, y)
                plt.plot(x2, y2)
                plt.legend([result3[1], result6[1]])
                ax.set_xticks([50, 100, 150, 200, 250, 300, 350])
                ax.set_xticklabels(['50', '100', '150', '200', '250', '300', '350'])
                plt.show() 
    print()

###########################################
# Command 9 - Outputs all stations within a 
# mile square radius given a set of latitude
# and longitude from user input. Gives an 
# option to plot
###########################################
def command9(dbConn):
    dbCursor = dbConn.cursor()

    print()
    latitude = float(input("Enter a latitude: "))

    sql = """
           SELECT Station_Name, Latitude, Longitude
           FROM Stops
           JOIN Stations ON Stops.Station_ID = Stations.Station_ID
           WHERE (Latitude BETWEEN ? AND ?) AND (Longitude BETWEEN ? AND ?)
           GROUP BY Longitude
           ORDER BY Station_Name, Latitude DESC
          """

    if latitude < 40 or latitude > 43:
        print("**Latitude entered is out of bounds...")
    else:
        longitude = float(input("Enter a longitude: "))

        if longitude < -88 or longitude > -87:
            print("**Longitude entered is out of bounds...")
        else:
            mileLatitude = 1 / 69.0 #Degree of latitude
            mileLongitude = 1 / 51.0 #Degree of longitude

            #Calculates the upper and lower bounds for latitude and longitude based on user input
            minimumLatitude = round(latitude - mileLatitude, 3)
            maximumLatitude = round(latitude + mileLatitude, 3)
            minimumLongitude = round(longitude - mileLongitude, 3)
            maximumLongitude = round(longitude + mileLongitude, 3)

            dbCursor.execute(sql, [minimumLatitude, maximumLatitude, minimumLongitude, maximumLongitude])
            result = dbCursor.fetchall()

            if result == []:
                print("**No stations found...")
            else:
                print()
                print("List of Stations Within a Mile")
                for row in result:
                    print(row[0], ": " + "(" + str(row[1]) + ", " + str(row[2]) + ")")
                print()

                plot = input("Plot? (y/n) ")

                if plot == "y":
                    x = []
                    y = []

                    for row in result:
                        x.append(row[2])
                        y.append(row[1])

                    image = plt.imread("chicago.png")
                    xydims = [-87.9277, -87.5569, 41.7012, 42.0868] 
                    
                    plt.imshow(image, extent=xydims)
                    plt.title("Stations Near You")
                    plt.plot(x, y, 'bo')

                    for row in result:
                        plt.annotate(row[0], (row[2], row[1]))

                    plt.xlim([-87.9277, -87.5569])
                    plt.ylim([41.7012, 42.0868])
                    plt.show()
    print()

###########################################
# Main
###########################################
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

validCommands = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "x"] #Array of all valid commands the user can input

command = input("Please enter a command (1-9, x to exit): ")

while command != 'x':
    #Will keep asking the user to enter a command if the command entered is invalid
    while command not in validCommands:
        print("**Error, unknown command, try again...")
        print()

        command = input("Please enter a command (1-9, x to exit): ")

    #All the valid commands in the database app
    while command in validCommands:
        if command == "1":
            command1(dbConn)
        elif command == "2":
            command2(dbConn)
        elif command == "3":
            command3(dbConn)
        elif command == "4":
            command4(dbConn)
        elif command == "5":
            command5(dbConn)
        elif command == "6":
            command6(dbConn)
        elif command == "7":
            command7(dbConn)
        elif command == "8":
            command8(dbConn)
        elif command == "9":
            command9(dbConn)

        command = input("Please enter a command (1-9, x to exit): ")

        #User decides to quit the program
        if command == 'x':
            break