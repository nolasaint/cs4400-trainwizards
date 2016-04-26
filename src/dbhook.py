import pymysql

'''

  dbhook.py

  author:  Evan Bailey
  date:    2016-04-24
  version: 1.3

  This file provides various functions to aide in fetching data from
  the "trainwizards" database. It is part of the 3rd phase of our
  team's (Team 68) project for Spring 2016 CS 4400 at Georgia Tech.

  Notes:
  - setupConnection() must be called before any other functions can be
    used

  - teardownConnection() should be called once the database is no
    longer needed in the program

  Changelog:
  - 1.0: functionality
  - 1.1: documentation fixes
  - 1.2: minor SQL query changes, added checkManager
  - 1.3: added getSID

'''

# Dictionary keys
_TRAINNUM         = "trainNum"
_DEPARTTIME       = "departTime"
_ARRIVETIME       = "arriveTime"
_TRAVELTIME       = "travelTime"
_DEPARTDATE       = "departDate"
_STATIONNAME      = "stationName"
_FIRSTCLASSPRICE  = "firstClassPrice"
_SECONDCLASSPRICE = "secondClassPrice"
_TICKETCLASS      = "ticketClass"
_TICKETPRICE      = "ticketPrice"
_NUMBAGS          = "numBags"
_FIRSTNAME        = "firstName"
_LASTNAME         = "lastName"
_RATING           = "rating"
_COMMENT          = "comment"

# Connection status variables
_connected = False
_connection = None
_cursor = None

# Trainwizards database variables
_host = "academic-mysql.cc.gatech.edu"
_user = "cs4400_Team_68"
_pass = "Glk20Zjm"
_dbse = "cs4400_Team_68"

def _formatTimedelta(timedelta): #{
    hours, remainder = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # TODO maybe change to string.format() lol
    timestr = ""
    
    if hours < 10:
        timestr += "0"
    timestr += str(hours) + ":"
    
    if minutes < 10:
        timestr += "0"
    timestr += str(minutes) + ":"

    if seconds < 10:
        timestr += "0"
    timestr += str(seconds)
    
    return timestr
#}


#
# Attempts to connect to the database.
#
# Returns True if a connection was established, False otherwise
#
def setupConnection(): #{
    global _connected
    global _connection
    global _cursor
    
    if not _connected:
        # Try to connect to the database
        try:
            _connection = pymysql.connect(host = _host, user = _user, passwd = _pass, db = _dbse)
            _cursor = _connection.cursor()
            _connected = True
        except:
            _connected = False
    
    return _connected
#}

#
# Closes the connection to the database.
#
def teardownConnection(): #{
    global _connected

    if _connected:
        _connection.close()
        _connected = False
#}


# function: checkLogin(cursor, username, password)
#
# Determines if the provided login information is valid.
#
# Returns True if the login information is correct, False otherwise
# --------------------------------------
def checkLogin(username, password): #{
    sql = "SELECT username, password FROM User WHERE username = %s AND "\
          "password = %s;"
    replies = _cursor.execute(sql, (username, password))

    # Clear cursor
    _cursor.fetchall()
    
    return replies > 0
#}


# function: checkManager(username)
#
# Determines if the specified user is a manager.
#
# Returns True if the login information is correct, False otherwise
# --------------------------------------
def checkManager(username): #{
    sql = "SELECT mUsername FROM Manager WHERE mUsername = %s;"
    replies = _cursor.execute(sql, (username))

    # Clear cursor
    _cursor.fetchall()
    
    return replies > 0
#}


# function: checkIfCardowner(username, cardNumber)
#
# Determines if the specified user owns the specified card.
#
# Note: cardNumber must be a string
#
# Returns True if the user owns the card, False otherwise
# --------------------------------------
def checkIfCardowner(username, cardNumber): #{
    sql = "SELECT * FROM Owns WHERE cardNum = %s AND username = %s;"
    replies = _cursor.execute(sql, (cardNumber, username))
    
    # Clear cursor
    _cursor.fetchall()
    
    return replies > 0
#}


