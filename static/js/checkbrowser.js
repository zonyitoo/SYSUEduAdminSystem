// JavaScript Document

function detectBrowser()
{
	var browser=navigator.appName;
	var b_version=navigator.appVersion;
	var version=parseFloat(b_version);
	if (top.location.href!=location.href)
		top.location.href=index.html;
	if (!(browser=="Netscape" && version>=5|| browser=="Microsoft Internet Explorer" && version>=9))
	{
		alert("It's time to upgrade your browser!");
		location="http://www.googlestable.com";
	}
}
