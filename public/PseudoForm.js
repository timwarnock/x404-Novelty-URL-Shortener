/* ********************************************************************************
  PseudoForm.js

  PseudoForm namespace 'xpf'

******************************************************************************** */
var xpf = new function() {

var _self= this;

// public
this.addCSS = function() {
  var head = document.head;
  var link = document.createElement("link");
  link.type = "text/css";
  link.rel = "stylesheet";
  link.href = "https://avant.net/artwork/artwork.css";
  head.appendChild(link);
};


// public
this.sleep = function(ms) {
    // usage: 
    // sleep(1000).then(() => { //do something after });
    return new Promise(resolve => setTimeout(resolve, ms));
}


// public
this._GET = function(testk) {
    var qs = window.location.search.substring(1);
    var qs_array = qs.split('&');
    for (var i = 0; i < qs_array.length; i++) {
        var ik = qs_array[i].split('=');
        if(ik[0] == testk){
            return ik[1];
        }
    }
}

// private 
var _JSON = function(method, url, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        var resjson = xhr.response;
        if (typeof resjson == "string") {
          resjson = JSON.parse(xhr.response);
        }
        callback(null, resjson);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send(JSON.stringify(data));
};

// public
this.POST = function(url, data, callback) { _JSON('POST', url, data, callback); };
this.PUT = function(url, data, callback) { _JSON('PUT', url, data, callback); };

// private (fetch JSON object from URL)
var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        var resjson = xhr.response;
        if (typeof resjson == "string") {
          resjson = JSON.parse(xhr.response);
        }
        callback(null, resjson);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

// public
this.getformkey = function() {
    getJSON('/__formkey__/',
    function(err, data) {
      if (err !== null) {
        console.log('Something went wrong: ' + err);
      } else {
        if ("formkey" in data) {
          _self.formkey = data.formkey;
        } else {
          console.log('SUCCESS status from //__formkey__/ but no formkey returned');
        }
      }
    });
}


}; //end xpf

