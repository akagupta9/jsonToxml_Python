import sys
import json;


class DataFetcher_ConverterUtility:

    def __init__(self, filePath):
        self.filePath = filePath;
        jsonFile = open(self.filePath)
        self.jsonData = json.load(jsonFile)

    def sanitize(self, input):
        input = input.replace("&", "&amp;").replace("\"", "&quot;")
        input = input.replace("<", "&lt;").replace(">", "&gt;")
        return input

    def getTotalTestCasesInSuite(self,suiteIndex):
        return len(self.jsonData[suiteIndex]['results'])

    def getTotalTestSuite(self):
        return len(self.jsonData)

    def getTestSuiteInfo(self, testSuiteIndex):
        testSuiteDatDictionary = {};
        jsonResultData = self.jsonData[testSuiteIndex]['results'];
        generationTime = self.jsonData[testSuiteIndex]['generated_at'];
        testSuiteDatDictionary["generated_at"] = generationTime;
        totalTestCasesInSuite = self.getTotalTestCasesInSuite(testSuiteIndex)
        testSuiteDatDictionary["testCounts"] = totalTestCasesInSuite;

        return testSuiteDatDictionary;

    def getTestCasesInfo(self, suiteIndex,  testCaseIndex):
        testCaseDatDictionary = {};
        jsonResultData = self.jsonData[suiteIndex]['results'][testCaseIndex];
        nodeData = jsonResultData['node'];
        executionTime = jsonResultData['execution_time'];

        # if jsonResultData['fail'] is None:
        #     testCaseFailureStatus = True;
        # else:
        #     testCaseFailureStatus = False;

        if jsonResultData['fail']:
            testCaseFailureStatus = True;
        else:
            testCaseFailureStatus = False;

        if jsonResultData['error'] != None:
            # testCaseErrorMessage = self.sanitize(jsonResultData['error']);
            testCaseErrorMessage = jsonResultData['error'];
        else:
            testCaseErrorMessage = " ";

        testCaseClassName = nodeData['package_name'];
        testCaseName = nodeData['name'];

        testCaseDatDictionary["executionTime"] = executionTime;
        testCaseDatDictionary['testCaseFailureStatus'] = testCaseFailureStatus;
        testCaseDatDictionary['testCaseErrorMessage'] = testCaseErrorMessage;
        testCaseDatDictionary['testCaseClassName'] = testCaseClassName;
        testCaseDatDictionary['testCaseName'] = testCaseName;
        testCaseDatDictionary['testCaseFailureStatus'] = testCaseFailureStatus;
        testCaseDatDictionary['testCaseFailureType'] = 'WARNING';

        return testCaseDatDictionary;


    def generateXMlFile(self):
        xmlHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
        testSuitesStartTag = "<testsuites"
        testSuitesEndTag = "</testsuites>"

        testSuiteTag = ""
        testSuiteStartTag = "\n" + "<testsuite"
        testSuiteEndTag = "</testsuite>"

        testCaseTag = ""
        testCaseStart = "\n" + "<testcase"
        testCaseEnd = "</testcase>"

        failureTagStart = "\n" + "<failure"
        failureTagEnd = "</failure>"

        testSuitesStartTag += ">"

        for testSuiteCounter in range(0, self.getTotalTestSuite()):

            testSuiteInfo = self.getTestSuiteInfo(testSuiteCounter);
            testSuiteTag += testSuiteStartTag;
            testSuiteTag += " tests=" + "\"" + str(testSuiteInfo['testCounts']) + "\"";
            testSuiteTag += " generated_at=" + "\"" + str(testSuiteInfo['generated_at']) + "\"";

            totalTestCasesInSuite = self.getTotalTestCasesInSuite(testSuiteCounter);

            for testcaseCounter in range(0, totalTestCasesInSuite):

                testCaseInfo = self.getTestCasesInfo(testSuiteCounter, testcaseCounter);
                testCaseTag += testCaseStart
                testCaseTag += " name=" + "\"" + testCaseInfo['testCaseName'] + "\"";
                testCaseTag += " class=" + "\"" + testCaseInfo['testCaseClassName'] + "\"";
                testCaseTag += " time=" + "\"" + str(testCaseInfo['executionTime']) + "\"" + ">";

                if testCaseInfo['testCaseFailureStatus']:
                    testCaseTag += failureTagStart;
                    testCaseTag += " message=" + "\"" + testCaseInfo['testCaseErrorMessage'] + "\"";
                    testCaseTag += " type=" + "\"" + testCaseInfo['testCaseFailureType'] + "\"";
                    testCaseTag += ">" + failureTagEnd + "\n";

                testCaseTag += testCaseEnd + "\n";
            testSuiteTag += ">" + testCaseTag;
            testSuiteTag += ">" + testSuiteEndTag + "\n";

        testSuitesStartTag += testSuiteTag;
        testSuitesStartTag += testSuitesEndTag + "\n";

        return xmlHeader + testSuitesStartTag;


object = DataFetcher_ConverterUtility(".//run_results.json");
data = object.generateXMlFile()
xmlFile = open(".//output.xml", 'w');
xmlFile.write(data)
xmlFile.close();
