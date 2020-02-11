

var fs = require("fs");
const math = require('mathjs')
var esprima = require('esprima');
var functionExtractor = require("function-extractor");

String.prototype.replaceAt=function(index, replacement) {
    return this.substr(0, index) + replacement+ this.substr(index + replacement.length);
}


function genPermutations(options) {
  var holdingArr = [];
  var threeOptions = options
  var recursiveABC = function(singleSolution) {
      if (singleSolution.length > (options.length-1)) {
        holdingArr.push(singleSolution);
        return;
      }
      for (var i=0; i < threeOptions.length; i++) {
        recursiveABC(singleSolution.concat([threeOptions[i]]));
      }
  };
  recursiveABC([]);
  return holdingArr;
}

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}


function allSubsets(arra, arra_size)
 {
    var result_set = [], 
        result;
    
   
for(var x = 0; x < Math.pow(2, arra.length); x++)
  {
    result = [];
    i = arra.length - 1; 
     do
      {
      if( (x & (1 << i)) !== 0)
          {
             result.push(arra[i]);
           }
        }  while(i--);

    if( result.length == arra_size)
       {
          result_set.push(result);
        }
    }

    return result_set; 
}


var source = fs.readFileSync("/Users/kairotieremorton/Desktop/test.js", "utf8")

var functions = functionExtractor.parse(source);
var intOperations = ['+', '*', '-'];
//var intOperations = ['+', '-'];
var intConsts = ['2','3','4','5','x'];
var operatorIndicies = [];
var numericIndicies = [];
var parsed = esprima.parseScript(source.slice(functions[0].blockStart+9,functions[0].end-1), {tokens: true, range: true});
console.log(parsed.tokens);


var counter = 0
parsed.tokens.forEach(function(token) {
	//console.log(token);
	
	if(token.type == 'Punctuator' && token.value != "(" && token.value != ")" && token.value != ";"){
		
		operatorIndicies.push(token.range[0]);

		//out[token.range[0]] = intOperations[Math.floor(Math.random()*intOperations.length)];
		
		
 		//console.log(source.slice(functions[0].blockStart+9,functions[0].end-1).replaceAt(token.range[0], '-'))	
 } else if(token.type == 'Numeric' || token.type == 'Identifier'){
		if(token.type == 'Identifier'){
			counter++;
			if(counter > 1){
				numericIndicies.push(token.range[0]);
			}
		} else{

			numericIndicies.push(token.range[0]);
		}
		

		//out[token.range[0]] = intOperations[Math.floor(Math.random()*intOperations.length)];
		
		
 		//console.log(source.slice(functions[0].blockStart+9,functions[0].end-1).replaceAt(token.range[0], '-'))	
 }
});

var data_counter = 0;

for(index = 0; index < intOperations.length; index++){
	for(index1 = 0; index1 < intOperations.length; index1++){
var modifiedIntOperations = [intOperations[index], intOperations[index1]];
var genOperatorPerms = genPermutations(modifiedIntOperations);
var operatorPerms = []
genOperatorPerms.forEach(function(element) {
  
  	operatorPerms.push(element);
  
});
var constsPerms = allSubsets(intConsts, modifiedIntOperations.length);
var out = source.slice(functions[0].blockStart+9,functions[0].end-1).split('');
var newCodeSnippets = []
//console.log(constsPerms);

for(i = 0; i < operatorPerms.length; i++){
	
		var zip1 = operatorPerms[i].map(function(e, x) {
  			return [e, operatorIndicies[x]];
		});
		for(q = 0; q < constsPerms.length; q++){
		//console.log(c);
		var zip2 = constsPerms[q].map(function(e, x) {
  			return [e, numericIndicies[x]];
		});
		
		for(j = 0; j < zip1.length; j++){
			//console.log(zip1[j]);
			out[zip1[j][1]] = zip1[j][0];
		}
		for(s = 0; s < zip2.length; s++){
			out[zip2[s][1]] = zip2[s][0];
		}

		var string_version = out.join('');
		//console.log(string_version);
		var result = math.simplify(string_version.substring(0,string_version.length - 2)).toString();

		result = result.replace("x ^ 2", "x * x");
		result = result.replace("-x", "-1*x");
		//result = result.replace("2 * x", "x+x");

		//var result = string_version;
		if(!newCodeSnippets.includes(result) && result.includes("x") && !result.includes("(")){
		//console.log(result);
		newCodeSnippets.push(result);
	}

		
}
}


//console.log(newCodeSnippets.length);


for(i = 0; i < newCodeSnippets.length; i++){
	var operators = [];
	console.log(newCodeSnippets[i]);
	esprima.parseScript(newCodeSnippets[i], {}, function (node) {
 	//console.log(node.tokens);
 	if(node.property != undefined){
    //console.log(node.property['name']);
 	}
 	if (node.operator != undefined){
 		
 		operators.push(node.operator);
 		
 	} 
});
	var unique = Array.from(new Set(operators));
	var one_hot = [];

	for(idx = 0; idx < intOperations.length; idx++){
		if(unique.includes(intOperations[idx])){
			one_hot.push(idx+1)
		} 
	}

	for(j = 1; j <= 20; j++){
	x = j;
	console.log(x + "," + eval(newCodeSnippets[i]) + "," + one_hot);
	data_counter++;
}
//console.log("\n\n\n")
}
}}

//console.log(data_counter);

//  esprima.parseScript(source.slice(functions[0].blockStart+9,functions[0].end-1), {}, function (node) {
//  	//console.log(node.tokens);
//  	if(node.property != undefined){
//     console.log(node.property['name']);
//  	}
//  	if (node.operator != undefined){
//  		console.log(node.operator);
 		
//  	} 
// });

//console.log(utils.getCode(esprima.parseScript(source.slice(functions[0].blockStart+9,functions[0].end-1))));
// esprima.tokenize(source.slice(functions[0].blockStart+9,functions[0].end-1), {}, function (node){
// 	if(node.type == 'Punctuator' && node.value != "(" && node.value != ")"){
// 		node.value
// }
// });

//console.log(esprima.tokenize(source.slice(functions[0].blockStart+9,functions[0].end-1)));

