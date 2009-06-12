// holds an instance of XMLHttpRequest
var xmlHttp = createXmlHttpRequestObject();
// holds the remote server address 
var serverAddress = "../cgi-bin/save_user.py";
// when set to true, display detailed error messages
var showErrors = true;
// initialize the validation requests cache 
var cache = new Array();

function createXmlHttpRequestObject() 
{
  var xmlHttp;

  try { // Firefox, Opera 8.0+, Safari
      xmlHttp = new XMLHttpRequest();
  } catch (e) { // Internet Explorer
    try {
      xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e) {
      xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
  }

  if (!xmlHttp)
    displayError("Error creating the XMLHttpRequest object.");
  else 
    return xmlHttp;
}

// function that displays an error message
function displayError($message)
{
  // ignore errors if showErrors is false
  if (showErrors)
  {
    // turn error displaying Off
    showErrors = false;
    // display error message
 
    alert("Error encountered: \n" + $message);
    // retry validation after 10 seconds
    setTimeout("validate();", 10000);
  }
}

// the function handles the validation for any form field
function validate(inputValue, fieldID)
{
  // only continue if xmlHttp isn't void
  if (xmlHttp)
  {
    // if we received non-null parameters, we add them to cache in the
    // form of the query string to be sent to the server for validation
    if (fieldID)
    {
      // encode values for safely adding them to an HTTP request query string
      inputValue = encodeURIComponent(inputValue);
      fieldID = encodeURIComponent(fieldID);
      // add the values to the queue
      cache.push("inputValue=" + inputValue + "&fieldID=" + fieldID);
    }
    // try to connect to the server
    try {
      // continue only if the XMLHttpRequest object isn't busy
      // and the cache is not empty
      if ((xmlHttp.readyState == 4 || xmlHttp.readyState == 0) 
         && cache.length > 0)
      {
        // get a new set of parameters from the cache
        var cacheEntry = cache.shift();
        // make a server request to validate the extracted data
        xmlHttp.open("POST", serverAddress, true);
        xmlHttp.setRequestHeader("Content-Type", 
                                 "application/x-www-form-urlencoded");
        xmlHttp.onreadystatechange = handleRequestStateChange;
        xmlHttp.send(cacheEntry);
      }
    }
    catch (e)
    {
      // display an error when failing to connect to the server
      displayError(e.toString());
    }
  }
}

// function that handles the HTTP response
function handleRequestStateChange() 
{
  // when readyState is 4, we read the server response
  if (xmlHttp.readyState == 4) 
  {
    // continue only if HTTP status is "OK"
    if (xmlHttp.status == 200) 
    {
      try
      {
        // read the response from the server
        readResponse();
      }
      catch(e)
 
      {
        // display error message
        displayError(e.toString());
      }
    }
    else
    {
      // display error message
      displayError(xmlHttp.statusText);
    }
  }
}

// read server's response 
function readResponse()
{
  // retrieve the server's response 
  var response = xmlHttp.responseText;
  // server error?
  if (response.indexOf("ERRNO") >= 0 
      || response.indexOf("error:") >= 0
      || response.length == 0)
    throw(response.length == 0 ? "Server error." : response);
  // get response in XML format (assume the response is valid XML)
  responseXml = xmlHttp.responseXML;
  // get the document element
  xmlDoc = responseXml.documentElement;
  result = xmlDoc.getElementsByTagName("result")[0].firstChild.data;
  fieldID = xmlDoc.getElementsByTagName("fieldid")[0].firstChild.data;
  // find the HTML element that displays the error
  message = document.getElementById(fieldID + "Failed");
  // show the error or hide the error
  message.className = (result == "0") ? "error" : "hidden";
  // call validate() again, in case there are values left in the cache
  setTimeout("validate();", 250);
}

// sets focus on the first field of the form
function setFocus()    
{
  document.getElementById("txtUsername").focus();
}

