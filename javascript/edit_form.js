/* This code is to toggle the colour of the save and view buttons when data is changed

*/

// Declare any global variables to hold toggle state
//	var toggle = true; // Always start with true	


// This function toggles the buttons by changing the style
	function state_changed(){
		document.getElementById("save_button").setAttribute("style", "background:#ff0000");
		document.getElementById("view_button").setAttribute("style", "background:#999999");
		document.getElementById("copy_button").setAttribute("style", "background:#999999");		
}
	function copy_card(arg_key_name){
	var current_value
	current_value = document.getElementById("Cardtitle").value;
	document.getElementById("Cardtitle").value = "Copy of " + current_value;
	document.getElementById("field_Cardtitle").setAttribute("style", "background:#ff0000");
	document.getElementById("Key_Name").value = arg_key_name;	
	state_changed()
}
