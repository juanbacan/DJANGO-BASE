const widthNav = 320;
const widtResize = 820;
let navIsOpen = false;

function openNav1() {
    document.getElementById("sidebar-main").style.width = widthNav + "px";
    document.getElementById("main").style.marginLeft = widthNav + "px";
    navIsOpen = true;
}

function openNav() {
    document.getElementById("sidebar-main").style.width = widthNav + "px";
    navIsOpen = true;
}

function changeNav() {
    if (navIsOpen) {
        closeNav();
    } else {
        openNav();
    }
}

function closeNav() {
    document.getElementById("sidebar-main").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
    navIsOpen = false;
}

window.addEventListener("resize", function() {
    if (window.innerWidth < widtResize) {
        closeNav();
        document.getElementById("btn-change-sidebar").style.display = "block";
    } else{
        openNav1();
        document.getElementById("btn-change-sidebar").style.display = "none";
    }
});

if (window.innerWidth < widtResize ) {
    closeNav();
    document.getElementById("btn-change-sidebar").style.display = "block";
} else {
    openNav1();
    document.getElementById("btn-change-sidebar").style.display = "none";
}

// If the user clicks anywhere outside of the sidebar, close it
window.addEventListener("click", function(event) {
    /*if (event.target == document.getElementById("main")) {
        closeNav();
    }*/
    if (window.innerWidth < widtResize && navIsOpen) {
        console.log("close");
        closeNav();
        if (navIsOpen){
            if (event.target != document.getElementById("sidebar-main") && event.target != document.getElementById("btn-change-sidebar")) {
                closeNav();
            }
        }
    }
});
