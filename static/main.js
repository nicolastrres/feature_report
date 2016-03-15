window.onload = function () {
    document.getElementById("file").onchange = function () {
        document.getElementById("upload_form").submit();
    };

    var scenarios = document.getElementById("scenarios");
    if(scenarios.offsetHeight > document.documentElement.offsetHeight){
        document.getElementById("features_nav").style.height = scenarios.offsetHeight+'px';
    }
};

