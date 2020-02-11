

//generate random int from min to max-1
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}

//generate random string of any length between min and max length inclusive using characters specified by ascii range variable
function generateRandomString(minLen, maxLen){
	var resultString = "";
	
	var length = getRandomInt(minLen, maxLen+1);
	for(var i = 1; i <= length; i++){
		resultString += String.fromCharCode(getRandomInt(asciiRange[0], asciiRange[1]+1));
	}
	return resultString;
}

function getInvOneHot(vec){
	var outVec = [];
	for(var i = 0; i < vec.length; i++){
		outVec.push(Math.abs(vec[i]-1));
	}
	return outVec;
}

//converts string to one-hot encoded (type = 1) eg. [[0, 0, 1, 0, 1, 0, 1],[1, 0, 0, 0, 0, 1, 1], [....], ....]  or character count vectors (type = 0) [2, 8, 1, 5, 4, ......]
function convertStringToVec(input, type, max_length){
  //var asciiRange = [32, 126];
  //console.log(type);
  if(type == "basic"){
    
    var vec = new Array((asciiRange[1]+1)-asciiRange[0]).fill(0);


    for(var i = 0; i < input.length; i++){
      vec[(input.charAt(i).charCodeAt(0))-asciiRange[0]] += 1;
    }

    

    return vec;
  } else {
    var vec = new Array(max_length);
    for (var i = 0; i < vec.length; i++) {
      vec[i] = new Array((asciiRange[1]+1)-asciiRange[0]).fill(0);
    }
    
    
    var final_vec = [];


    for(var i = 0; i < input.length; i++){

      vec[i][(input.charAt(i).charCodeAt(0))-asciiRange[0]] = 1;
    }

    //console.log(vec);

    for(var i = 0; i < vec.length; i++){
      for(var j = 0; j < vec[0].length; j++){
        final_vec.push(vec[i][j]);
      }
    }
    return final_vec;
  }
}


//pick randomly from 4 functions (replace, charAt, add, substring) and apply one to the input string 
//returns a tuple array: [output string, function number] 
function applyRandomFunction(input){
	var functionNumber = getRandomInt(1, numberOfFunctions+1);
	var outStr = "";
	var out = new Array(2); 


	switch(functionNumber){
		case 1:
			//var asciiRange = [32, 126];
			
			var randomPos;
			var randomChar = String.fromCharCode(getRandomInt(asciiRange[0], asciiRange[1]+1));
			randomPos = getRandomInt(0, input.length);
			outStr = input.replace(input[randomPos], randomChar)
			// if(Math.random() < 0.85){
			// 	var randomChar = String.fromCharCode(getRandomInt(asciiRange[0], asciiRange[1]+1));
			// 	randomPos = getRandomInt(0, input.length);
			// 	outStr = input.replace(input[randomPos], randomChar)
			// } else {
				
			// 	randomPos = [];
			// 	randomPos.push(getRandomInt(0, input.length-1));
			// 	randomPos.push(getRandomInt(randomPos[0], input.length));
			// 	//console.log(randomPos.toString());
			// 	var randomChars = generateRandomString((randomPos[1]-randomPos[0]), (randomPos[1]-randomPos[0])+1);
			// 	//console.log(randomChars.toString());
			// 	outStr = input.replace(input.substring(randomPos[0], randomPos[1]+1), randomChars);

			// }
			
			break;
		case 2:
			outStr = input[getRandomInt(0, input.length)];
			break;
		
		case 3:
			var randomPos = [];
			randomPos.push(getRandomInt(0, input.length-2));
			randomPos.push(randomPos[0]+2);
			subStr = input.substring(randomPos[0], randomPos[1]+1);
			outStr = input + subStr;
			break;

		case 4:
			var randomPos = [];
			randomPos.push(getRandomInt(0, input.length-1));
			randomPos.push(getRandomInt(randomPos[0], input.length));
			outStr = input.substring(randomPos[0], randomPos[1]+1);
			break;

	}
	out = [outStr, functionNumber];
	return out;
}

//subtracts two integer arrays
function subtractOneHotVecs(vec1, vec2){
	var newVec = new Array(vec1.length)

	for(var i = 0; i < newVec.length; i++){
		newVec[i] = Math.abs(vec1[i]-vec2[i]);
	}
	return newVec;
}


//generates data and saves it to file named string_data.csv
//each row of the new data consists of [vector of input string, vector of output string, functions one hot vector] 
//or [vector of input string, vector of output string, subtraction of vectors, functions one hot vector]
function generateData(ammountOfData, vecType, max_string_length, maxFunctionsToApply, vecSubtraction, toggleFilter){
	const fs = require('fs');
	var fd = fs.openSync("string_data.csv", 'w');
	var data = new Array(ammountOfData);
	for(var i = 1; i <= ammountOfData; i++){
		var numFunctionsToApply = getRandomInt(1,maxFunctionsToApply+1);
		var funcOneHot = new Array(numberOfFunctions).fill(0);
		var functionsUsed = [];
		var randomString = generateRandomString(1, max_string_length-3);
		var inputString = randomString;
		var inputStringOneHot = convertStringToVec(randomString, vecType, max_string_length);
		var outputString = "";
		var finalString = "";
		for(var j = 1; j <= numFunctionsToApply; j++){
			outputString = applyRandomFunction(inputString);
			while(functionsUsed.includes(outputString[1])){
				outputString = applyRandomFunction(inputString);
			}
			functionsUsed.push(outputString[1]);
			inputString = outputString[0];
		}
		finalString = inputString;
		
		var outputStringOneHot = convertStringToVec(inputString, vecType, max_string_length);
		for(var k = 0; k < functionsUsed.length; k++){
			funcOneHot[functionsUsed[k]-1] = 1;
		}

		if(toggleFilter){
			funcOneHot = getInvOneHot(funcOneHot);
		}

		if(vecSubtraction){
			var row = [randomString, finalString, functionsUsed, inputStringOneHot, outputStringOneHot, subtractOneHotVecs(outputStringOneHot, inputStringOneHot), funcOneHot];
		} else {
			var row = [randomString, finalString, functionsUsed, inputStringOneHot, outputStringOneHot, funcOneHot];
		}

		data.push(row);

		
  
		// Data which will write in a file. 
		var writeData = row.slice(3,row.length).toString();
		console.log(i);
  		
  		var bytes = fs.writeSync(fd, writeData+"\n", null, null);
		
		




	}
	fs.closeSync(fd);
	return data;
}

var readlineSync = require('readline-sync');

function getInput(question){
	var qAnswer = readlineSync.question(question);
	
	return qAnswer;
}


var asciiRange = [97, 122];

var asciiRange = getInput("Enter the ascii range: ").split("-").map(function (x) { 
   return parseInt(x, 10); 
}); 

var numRows = parseInt(getInput("Enter the amount of data: "), 10);

var maxStringLength = parseInt(getInput("Enter the maximum string length: "), 10);

var encoding = "one-hot";

if(getInput("Do you want one-hot encoding (y/n): ").toLowerCase() == "n"){
	encoding = "basic";
}

var filter = false;
if(getInput("Do you want to toggle filter mode (y/n): ").toLowerCase() == "y"){
	filter = true;
}

var numberOfFunctions = 4;

if(getInput("Do you want the subtracted vectors as a column (y/n): ").toLowerCase() == "y"){
	generateData(numRows, encoding, maxStringLength, 2, true, filter);
} else {
	generateData(numRows, encoding, maxStringLength, 2, false, filter);
}





