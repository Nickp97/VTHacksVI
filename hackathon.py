################################################
# This Code written for VT Hacks Hackathon VI. #
#                                              #
# This code base makes use of the Capital One  #
# Nessie API used for hackathons.              #
#                                              #
# @version: 15 - 17 February 2018              #
# @author: Lance E. Church                     #
################################################

# This is written for PYTHON 3
# Don't forget to install requests package
import requests
import json
import csv
import random

###################
# API Page Class #
##################

class Page:
  ################################
  # Class documentation String   #
  # Accessed via: Page.__doc__ #
  ################################
  'A record of all pages provided by the Capital One API'

  ################################
  # Class field (data) variables #
  ################################
  page_count = 0
  pages = []

  ###############
  # Constructor #
  ###############

  # Make a page entity that can be added to the list of all pages visited
  def __init__(self, pageURL):
    self.pageString = pageURL
    self.addPage()

  #############
  # Functions #
  #############

  # Adds an API page to the list of all pages
  def addPage(self):
    Page.page_count += 1
    Page.pages.append(self)

  # Displays the number of entries in the page list
  @staticmethod
  def countPagesDisplay():
    print(str(Page.page_count))

  # Displays the list of all API pages stored
  @staticmethod
  def listPagesDisplay():
    counter = 1
    for x in Page.pages:
      if counter < 10:
        print(counter, " : ", x.pageString)
      else:
        print(counter, ": ", x.pageString)

      counter += 1
# End Entity class documentation

#########################
# Business Entity Class #
#########################

