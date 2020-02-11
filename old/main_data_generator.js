function getInput(question){
  var qAnswer = readlineSync.question(question);
  
  return qAnswer;
}

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

var readlineSync = require('readline-sync');
var asciiRange = [32, 90];


var data;


function convertStringToVec(input, type, max_length){
  //var asciiRange = [32, 126];
  //console.log(type);
  if(type == "basic"){
    
    var vec = new Array(max_length).fill(0);


    for(var i = 0; i < input.length; i++){
      vec[i] = (input.charAt(i).charCodeAt(0)+1)-asciiRange[0];
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

function getFunctionsUsed(composite, outType){
  var functionsUsed = [];
  var possibleFunctionsStr = ["str.++", "str.replace", "str.at", "int.to.str", "str.substr", "(+", "(-", "str.len", "str.to.int", "str.indexof"];
  var possibleFunctionsBool = ["str.++", "str.replace", "str.at", "int.to.str", "str.substr", "(+", "(-", "str.len", "str.to.int", "str.indexof", "str.contains", "str.prefixof", "str.suffixof"];
  var possibleFunctions = possibleFunctionsStr
  if(outType == "Bool"){
    possibleFunctions = possibleFunctionsBool
  }
  for(var i = 0; i < possibleFunctions.length; i++){
    if(composite.includes(possibleFunctions[i])){
      functionsUsed.push(i);
    }
  }
  return functionsUsed;
}


function subtractOneHotVecs(vec1, vec2){
  var newVec = new Array(vec1.length)

  for(var i = 0; i < newVec.length; i++){
    newVec[i] = Math.abs(vec1[i]-vec2[i]);
  }
  return newVec;
}

function getInvOneHot(vec){
  var outVec = [];
  for(var i = 0; i < vec.length; i++){
    outVec.push(Math.abs(vec[i]-1));
  }
  return outVec;
}



// const fs = require('fs');
// var fd = fs.openSync("test.csv", 'w');
// var final_row = [convertStringToVec("Kai/More", "one-hot", 8), convertStringToVec("K:M:", "one-hot", 8)]
// var writeData = final_row.toString();
// fs.appendFileSync('test.csv', writeData+"\n");

// console.log("done");

function generateData(ammountOfData, inType, outType, inFile, outFile, numPossibleFunctions){

var counter = 0;


//var num_Examples = 4;
var fileinput = require('fileinput');
const fs = require('fs');
var fd = fs.openSync(outFile, 'w');

fileinput.input(inFile)
  .on('line', function(line) {
    if(counter >= ammountOfData){
      return "done";
    }
  
    var func = line.toString();
    // var input = generateRandomString(1, 20);
    var input_list = []
    var output_list = []
    // var input = "POTATO0123"
    var functionsUsedOneHot = new Array(numPossibleFunctions).fill(0);
    var functions = getFunctionsUsed(func);
    //console.log('(set-logic ALL)\n' + func + '(declare-fun x () String)\n(assert (= x (f "'+ input +'")))\n(check-sat)\n(get-value (x))\n\n\n\n')
    //console.log(func);

    for(var k = 0; k < functions.length; k++){
      functionsUsedOneHot[functions[k]] = 1;
    }
  // var final_row = [];
  // var while_counter = 0;
  // while(input_list.length < num_Examples && while_counter < 10){
  // while_counter += 1;
  if(inType == "String"){
    var input = generateRandomString(1, 20);
    // Data which will write in a file. 
    var data = '(set-logic ALL)\n' + func + '(declare-fun x () '+outType+')\n(assert (= x (f "'+ input +'")))\n(check-sat)\n(get-value (x))'
  } else {
    var input = getRandomInt(1, 10)
    var data = '(set-logic ALL)\n' + func + '(declare-fun x () '+outType+')\n(assert (= x (f '+ input +')))\n(check-sat)\n(get-value (x))'
  }

  // console.log(data)
  
  
  

try{
  fs.writeFileSync('function.smt2', data, (err) => { 
      
    // In case of a error throw err. 
  }) 


  var execSync = require('child_process').execSync, output;
  var output = execSync('cvc4 -m function.smt2').toString().split("\n")[1]
  // console.log(output)
  var new_output;
  if(outType == "String"){
    new_output = output.split('"')[1];
  } else {
    new_output = output.slice(output.indexOf(" ")+1,output.indexOf(")"))

  }
  var final_row = [];
  // console.log(new_output)
  // console.log(input)
  // console.log(line.toString())
  // console.log(new_output)
  if(new_output != "" && new_output.length <= 20){
    console.log(new_output)
    // input_list.push(input);
    // output_list.push(output);

    if(inType == "String"){
      var input_vec = convertStringToVec(input, "basic", 20)
    } else {
       var input_vec = input
    }



    if(outType == "String"){
      var output_vec = convertStringToVec(new_output, "basic", 20)
    } else if (outType == "Int") {
      var output_vec = parseInt(new_output);
    } else {
      var output_vec = (new_output == 'true');
      if (output_vec){
        output_vec = 1
      } else {
        output_vec = 0
      }

    }


    // console.log(output)
    



    // output_vec = convertStringToVec(output, "one-hot", 20)

    final_row = [input_vec, output_vec, functionsUsedOneHot];
    //final_row = [subtractOneHotVecs(input_vec, output_vec), convertStringToVec(output, "one-hot", 20), functionsUsedOneHot]
    var writeData = final_row.toString();
    fs.appendFileSync(outFile, writeData+"\n");
    counter++;
    console.log(counter);


    
  }
} catch(err){

}

//}
//   if(while_counter < 10){
//   console.log(counter);
//   for(var i = 0; i < num_Examples; i++){
//     final_row.push(convertStringToVec(input_list[i], "basic", 20))
//     final_row.push(convertStringToVec(output_list[i], "basic", 20))
//   }
//   final_row.push(functionsUsedOneHot)
//   var writeData = final_row.toString();
//   fs.appendFileSync('string_data_full_multi.csv', writeData+"\n");
//   counter++;
// }
});
}

generateData(150000, "Int", "String", "/Users/kairotieremorton/all_functions/random_functions_int_str_shuffled.csv", "int_str_data.csv", 10)