# function: getSchedule(trainNum)
#
# Retrieves information about the departure schedule for the specified train.
#
# Returns a list of dictionaries with the following key-value scheme:
#     'trainNum':    [int] the train's ID numer
#     'departTime':  [str] the time (HH:MM:SS) the train will depart
#     'arriveTime':  [str] the time (HH:MM:SS) the train will arrive
#     'stationName': [str] the name of the destination station
# --------------------------------------
def getSchedule(trainNum): #{
    sql = "SELECT rtrainNum, departTime, arriveTime, name FROM Route INNER "\
          "JOIN Station ON Route.sourceSID=Station.SID WHERE rtrainNum = %s;"
    replies = _cursor.execute(sql, (trainNum))
    retval = []
    
    for i in range(replies): #{
        reply = _cursor.fetchone()

        rDict = {}
        rDict[_TRAINNUM]    = reply[0]
        rDict[_DEPARTTIME]  = _formatTimedelta(reply[1])
        rDict[_ARRIVETIME]  = _formatTimedelta(reply[2])
        rDict[_STATIONNAME] = reply[3]
        
        retval.append(rDict)
    #}
    return retval
#}


# function: getDepartures(sourceSID, destSID)
#
# Retrieves information about all trains that travel along the specified route.
#
# Returns a list of dictionaries with the following key-value scheme:
#     'trainNum':         [int] the train's ID number
#     'departTime':       [str] the time (HH:MM:SS) the train will depart
#     'arriveTime':       [str] the time (HH:MM:SS) the train will arrive
#     'travelTime':       [str] the time (HH:MM:SS) the trip will take
#     'firstClassPrice':  [flo] the price for a 1st-class seat
#     'secondClassPrice': [flo] the price for a 2nd-class seat
# --------------------------------------
def getDepartures(sourceSID, destSID): #{
    sql = "SELECT trainNum, MIN( departTime ) , MAX( arriveTime ) , "\
          "TIMEDIFF( MAX( arriveTime ) , MIN( departTime ) ) , "\
          "firstClassPrice, secondClassPrice FROM Train INNER JOIN Route "\
          "ON Train.trainNum = Route.rTrainNum WHERE  TrainNum IN ( SELECT "\
          "rTrainNum FROM Route WHERE sourceSID = %s ) AND rTrainNum IN ( "\
          "SELECT rTrainNum FROM Route WHERE destSID = %s ) GROUP BY trainNum;"
    replies = _cursor.execute(sql, (sourceSID, destSID))
    retval = []
    
    for i in range(replies): #{
        reply = _cursor.fetchone()
        
        rDict = {}
        rDict[_TRAINNUM]   = reply[0]
        rDict[_DEPARTTIME] = _formatTimedelta(reply[1])
        rDict[_ARRIVETIME] = _formatTimedelta(reply[2])
        rDict[_TRAVELTIME] = _formatTimedelta(reply[3])
        rDict[_FIRSTCLASSPRICE]  = float(reply[4])
        rDict[_SECONDCLASSPRICE] = float(reply[5])
        
        retval.append(rDict)
    #}
    return retval
#}


