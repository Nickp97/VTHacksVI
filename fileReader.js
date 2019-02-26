/*
* Initial attempt at using JavaScript in order to parse the txt file produced from the Python script.
* This JavaScript file would have been used to parse the text data into a nice clean format that could
* have been displayed in an HTML document.
*
* Can be run in a terminal with the command: node fileReader.js
*
* The command will spam the terminal with the record data for all 632 entities that were pulled from
* the Capital One data set via the Nessie API.
*/

const fs = require('fs')

// Reading data in utf-8 format
// which is a type of character set.
// Instead of 'utf-8' it can be
// other character set also like 'ascii'
fs.readFile('file.txt', 'utf-8', (err, data) => {
    if (err) throw err;


    companyArray = data.split("\n\n");


    for (var i = 0; i < companyArray.length; i++)
    {
        companyArray[i] = companyArray[i].split(", ")
    }

    // Converting Raw Buffer to text
    // data using tostring function.
    for (var j = 0; j < companyArray.length - 1; j++)
    {
        console.log("Next Company Information to follow:")
        console.log(companyArray[j][0])

        for (var k = 1; k < companyArray[j].length; k++)
        {
            console.log("\t" + companyArray[j][k])
        }

        console.log("\n")
    }
})
