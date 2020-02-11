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













// const fs = require('fs');
// var fd = fs.openSync("test.csv", 'w');
// var final_row = [convertStringToVec("Kai/More", "one-hot", 8), convertStringToVec("K:M:", "one-hot", 8)]
// var writeData = final_row.toString();
// fs.appendFileSync('test.csv', writeData+"\n");

// console.log("done");

function generateData(ammountOfData, inType, outType, inFile){

var counter = 0;


var num_Examples = 10;
var fileinput = require('fileinput');
const fs = require('fs');
// var fd = fs.openSync(outFile, 'w');




fileinput.input(inFile)
  .on('line', function(line) {
    if(counter >= ammountOfData){
      return "done";
    }
  
    var func = line.toString();
    var input_list = []
    var output_list = []
  // console.log(func)
  var while_counter = 0;
  while(input_list.length < num_Examples && while_counter < 30){
  while_counter += 1;
  // console.log(while_counter)
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
  //console.log(new_output)
  // console.log(input)
  // console.log(line.toString())
  // console.log(new_output)


  if(new_output != "" && new_output.length <= 20){
    // console.log(input)
    input_list.push(input);
    output_list.push(new_output);


    // counter++;
    // console.log(counter);


    
  }
} catch(err){

}

}

if(while_counter < 30 && !(output_list.every( (val, i, arr) => val === arr[0]))) { 
  counter++;
  fs.copyFile("/Users/kairotieremorton/str_str.sl", "benchmark_"+counter+".sl", (err) => {
  });
  var fd = fs.openSync("benchmark_"+counter+".sl", 'w');

  for(var i = 0; i < num_Examples; i++){
    fs.appendFileSync("benchmark_"+counter+".sl", '(constraint (= (f "'+ input_list[i] +'") "'+output_list[i]+'"))\n\n');
  }

  fs.appendFileSync("benchmark_"+counter+".sl", "\n(check-synth)");
  
  console.log(counter);
}

});

}



generateData(1000, "String", "String", "/Users/kairotieremorton/all_functions/random_functions_str_str_shuffled.csv")