class Entity:
  ################################
  # Class documentation String   #
  # Accessed via: Entity.__doc__ #
  ################################
  'Common base class for all business entities in the Capital One API database.'

  ################################
  # Class field (data) variables #
  ################################
  entity_count = 0
  data_entities = []

  ###############
  # Constructor #
  ###############

  # Sets instance variable values
  def __init__(self, _id, name, geocode, accessibility, hours, address, language_list, amount_left):
    Entity.entity_count += 1

    self.entity_count = Entity.entity_count

    self.account_id_number = _id
    self.name = name
    self.geography_longitude = geocode['lng']
    self.geography_latitude = geocode['lat']
    self.accessibility = accessibility
    self.hours = hours
    self.address_street_number = address['street_number']
    self.address_street_name = address['street_name']
    self.address_city = address['city']
    self.address_zip = address['zip']
    self.address_state = address['state']
    self.languages = language_list
    self.account_balance = amount_left
    self.formatted_account_balance = '${:,.2f}'.format(self.account_balance)

    self.street_address = self.address_street_number + " " + self.address_street_name
    self.city_address = self.address_city + ", " + self.address_state + " " + self.address_zip

    self.allDataAsArray = [str(self.entity_count), str(self.account_id_number), self.name ,str(self.geography_longitude), str(self.geography_latitude), str(self.accessibility), str(self.hours), self.street_address, self.address_city, self.address_state, str(self.address_zip), str(self.languages), self.account_balance]

    # Will append time period, deposits, withdrawels, new balance
    # to the end of the data array and data string repeatedly for all
    # time periods in simulation
    self.timePeriod = []
    self.deposits = []
    self.withdrawels = []
    self.earnings = []

  #############
  # Functions #
  #############

  # Need getter / setter things (maybe?)
  # Need data manipulators
  # Need data classifiers
  # Already have a lot of display functions, maybe too many

  # Used to update the array with the data after the simulation has been run
  def updateAllDataAsArray(self):
    length = 0
    while length < len(self.timePeriod):
      self.allDataAsArray.append(self.timePeriod[length])
      self.allDataAsArray.append(self.deposits[length])
      self.allDataAsArray.append(self.withdrawels[length])
      self.allDataAsArray.append(self.earnings[length])
      length += 1

  # Conditions based upon company wealth.
  # lower: < $100,000, low: $100,000 - $250,000, middle: $250,001 - $750,000, upper: $750,001 - $5,000,000, top: > $5,000,000
  def economicSituation(self, timePeriod):
    # seven random factors to represent ~14% of company growth/decline each time
    firstCond = random.randint(0,15)
    secondCond = random.randint(0,15)
    thirdCond = random.randint(0,15)
    fourthCond = random.randint(0,15)
    fifthCond = random.randint(0,15)
    sixthCond = random.randint(0,15)
    seventhCond = random.randint(0,15)
    depositConditions = firstCond + secondCond + thirdCond + fourthCond + fifthCond + sixthCond + seventhCond + 2

    firstCond = random.randint(0,15)
    secondCond = random.randint(0,15)
    thirdCond = random.randint(0,15)
    fourthCond = random.randint(0,15)
    fifthCond = random.randint(0,15)
    sixthCond = random.randint(0,15)
    seventhCond = random.randint(0,15)
    withdrawelConditions = firstCond + secondCond + thirdCond + fourthCond + fifthCond + sixthCond + seventhCond + 2

    depositAmount = 0
    withdrawelAmount = 0
    earnings = 0
    newBalance = 0

    # If simulation has not run yet for a single period
    if len(self.earnings) == 0:
      if self.account_balance < 100000:
        depositAmount = (depositConditions / 100) * 20000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 20000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.account_balance + earnings
      elif self.account_balance < 250000:
        depositAmount = (depositConditions / 100) * 40000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 40000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.account_balance + earnings
      elif self.account_balance < 750000:
        depositAmount = (depositConditions / 100) * 100000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 100000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.account_balance + earnings
      elif self.account_balance < 5000000:
        depositAmount = (depositConditions / 100) * 150000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 150000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.account_balance + earnings
      else:
        depositAmount = (depositConditions / 100) * 200000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 200000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.account_balance + earnings

    # for when simulation has run for at least one time period
    else:
      if self.earnings[len(self.earnings) - 1] < 100000:
        depositAmount = (depositConditions / 100) * 20000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 20000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.earnings[len(self.earnings) - 1] + earnings
      elif self.earnings[len(self.earnings) - 1] < 250000:
        depositAmount = (depositConditions / 100) * 40000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 40000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.earnings[len(self.earnings) - 1] + earnings
      elif self.earnings[len(self.earnings) - 1] < 750000:
        depositAmount = (depositConditions / 100) * 100000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 100000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.earnings[len(self.earnings) - 1] + earnings
      elif self.earnings[len(self.earnings) - 1] < 5000000:
        depositAmount = (depositConditions / 100) * 150000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 150000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.earnings[len(self.earnings) - 1] + earnings
      else:
        depositAmount = (depositConditions / 100) * 200000
        withdrawelAmount = (1 - (withdrawelConditions / 100)) * 200000
        earnings = depositAmount - withdrawelAmount
        newBalance = self.earnings[len(self.earnings) - 1] + earnings

    # record the results of a time period to the appropriate results array
    self.timePeriod.append(timePeriod)
    self.deposits.append(depositAmount)
    self.withdrawels.append(withdrawelAmount)
    self.earnings.append(newBalance)


  # Return the entity as a string
  def getAllAsString(self):
    theString = ''
    length = 0
    for x in self.allDataAsArray:
      if length < len(self.allDataAsArray) - 1:
        theString += (str(x) + ', ')
        length += 1
      else:
        theString += (str(x))
    return theString

  # Return the entity as an array
  def getAllAsArray(self):
    return self.allDataAsArray

  # Displays all of the data of an entity as a single string with commas used to seperate out different fields.
  def displayAll(self):
    print(self.allDataAsString)

  # Displays the total number of instances of the entity class that currently exist
  def displayEntityCount(self):
    print ("Total Entities: " + Entity.entity_count)

  # Displays the address of the provided entity
  def displayAddress(self):
    print ("Address:\n\t" + self.street_address + "\n\t" + self.city_address)

  # Displays the address with no leading "Address: " statement
  def displayAddressSimple(self):
    print(self.street_address)
    print(self.city_address)

  # Displays the account name of the provided entity
  def displayName(self):
    print("Account Name: " + self.name)

  # Displays the account name  with no leading "Name: " statement
  def displayNameSimple(self):
    print(self.name)

  # Displays the account id number of the provided entity
  def displayAccountNumber(self):
    print("Account ID #: " + self.account_id_number)

  # Displays the account id number with no leading "Account ID #: " statement
  def displayAccountNumberSimple(self):
    print(self.account_id_number)

  # Displays the account monetary balance of the provided entity
  def displayAccountBalance(self):
    print("Current Account Balance: " + '${:,.2f}'.format(self.account_balance))

  # Displays the account monetary balance of the provided entity
  def displayAccountBalanceSimple(self):
    print(self.formatted_account_balance)

  def displayEntityBaseInfo(self):
    print('Entity Item: ' + str(self.entity_count))
    self.displayNameSimple()
    self.displayAccountNumberSimple()
    self.displayAddressSimple()
    self.displayAccountBalanceSimple()
# End Entity class documentation

###############
# World Class #
###############

