
// Whenever a new photo is selected, replace the image preview
document.getElementById("hiddenButton").onchange = function () {
    var reader = new FileReader();

    reader.onload = function (e) {
        // get loaded data and render thumbnail.
        document.getElementById("image").src = e.target.result;
    };

    // read the image file as a data URL.
    reader.readAsDataURL(this.files[0]);
};

//When the image is clcked, pretend it is a button for file selecting
$("#image").click(function() {
	$("input[id='hiddenButton']").click();
});



//MAKE SURE PHOTO IS ATTACHED
function validate (formObj) {
	if ( $("#image").attr("src") == "resources/images/upload.jpg") {
		alert("Please choose a picture before submitting");
		return false;
	}
	else {
		alert("Form validated");
		return true;
	}
}