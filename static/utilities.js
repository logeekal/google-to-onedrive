function popup(url){
	newWindow = window.open(url, height=250, width=250);
	if (window.focus){
		newWindow.focus();
	}
	return false;
}

$(document).ready(function(){
	$('.filebox').append('This is the Google Drive List');
	$('.filebox').buttonset();
});


