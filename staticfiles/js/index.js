window.onload = function () {
    setTimeout(load, 1000);
};

var maindiv = document.getElementById("main");
window.addEventListener('scroll', redirect);
maindiv.addEventListener('click', redirect);

function redirect() {
    window.location.href = "landing/";
}

function load() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("main").style.display = "block";
}

countDownDate = countDownDate;

var x = setInterval(function () {
    var now = new Date().toLocaleString("en-US", { timeZone: "Asia/Dhaka" });
    now = new Date(now).getTime();

    var distance = countDownDate - now;

    if (distance < 0) {
        clearInterval(x);
        setModified(0, 0, 0, 0);
        return;
    }

    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("days").innerHTML = days;
    document.getElementById("hours").innerHTML = hours;
    document.getElementById("minutes").innerHTML = minutes;
    document.getElementById("seconds").innerHTML = seconds;
}, 1000);

function setModified(d, h, m, s) {
    document.getElementById("days").innerHTML = d;
    document.getElementById("hours").innerHTML = h;
    document.getElementById("minutes").innerHTML = m;
    document.getElementById("seconds").innerHTML = s;

    ["days", "hours", "minutes", "seconds", "colon-1", "colon-2"].forEach(id => {
        var el = document.getElementById(id);
        if (el) el.className = "timer-modified";
    });
}