# function: getTickets(reservationID)
#
# Retrieves information about all tickets that are part of the specified
# reservation.
#
# Returns a list of dictionaries with the following key-value scheme:
#     'trainNum':    [int] the train's ID number
#     'departTime':  [str] the time (HH:MM:SS) the train will depart
#     'arriveTime':  [str] the time (HH:MM:SS) the train will arrive
#     'travelTime':  [str] the time (HH:MM:SS) the trip will take
#     'departDate':  [str] the date (B d, Y) the trip will occur on
#     'ticketClass': [int] 1 = 1st class, 2 = 2nd class
#     'ticketPrice': [flo] the total cost of the ticket
#     'numBags':     [int] the number of bags the passenger will be carrying
#     'firstName':   [str] the passenger's first name
#     'lastName':    [str] the passenger's last name
# --------------------------------------
def getTickets(reservationID): #{
    sql = "SELECT t1.tTrainNum, t2.departTime, t2.arriveTime, timeDiff("\
          "t2.arriveTime, t2.departTime), t1.departureDate, t1.class, "\
          "t1.Price, t1.numbags, t1.fName, t1.lName FROM (SELECT fNAME, "\
          "lNAME, departureDate, class, numbags, Price, tTrainNum FROM "\
          "Ticket WHERE tReservationID=%s) as t1 JOIN (SELECT MIN("\
          "departTime) AS departTime, MAX(arriveTime) AS arriveTime, "\
          "rTrainNum FROM Route WHERE rTrainNum IN (SELECT tTrainNum FROM "\
          "Ticket WHERE tReservationID=%s) AND (sourceSID IN (SELECT "\
          "tSourceSID FROM Ticket WHERE tReservationID=%s) OR destSID "\
          "IN (SELECT tdestSID FROM Ticket WHERE tReservationID=%s))) "\
          "AS t2 ON t1.tTrainNum=t2.rTrainNum;"
    replies = _cursor.execute(sql, (reservationID, reservationID, reservationID, reservationID))
    retval = []
    
    for i in range(replies): #{
        reply = _cursor.fetchone()
        
        rDict = {}
        rDict[_TRAINNUM]    = reply[0]
        rDict[_DEPARTTIME]  = _formatTimedelta(reply[1])
        rDict[_ARRIVETIME]  = _formatTimedelta(reply[2])
        rDict[_TRAVELTIME]  = _formatTimedelta(reply[3])
        rDict[_DEPARTDATE]  = reply[4].strftime("%B %d, %Y")
        rDict[_TICKETCLASS] = int(reply[5])
        rDict[_TICKETPRICE] = float(reply[6])
        rDict[_NUMBAGS]     = int(reply[7])
        rDict[_FIRSTNAME]   = reply[8]
        rDict[_LASTNAME]    = reply[9]
        
        retval.append(rDict)
    #}

    return retval
#}


# function: getReviews(trainNum)
#
# Retrieves a list of reviews for the specified train.
#
# Returns a list of dictionaries with the following key-value scheme:
#     'rating':  [flo] the numerical rating (out of 10)
#     'comment': [str] the customer's comments about the train
# --------------------------------------
def getReviews(trainNum): #{
    sql = "SELECT rating, Comment FROM Review WHERE rvTrainNumber=%s;"
    replies = _cursor.execute(sql, (trainNum))
    retval = []
    
    for i in range(replies): #{
        reply = _cursor.fetchone()
        
        rDict = {}
        rDict[_RATING]  = int(reply[0])
        rDict[_COMMENT] = reply[1]
        
        retval.append(rDict)
    #}
    
    return retval
#}


# function: getTotalCost(reservationID)
#
# Retrieves the total cost of the specified reservation.
#
# Returns the total cost (as a float), or 0.0 if no reservation was found
# --------------------------------------
def getTotalCost(reservationID): #{
    sql = "SELECT totalCost FROM Reservation WHERE reservationID=%s;"
    replies = _cursor.execute(sql, (reservationID))
    retval = float(0)
    
    if replies > 0: #{
        retval = float(_cursor.fetchone()[0])
    #}

    # Sanity check
    _cursor.fetchall()
    
    return retval
#}


# function: getPopularRoutes(num)
#
# Retrieves the $num routes in each month with the most reservations.
#
# Returns a list of 12 lists, populated by tuples with the following scheme:
#     (trainNum, numReservations)
# --------------------------------------
def getPopularRoutes(num): #{
    sql = "SELECT Month(departureDate) AS Month, tTrainNum, "\
          "COUNT(tReservationID) FROM Ticket INNER JOIN Reservation ON "\
          "Ticket.tReservationID = Reservation.reservationID WHERE "\
          "isCancelled = 0 GROUP BY Month, tTrainNum ORDER BY Month;"
    replies = _cursor.execute(sql)
    retval = [[] for i in range(12)] # makes a list of 12 lists
    months = [[] for i in range(12)]
    
    # Populate month buckets
    for i in range(replies): #{
        reply = _cursor.fetchone()
        months[reply[0]].append((reply[1], reply[2]))
    #}
    
    m = 0
    # Sort each month bucket
    for month in months: #{
        month.sort(key=lambda x: -x[1])
        
        count = 0
        # Select at most the first $num elements of each month
        while count < min(num, len(month)): #{
            retval[m].append(month[count])
            count += 1
        #}
        
        m += 1
    #}
    
    return retval
