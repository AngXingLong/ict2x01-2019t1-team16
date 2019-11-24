function insertJS(location){
    var script = document.createElement('script');
    script.src = location;
    document.getElementsByTagName('head')[0].appendChild(script);
  }
  
  function insertCSS(location){
    var link = document.createElement( "link" );
    link.href = location
    link.type = "text/css";
    link.rel = "stylesheet";
    document.getElementsByTagName("head")[0].appendChild(link);
  }

  insertCSS("css/bootstrap.min.css");
  insertJS("js/jquery-3.3.1.slim.min.js");
  insertJS("js/popper.min.js");
  insertJS("js/bootstrap.min.js");


