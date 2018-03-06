import csv
import xlwt
import os

allData = []

###create multiple files and reference them and divide my code into view, model, mv

#opening all files in a folder and reading data
dataDir = '/Users/sgorbachov/Documents/PyCharm/UPIT/dataAnalysis/data'
os.chdir(dataDir)
for file in os.listdir(dataDir):
    if file == '.DS_Store':
         print('a DS_Store item encountered')
         os.remove(file)

    else:
        with open(file, 'rt') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print(row)
                allData.append(dict(row))



#get list of possible values in each category; ex. {ID: {s1,s2,...}, Gender: {'', 'f','m'},...
def dictOfListsOfCategoryItems():
    dict = {}
    listOfKeys = []

    for key in allData[1]:
        listOfCategories = set([allData[x][key].lower() for x in range(len(allData))])
        dict[key] = listOfCategories
        listOfKeys.append(key)

    dict['Keys'] = listOfKeys

    return dict

#Categories:
countables = ['Age', 'Gender', 'FL', 'Level','Academic status','NL']
uncountables = ['Purpose', 'Other languages', 'Devices owned']
calculate = ['How long (months)']

#ID,
#Countable: Age, Gender, FL, Level, Academic status, NL
#Calculate: How long (months)
#Uncountable: Purpose, Other languages, Devices owned
#Activity, Device, Frequency, Experienced, Beneficiality


dictOfListsOfCategoryItems = dictOfListsOfCategoryItems()
#print(dictOfListsOfCategoryItems['Age'])

#get data about every student
def getDemoData(ID):
    list = []
    for i in ID:
        for k in allData:
            if i == k['ID'].lower():
                list.append(k)
                break
    return list

demoData = getDemoData(dictOfListsOfCategoryItems['ID'])

### Count number of each possible input value in a contable category
def countCountables(categoryItemsList, category):
    returnDict = {}

    if not returnDict:
        for i in categoryItemsList:
            returnDict[i] = 0

    for i in demoData:
        for key in returnDict:
            if i[category].lower() == key:
                returnDict[key] += 1

    return returnDict
#
# r3 = categoryValuesCouter(dictOfListsOfCategoryItems['FL'],'FL')
# print(r3)







###Get lists of possible inputs for uncountables
purposeList = ['cultural interest','tourism/vacation','communicate better','business/employment','academic','language requirement','understand ethnic heritage','religious','other:']
devicesOwned = ['laptop', 'desktop','phone w', 'phone w/out', 'tablet']

listOfPossibleLanguages = []
for i in demoData:
    for x in i['Other languages'].split(','):
        listOfPossibleLanguages.append(x.lower().strip())
listOfPossibleLanguagesSet = set(listOfPossibleLanguages)

dictOfListsOfUniqueUncountableValues = {'Purpose':purposeList,
                                        'Other languages': listOfPossibleLanguagesSet,
                                        'Devices owned': devicesOwned}
###

###fix this as it now it's a dictionary not a list
def countUncountables(listOfPossibleValues,category):
    dict = {}

    if not dict:
        for z in listOfPossibleValues:
            dict[z] = 0

        for i in demoData:
            for x in listOfPossibleValues:
                if x in i[category].lower():
                    dict[x] += 1
    return dict

# r5 = countUncountables(dictOfListsOfUniqueUncountableValues['Devices owned'],'Devices owned')
# print(r5)

#print(dictOfListsOfCategoryItems['Keys'])

def uncountableFinalCounter():
    dictionaryOfUncountables = {}
    for key in uncountables:
        dictionaryOfUncountables[key] = countUncountables(dictOfListsOfUniqueUncountableValues[key], key)
    return dictionaryOfUncountables

#print(uncountableFinalCounter())


#Count countable categories
def countableCounter():
    dictionaryOfCountables = {}
    for key in countables:
        dictionaryOfCountables[key] = countCountables(dictOfListsOfCategoryItems[key], key)
    return dictionaryOfCountables

#print(countableCounter())


def finalCounter():
    finalDictionary = {}
    for key in dictOfListsOfCategoryItems['Keys']:
        if key in uncountables:
            finalDictionary[key] = countUncountables(dictOfListsOfUniqueUncountableValues[key], key)
        elif key in countables:
            finalDictionary[key] = countCountables(dictOfListsOfCategoryItems[key], key)

    return finalDictionary

finalResult = finalCounter()


#print(finalResult)
# for key, value in finalResult.items():
#     print(key, value)
    #print(finalResult[key])


####SORT by values from largest to smallest

#write a csv
pathToAppend = '/Users/sgorbachov/Documents/PyCharm/UPIT/dataAnalysis/output/demoResults.csv'

for key,value in finalResult.items():
    # fieldnames = [header for header in value]
    # fieldnames.insert(0, 'category')
    # print(fieldnames)
    for key4 in value:
        if key4 == "":
            value['No entry'] = value.pop("")
    fieldnames = [header for header in value]
    fieldnames.insert(0, 'Category')
    value['Category'] = key



    with open(pathToAppend, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(value)





    # for key2,value2 in value.items():
    #     print(key2,value2)

    # with open(pathToAppend, 'a') as csvfile:
    #     fieldnames = [header for header in value]
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #
    #
    #     writer

    # for key2,value2 in value.items():
    #     print(key2)
        # fieldnames = [x for key in value]
        # print(fieldnames)


# with open(pathToAppend, 'a') as csvfile:
#     fieldnames = ['Activity', 'Device', 'Average beneficiality', 'Exp', 'Never', 'perDay', 'perWeek', 'perMonth']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#
#     for i in listOfFinalResult:
#         for key, value in i.items():
#             writer.writerow({'Activity': key,
#                              'Device': value['Device'],
#                              'Average beneficiality':value['Average beneficiality'],
#                              'Exp':value['Experienced'],
#                              'Never':value['never'],
#                              'perDay':value['perDay'],
#                              'perWeek': value['perWeek'],
#                              'perMonth': value['perMonth']
#                                  })
#