#}


# function: getRevenueReport()
#
# Retrieves the revenue report based on the current database state.
#
# Note: monthNum starts at 1 and goes to 12
#
# Returns a 3-element list holding tuples with the following format:
#     (monthNum, revenueEarned)
# --------------------------------------
def getRevenueReport(): #{
    sql = "SELECT Month(departureDate) AS Month, SUM(Price) AS Revenue FROM "\
          "Ticket GROUP BY Month ORDER BY Month LIMIT 3;"
    replies = _cursor.execute(sql)
    retval = []
    
    for i in range(replies): #{
        reply = _cursor.fetchone()

        retval.append((reply[0], float(reply[1])))
    #}
    
    return retval
#}


# function: getSID(name)
#
# Retrieves the SID of the specified station
#
# Returns the [int] SID of the station with the specified name
# --------------------------------------
def getSID(name): #{
    sql = "SELECT SID FROM Station WHERE name = %s;"
    replies = _cursor.execute(sql, (name))

    if replies > 0:
      return _cursor.fetchone()[0]
#}


# function: addCustomer(username, password, email)
#
# Adds a new customer to the database.
#
# Note: will cause an exception if the username is not unique
# --------------------------------------
def addCustomer(username, password, email): #{
    sql = "INSERT INTO User VALUES (%s, %s);"
    _cursor.execute(sql, (username, password))
    
    sql = "INSERT INTO Customer (cUsername, email) VALUES (%s, %s);"
    _cursor.execute(sql, (username, email))
    
    _connection.commit()
#}


# function: addReservation(username, cardNumber, totalCost)
#
# Adds a new reservation to the database and returns its ID.
#
# Note: cardNumber must be a string
# Note: totalCost must be numberic
# Note: will cause an exception if the username or cardNumber are not found
#       in the DB
#
# Returns the newly-created reservation's reservationID
# --------------------------------------
def addReservation(username, cardNumber, totalCost): #{
    sql = "INSERT INTO Reservation (totalCost, rUsername, rCardNumber) "\
          "VALUES (%s, %s, %s);"
    _cursor.execute(sql, (totalCost, username, cardNumber))
    _connection.commit()
    
    sql = "SELECT reservationID FROM Reservation WHERE reservationID = "\
          "LAST_INSERT_ID();"
    _cursor.execute(sql)
    
    retval = int(_cursor.fetchone()[0])
    
    # Failsafe
    _cursor.fetchall()
    
    return retval
#}


# function: addTicket(...)
#
# Adds a new ticket to the database.
#
# Note: tClass must be 1 or 2
# Note: departDate must be a string formatted as: "YYYY-MM-DD"
# Note: sourceSID and destSID must be integers
# Note: will cause an exception if the specified reservationID, sourceSID,
#       destSID, or trainNum are not found in the DB
#
# Returns the newly-created ticket's ticketID
# --------------------------------------
def addTicket(reservationID, fName, lName, tClass, numBags, departDate, price, sourceSID, destSID, trainNum): #{
    sql = "INSERT INTO Ticket (fName, lName, class, numBags, departureDate, "\
          "Price, tSourceSID, tDestSID, tTrainNum, tReservationID) VALUES "\
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    _cursor.execute(sql, (fName, lName, tClass, numBags, departDate, price,
                          sourceSID, destSID, trainNum, reservationID))
    _connection.commit()
    
    sql = "SELECT ticketID FROM Ticket WHERE ticketID = LAST_INSERT_ID();"
    _cursor.execute(sql)
    
    retval = int(_cursor.fetchone()[0])
    
    # Failsafe
    _cursor.fetchall()
    
    return retval
#}


