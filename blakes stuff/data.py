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

#########################
# API Page Class #
#########################

class Page:
  ################################
  # Class documentation String   #
  # Accessed via: Entity.__doc__ #
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

    self.allDataAsString = str(self.entity_count) + ", " + str(self.account_id_number) + ", " + self.name + ", " + str(self.geography_longitude) + ", " + str(self.geography_latitude) + ", " + str(self.accessibility) + ", " + str(self.hours) + ", " + self.street_address + ", " + self.address_city + ", " + self.address_state + ", " + str(self.address_zip) + ", " + str(self.languages) + ", " + self.formatted_account_balance

    self.allDataAsArray = [str(self.entity_count), str(self.account_id_number), self.name ,str(self.geography_longitude), str(self.geography_latitude), str(self.accessibility), str(self.hours), self.street_address, self.address_city, self.address_state, str(self.address_zip), str(self.languages), self.account_balance]

  #############
  # Functions #
  #############

  # Need getter / setter things (maybe?)
  # Need data manipulators
  # Need data classifiers

  # Return the entity as a string
  def getAllAsString(self):
    return self.allDataAsString

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

##############################
# Initial program setup code #
##############################

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

# Entity retrieval count, move to entity class
count = 0 # no data sources retrieved yet

###########################################################
# Testing this process to get all data points we can get. #
###########################################################
data_sets = 0

# Loop to read in data from Capital One API
# Most likely should be moved to its own function
# and called from there
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
    page = Page(previousURL)

# End While Loop

# Make CSV file for data to be printed to
with open('entity_file.csv', mode='w') as entity_file:
  entity_writer = csv.writer(entity_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  entity_writer.writerow(['ID', 'Account Number', 'Account Name', 'Longitude', 'Latitude', 'Accessibility', 'Hours', 'Street Address', 'City', 'State', 'Zip Code', 'Languages', 'Current Account Balance'])

  entity_array_position = 0
  while entity_array_position < len(Entity.data_entities):
    data = Entity.data_entities[entity_array_position]
    print(data.getAllAsString())
    entity_writer.writerow(data.getAllAsArray())
    entity_array_position += 1
  # End While Loop
