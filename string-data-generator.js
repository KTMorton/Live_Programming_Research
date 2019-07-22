var asciiRange = [97, 122];
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}

function generateRandomString(minLen, maxLen){
	var resultString = "";
	
	var length = getRandomInt(minLen, maxLen+1);
	for(var i = 1; i <= length; i++){
		resultString += String.fromCharCode(getRandomInt(asciiRange[0], asciiRange[1]+1));
	}
	return resultString;
}

function convertStringToVec(input, type){
	//var asciiRange = [32, 126];
	//console.log(type);
	if(type == 0){
		
		var vec = new Array((asciiRange[1]+1)-asciiRange[0]).fill(0);


		for(var i = 0; i < input.length; i++){
			vec[(input.charAt(i).charCodeAt(0))-asciiRange[0]] += 1;
		}

		

		return vec;
	} else {
		var vec = new Array(8).fill(new Array((asciiRange[1]+1)-asciiRange[0]).fill(0));
		
		var final_vec = [];

		for(var i = 0; i < input.length; i++){

			vec[i][(input.charAt(i).charCodeAt(0))-asciiRange[0]] = 1;
		}

		for(var i = 0; i < vec.length; i++){
			for(var j = 0; j < vec[0].length; j++){
				final_vec.push(vec[i][j]);
			}
		}
		return final_vec;
	}
}



function applyRandomFunction(input){
	var numberOfFunctions = 4;
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
			outStr = input + generateRandomString(1, 3);
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

function subtractOneHotVecs(vec1, vec2){
	var newVec = new Array(vec1.length)

	for(var i = 0; i < newVec.length; i++){
		newVec[i] = Math.abs(vec1[i]-vec2[i]);
	}
	return newVec;
}

// var randomString = generateRandomString(1,10);
// console.log(randomString);
// var output = applyRandomFunction(randomString);
// console.log(output[0]);
// console.log(convertStringToVec(output[0]).toString());
// console.log("\n");
// console.log(convertStringToVec(randomString).toString());

function generateData(ammountOfData, numberOfFunctions, vecType){
	const fs = require('fs');
	var fd = fs.openSync("string_data.csv", 'w');
	var data = new Array(ammountOfData);
	for(var i = 1; i <= ammountOfData; i++){
		var numFunctionsToApply = getRandomInt(1,3);
		var funcOneHot = new Array(numberOfFunctions).fill(0);
		var functionsUsed = [];
		var randomString = generateRandomString(1, 5);
		var inputString = randomString;
		var inputStringOneHot = convertStringToVec(randomString, vecType);
		var outputString = "";
		var finalString = "";
		//console.log(inputString);
		for(var j = 1; j <= numFunctionsToApply; j++){
			outputString = applyRandomFunction(inputString);
			while(functionsUsed.includes(outputString[1])){
				outputString = applyRandomFunction(inputString);
			}
			//console.log(outputString);
			functionsUsed.push(outputString[1]);
			inputString = outputString[0];
		}
		finalString = inputString;
		
		var outputStringOneHot = convertStringToVec(inputString, vecType);
		for(var k = 0; k < functionsUsed.length; k++){
			funcOneHot[functionsUsed[k]-1] = 1;
		}
		var row = [randomString, finalString, functionsUsed, inputStringOneHot, outputStringOneHot, subtractOneHotVecs(outputStringOneHot, inputStringOneHot), funcOneHot];
		//var row = [randomString, finalString, functionsUsed, inputStringOneHot, outputStringOneHot, funcOneHot];

		data.push(row);
		
  
		// Data which will write in a file. 
		var writeData = row.slice(3,row.length).toString();
		console.log(i);
  		
  		var bytes = fs.writeSync(fd, writeData+"\n", null, null);
		
		// var print = "";
		// for(var index = 0; index < row.length; index++){
		// 	print += ("["+row[index]+"],");
		// }
		// console.log(print);





	}
	fs.closeSync(fd);
	return data;
}

generateData(100000, 4, 1);