class World:
  ################################
  # Class documentation String   #
  # Accessed via: World.__doc__ #
  ################################
  'Static class used to pass time, create business transactions, force loans, track bank earnings.'

  ################################
  # Class field (data) variables #
  ################################
  months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  dates = ['1  ', '15 ']

  period = None
  monthPosition = 0
  datesPosition = 0
  year = 1

  ###############
  # Constructor #
  ###############

  # class treated as a static class, no constructor made

  #############
  # Functions #
  #############

  # Return the position of the current payment period
  @staticmethod
  def updatePeriod():
    # check if december to january transition
    if World.monthPosition > 11:
      World.monthPosition = 0
      World.year += 1

    World.period = World.dates[World.datesPosition] + World.months[World.monthPosition]

    if World.datesPosition == 0:
      World.datesPosition = 1
    else:
      World.datesPosition = 0
      World.monthPosition += 1

    return World.period
  # End of updatePeriod function

  @staticmethod
  def getPeriod():
    return ('Year ' + str(World.year) + ": " + World.period)
  # End of printPeriod function

  @staticmethod
  def yearsToTimePeriods(years):
    return years * 24

  @staticmethod
  def simulateTime():
    # specify how much time to pass, default is 5 years, do not change for now
    periodsToSimulate = World.yearsToTimePeriods(5)

    # pass the time
    while periodsToSimulate > 0:
      World.updatePeriod()
      periodsToSimulate -= 1
      for x in Entity.data_entities:
        x.economicSituation(World.getPeriod())

    # update entity data to reflect the earnings results over time
    for x in Entity.data_entities:
        x.updateAllDataAsArray()

    print('cookies are done baking!')

    '''
    # these lines to test output is correct
    # remove the triple quotes before and after this block of code to see
    # print results to console
    currentPeriod = 0
    totalPeriods = len(Entity.data_entities[0].timePeriod)
    testEntity = Entity.data_entities[631]
    while currentPeriod < totalPeriods:
      print(testEntity.timePeriod[currentPeriod])
      print('\tDeposit: ' + '${:,.2f}'.format(testEntity.deposits[currentPeriod]))
      print('\tWithdrawel: ' + '${:,.2f}'.format(testEntity.withdrawels[currentPeriod]))
      print('\tTotal Earnings: ' + '${:,.2f}'.format(testEntity.earnings[currentPeriod]))
      currentPeriod += 1
    '''
  # End of simuilateTime function

# End of World class

#####################
# Program Functions #
#####################

# Get Data from the Capital One API
def getDataUsingAPI():
  # Capital One API Data Access
  base_url = "http://api.reimaginebanking.com"
  apiKey = 'bb0373b06737a100c08c6efcfc710939'
  request_url = base_url + "/atms?key=" + apiKey
  response_data = requests.get(request_url)
  response_text = json.loads(response_data.text)

  # Entity data as a JSON object
  data = response_text['data']

  # Previous and next page (each page contains 10 entities)
  paging = response_text['paging']

  data_sets = 0

  while len(data) != 0:
    for x in data:
      entity = Entity(x['_id'], x['name'], x['geocode'], x['accessibility'], x['hours'], x['address'], x['language_list'], x['amount_left'])
      Entity.data_entities.append(entity)

    previousURL = base_url + paging['previous']
    nextURL = base_url + paging['next']

    if data_sets > 0:
      page = Page(previousURL)

    # Update API request for the next page
    response_data = requests.get(nextURL)
    response_text = json.loads(response_data.text)
    data = response_text['data']
    paging = response_text['paging']
    data_sets += 1

    if data_sets == 64:
      previousURL = base_url + paging['previous']
      Page(previousURL)
  # End While Loop
# End define getDataUsingAPI function

# Make CSV file for data
def createCSV():
  with open('entity_file.csv', mode='w') as entity_file:
    # Make CSV
    entity_writer = csv.writer(entity_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Column Names
    entity_writer.writerow(['ID', 'Account Number', 'Account Name', 'Longitude', 'Latitude', 'Accessibility', 'Hours', 'Street Address', 'City', 'State', 'Zip Code', 'Languages', 'Staring Account Balance', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount', 'Time Period', 'Deposit Amount', 'Withdrawal Amount', 'Time Period Balance Amount'])

    # Write data to CSV
    entity_array_position = 0
    while entity_array_position < len(Entity.data_entities):
      data = Entity.data_entities[entity_array_position]
      entity_writer.writerow(data.getAllAsArray())
      entity_array_position += 1

    Entity.data_entities[0].getAllAsString()
    # End While Loop
# End define createCSV function

def createTextFile():
  # open file
  f = open('file.txt','w')
  # loop through and write one entity per line in the file
  for x in Entity.data_entities:
    f.write(x.getAllAsString())
    # write a blank line between entity entries
    f.write('\n')
    f.write('\n')
  # close file
  f.close()

#####################
# Program Execution #
#####################
# Get starting data
getDataUsingAPI()

# Run simulation
World.simulateTime()

# Create a CSV based upon the results
createCSV()

# Create a text file based upon the results
createTextFile()
