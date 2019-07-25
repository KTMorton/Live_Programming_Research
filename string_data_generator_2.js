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
var asciiRange = [48, 90];


var data;


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

function getFunctionsUsed(composite){
  var functionsUsed = [];
  var possibleFunctions = ["str.++", "str.replace", "str.at", "int.to.str", "str.substr", "(+", "(-", "str.len", "str.to.int", "str.indexof"];

  for(var i = 0; i < possibleFunctions.length; i++){
    if(composite.includes(possibleFunctions[i])){
      functionsUsed.push(i);
    }
  }
  return functionsUsed;
}
function printArr(arr) {
  let str = "";
  for (let item of arr) {
    if (Array.isArray(item)) str += printArr(item);
    else str += item + ", ";
  }
  return str;
}

var counter = 1;
var fileinput = require('fileinput');
const fs = require('fs');
var fd = fs.openSync("string_data_2.csv", 'w');

fileinput.input("random_functions.csv")
  .on('line', function(line) {

    var func = line.toString();
    var input = generateRandomString(1, 5);
    var functionsUsedOneHot = new Array(10).fill(0);
    var functions = getFunctionsUsed(func);
    //console.log('(set-logic ALL)\n' + func + '(declare-fun x () String)\n(assert (= x (f "'+ input +'")))\n(check-sat)\n(get-value (x))\n\n\n\n')
    //console.log(func);

    for(var k = 0; k < functions.length; k++){
      functionsUsedOneHot[functions[k]] = 1;
    }
  
  // Data which will write in a file. 
  data = '(set-logic ALL)\n' + func + '(declare-fun x () String)\n(assert (= x (f "'+ input +'")))\n(check-sat)\n(get-value (x))'
  
  


  fs.writeFileSync('function.smt2', data, (err) => { 
      
    // In case of a error throw err. 
    if (err) throw err; 
  }) 


  var execSync = require('child_process').execSync, output;
  output = execSync('cvc4 -m function.smt2').toString().split("\n")[1].split('"')[1];
  var final_row = [];
  if(output != "" && output.length <= 8){
    console.log(counter);
    final_row = [input, output, convertStringToVec(input, "one-hot", 8), convertStringToVec(output, "one-hot", 8), functionsUsedOneHot];



    var writeData = printArr(final_row);
    fs.appendFileSync('string_data_2.csv', writeData+"\n");
    counter++;
  }

  


});








