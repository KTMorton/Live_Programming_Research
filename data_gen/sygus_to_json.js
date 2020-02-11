//Converts Sygus Benchmarks (inputs/outputs only) to json format for neural network
//used for prediction after the NN for criticality has already been trained.

var asciiRange = [32, 90];

function convertStringToVec(input, max_length){
  
    var vec = new Array(max_length).fill(0);
    for(var i = 0; i < input.length; i++){
      vec[i] = (input.charAt(i).charCodeAt(0))-asciiRange[0];
    }
    return vec;
}

function extractAllText(str){
  const re = /"(.*?)"/g;
  const result = [];
  let current;
  while (current = re.exec(str)) {
    result.push(current.pop());
  }
  return result.length > 0
    ? result
    : [str];
}

var fs = require('fs');
var testFolder = "/Users/kairotieremorton/Downloads/PBE_Strings_Track/";
var final_examples_list = {};
var file_list = fs.readdirSync(testFolder);

for(var index = 0; index < file_list.length; index++){
var addToFinalList = true;
var fileName = file_list[index];
console.log(fileName);
if(fileName.includes(".sl")){
var output = fs.readFileSync(testFolder + fileName, "utf8").split("constraint").slice(1);
for(var i = 0; i < output.length; i++){

	output[i] = output[i].match(/(?:[0-9]\)|[^\)])+/g).slice(0,2).toString().replace(" (= (f ", "").split(",");
	//console.log(output[i]);
}

for(var i = 0; i < output.length; i++){

	for(var j = 0; j < output[0].length; j++){
		if(output[i][j] != undefined){
		if((output[i][j].match(/\"/g) || []).length == 2){
			output[i][j] = convertStringToVec(extractAllText(output[i][j])[0].toUpperCase(), 20);

		} else {
			addToFinalList = false;
		}
	}
	

}

}
if(addToFinalList){
console.log(output)
final_examples_list[fileName] = output;
}
}

}


for (const [key, value] of Object.entries(final_examples_list)) {
  for(var i = 0; i < value.length; i++){
  	final_examples_list[key][i] = final_examples_list[key][i][0].concat(final_examples_list[key][i][1]);
  }
}

fs.writeFileSync('benchmarks.json', JSON.stringify(final_examples_list));

