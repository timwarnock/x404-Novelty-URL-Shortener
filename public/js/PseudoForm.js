/* ********************************************************************************
  PseudoForm.js

  PseudoForm namespace 'xpf'

******************************************************************************** */
var xpf = new function() {


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

// public (open single exhibit in modal browser)
//   + exid is the div#id to write the browser
//   + exname is the name of the exhibit to open
this.exhibit = function(exid,exname) {
  var artw = this.getArtwork();
  if (exname in artw) {
    this.openModalBrowser(exname);
  } else {
    console.log('Fetching json');
    var self = this;
    getJSON('https://avant.net/artwork/json',
    function(err, data) {
      if (err !== null) {
        console.log('Something went wrong: ' + err);
      } else {
        self.setArtwork.apply(self, [data]);
        var msg = '';
        msg += '<div id="xg_browser" class="modal"><div id="xg_browserContent_wrap"></div></div>';
        msg += '<div id="xg_image" class="modal2"><div id="xg_imageContent"></div></div>';
        document.getElementById(exid).innerHTML = msg;
        self.openModalBrowser.apply(self, [exname]);
      }
    });
  }
};


}; //end xpf


// event listeners
// TODO make better (DRY)
window.onclick = function(event) {
  var modal = document.getElementById('xg_browser');
  if (event.target == modal) {
    xga.closeModalBrowser();
  }
  var modal2 = document.getElementById('xg_image');
  if (event.target == modal2) {
    xga.closeModalImage();
  }
  var clicke = document.getElementById('xg_gallery_artwork');
  if (event.target == clicke) {
    xga.closeModalBrowser();
  }
};


