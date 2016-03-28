var bankType="Master"; //VISA or Master



//console.log("transaction page");

var bank = document.getElementsByClassName("bank")[0];
var inputs = bank.getElementsByTagName("input");

//console.log(inputs.length);
for ( var i=0; i<inputs.length; i++ )
{
	//var att = inputs[i].attributes;
	//console.log(att.length);
	if ( inputs[i].hasAttribute("bankcode") )
	{
		var bankCode = inputs[i].getAttribute("bankcode");
		//console.log(bankCode);
		if (bankType == bankCode )
		{
			//console.log(bankCode);
			inputs[i].click();
			break;
		}
		//console.log(bankCode);
	}
}

/*
var nodes = document.getElementsByClassName("inputtext fLeft input120")[0].focus()
*/

/*
var search = document.getElementsByClassName("input_text_autocon text_val_ori")[0];

search.value ="testing";

var nodes = document.getElementsByClassName("inputtext fLeft input120")[0].childNodes;

for (var i=0; i< nodes.length; i++ )
{
	//console.log(nodes[i].nodeName);
	if ( nodes[i].nodeName == "INPUT" )
	{
		console.log(nodes[i].nodeName);
		//nodes[i].nodeValue = "12";
		nodes[i].value = "12"
		//nodes[i].value = "testing";
		//nodes[i].click();
		break;
	}
}
*/
