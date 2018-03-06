import csv
import xlwt
import os

allData = []

## lower case all data maybe or double check - mb
## add count of replies somewhere if possible - mb


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
                allData.append(dict(row))



#get list of dict. items with a selected activity on a selected device
def selectOneActivityOnOneDevice(activity,device):
    list = []
    goodList = []

    for i in range(len(allData)):
         if allData[i]['Activity'] == activity and allData[i]['Device'] == device:
             list.append(allData[i])

    for i in list:
        goodList.append(i)

    return goodList


#need dictionary like this:
#   dict = {'Read fiction':{'Device':'Phone',
#                           'Average beneficiality':'3.5',
#                           'Experienced':'50%',
#                           'Never':'10%',
#                           'Several times per day':'20%',
#                           'Several times per week':'20%',
#                           'Several times per month':'20%'}
#           }


#average beneficiality
def averageBeneficiality(data):
    totalBeneficiality = 0
    adjustBeneficiality = 0
    for i in range(len(data)):
        if data[i]['Beneficiality'] == "":
            adjustBeneficiality += 1
        else:
            totalBeneficiality += float(data[i]['Beneficiality'])
    averageBeneficiality = totalBeneficiality / (len(data) - adjustBeneficiality)
    return "{0:.1f}".format(averageBeneficiality)



#perecentage of experienced
def percentExperienced(data):
    experiencedCount = 0
    notExperiencedCount = 0
    noEntry = 0
    adjustExperience = 0
    selectedDataLength = len(data)


    for i in range(len(data)):
        if data[i]['Experienced'] == "":
            adjustExperience += 1
        elif data[i]['Experienced'] == 'yes':
            experiencedCount += 1
        elif data[i]['Experienced'] == 'no':
            notExperiencedCount += 1

    experiencedPercentage = 100 * experiencedCount / (selectedDataLength-adjustExperience)
    notExperiencedPercentage = 100 * notExperiencedCount / (selectedDataLength-adjustExperience)
    noEntryExpPercentage = 100 * noEntry / (selectedDataLength-adjustExperience)

    expDict ={'Experienced%':"{0:.1f}".format(experiencedPercentage),
              'NotExperienced%':"{0:.1f}".format(notExperiencedPercentage),
              'NoEntryExp%': "{0:.1f}".format(noEntryExpPercentage)
             }

    return expDict

#perecentage of frequencies
def percentFrequency(data):
    neverCount = 0
    perDayCount = 0
    perWeekCount = 0
    perMonthCount = 0
    adjustFrequency = 0
    selectedDataLength = len(data)

    for i in range(selectedDataLength):
        if data[i]['Frequency'] == "":
            adjustFrequency += 1
        elif data[i]['Frequency'] == 'never':
            neverCount += 1
        elif data[i]['Frequency'] == 'several times per day':
            perDayCount += 1
        elif data[i]['Frequency'] == 'several times per week':
            perWeekCount += 1
        elif data[i]['Frequency'] == 'several times per month':
            perMonthCount += 1
        else:
            adjustFrequency += 1

    neverFrequency = 100 * neverCount / (selectedDataLength-adjustFrequency)
    perDayFrequency = 100 * perDayCount / (selectedDataLength-adjustFrequency)
    perWeekFrequency = 100 * perWeekCount / (selectedDataLength-adjustFrequency)
    perMonthrequency = 100 * perMonthCount / (selectedDataLength-adjustFrequency)

    freqDict = {'never': "{0:.1f}".format(neverFrequency),
                'perDay': "{0:.1f}".format(perDayFrequency),
                'perWeek': "{0:.1f}".format(perWeekFrequency),
                'perMonth': "{0:.1f}".format(perMonthrequency)
    }

    return freqDict



def finalDict(activity,device):
    selectedData = selectOneActivityOnOneDevice(activity,device)
    resultDict = { activity:  {'Device':device,
                               'Average beneficiality':averageBeneficiality(selectedData),
                              'Experienced': percentExperienced(selectedData)['Experienced%'],
                              'Not experienced': percentExperienced(selectedData)['NotExperienced%'],
                              'never': percentFrequency(selectedData)['never'],
                              'perDay': percentFrequency(selectedData)['perDay'],
                              'perWeek': percentFrequency(selectedData)['perWeek'],
                              'perMonth': percentFrequency(selectedData)['perMonth']
                             }
                }
    return resultDict


#find results for each activity on each device
#list of devices
listOfDevices = set([allData[x]['Device'] for x in range(len(allData))])

#list of activities
listOfActivities = set([allData[x]['Activity'] for x in range(len(allData))])



listOfFinalResult =[]
for d in listOfDevices:
    for a in listOfActivities:
        listOfFinalResult.append(finalDict(a, d))



#write a csv
pathToWrite = '/Users/sgorbachov/Documents/PyCharm/UPIT/dataAnalysis/output/results.csv'
with open(pathToWrite, 'w') as csvfile:
    fieldnames = ['Activity', 'Device', 'Average beneficiality', 'Exp', 'Never', 'perDay', 'perWeek', 'perMonth']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    for i in listOfFinalResult:
        for key, value in i.items():
            writer.writerow({'Activity': key,
                             'Device': value['Device'],
                             'Average beneficiality':value['Average beneficiality'],
                             'Exp':value['Experienced'],
                             'Never':value['never'],
                             'perDay':value['perDay'],
                             'perWeek': value['perWeek'],
                             'perMonth': value['perMonth']
                                 })



#USELESS
#get all dict. items with a selected device
def selectDevice(device):
    list = [allData[x] for x in range(len(allData)) if allData[x]['Device'] == device]
    return list


#get all dict. items with a selected activity
def selectActivity(activity):
    list = [allData[x] for x in range(len(allData)) if allData[x]['Activity'] == activity]
    return list