# function: addCard(cardNumber, ccv, cardholderName, expireDate)
#
# Adds a new credit card to the database.
#
# Note: cardNumber must be a string
# Note: ccv must be numeric
# Note: expireDate must be a string formatted as: "YYYY-MM-DD"
# Note: will cause an exception if the specified cardNumber already exists
#       in the DB
# --------------------------------------
def addCard(cardNumber, ccv, cardholderName, expireDate): #{
    sql = "INSERT INTO Card (cardNumber, ccv, cardholderName, expireDate) "\
          "VALUES (%s, %s, %s, %s);"
    _cursor.execute(sql, (cardNumber, ccv, cardholderName, expireDate))
    
    _connection.commit()
#}


# function: addReview(trainNum, username, rating, comment)
#
# Adds a new review for the specified train to the database.
#
# Note: rating must be numeric
# Note: will cause an exception if the specified trainNum or username are
#       not found in the DB
# --------------------------------------
def addReview(trainNum, username, rating, comment): #{
    sql = "INSERT INTO Review (userName, rvTrainNumber, rating, Comment) "\
          "VALUES (%s, %s, %s, %s);"
    _cursor.execute(sql, (username, trainNum, rating, comment))
    
    _connection.commit()
#}


# function: setTotalCost(reservationID, totalCost)
#
# Sets the total cost for the specified reservation.
#
# Note: will cause an exception if the specified reservationID is not
#       found in the DB
# --------------------------------------
def setTotalCost(reservationID, totalCost): #{
    sql = "UPDATE Reservation SET totalCost = %s WHERE reservationID=%s;"
    _cursor.execute(sql, (totalCost, reservationID))
    
    _connection.commit()
#}


# function: setTicketDate(reservationID, ticketID, departureDate)
#
# Sets the specified ticket's departure date to departureDate.
#
# Note: departureDate must be a string formatted as "YYYY-MM-DD"
# Note: will cause an exception if the specified reservationID or ticketID
#       are not found in the DB
# --------------------------------------
def setTicketDate(reservationID, ticketID, departureDate): #{
    sql = "UPDATE Ticket SET departureDate=%s WHERE tReservationID=%s AND "\
          "ticketID=%s;"
    _cursor.execute(sql, (departureDate, reservationID, ticketID))
    
    _connection.commit()
#}


# function: setCancelled(reservationID)
#
# Sets the specified reservation as cancelled.
#
# Note: will cause an exception if the specified reservationID is not found
#       in the DB
# --------------------------------------
def setCancelled(reservationID): #{
    sql = "UPDATE Reservation SET isCancelled = 1, cancellationDate = "\
          "DATE_FORMAT(NOW(), '%m/%d/%Y') WHERE reservationID = %s;"
    _cursor.execute(sql, (reservationID))
    
    _connection.commit()
#}


# function: setOwnership(username, cardNumber)
#
# Sets the specified customer as owning the specified credit card.
#
# Note: cardNumber must be a string
# Note: will cause an exception if the specified username or cardNumber is
#       not found in the DB
# --------------------------------------
def setOwnership(username, cardNumber): #{
    sql = "INSERT INTO Owns (username, cardNum) VALUES (%s, %s);"
    _cursor.execute(sql, (username, cardNumber))
    
    _connection.commit()
#}


# function: setStudent(username)
#
# Sets the specified customer as a student.
#
# Note: will cause an exception if the specified username is not found in
#       the DB
# --------------------------------------
def setStudent(username): #{
    sql = "UPDATE Customer SET isStudent = 1 WHERE cUsername=%s;"
    _cursor.execute(sql, (username))
    
    _connection.commit()
#}


# function: deleteCard(cardNumber)
#
# Deletes the specified credit card from the database.
#
# Note: cardNumber must be a string
# Note: will cause an exception if the specified cardNumber is not found in
#       the DB
# --------------------------------------
def deleteCard(cardNumber): #{
    sql = "DELETE cardNumber FROM Card WHERE cardNumber = %s;"
    _cursor.execute(sql, (cardNumber))
    
    _connection.commit()
#}
