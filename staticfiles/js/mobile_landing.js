document.addEventListener("DOMContentLoaded", load);

function load() {
    const brands = document.getElementsByClassName("brand-name");
    for (let i = 0; i < brands.length; i++) {
        if (brands[i].innerHTML.length > 8) {
            brands[i].style.fontSize = "2.7vw";
        }
    }
}

function showProd(prod_id) {
    const index = prod_id - 1;
    window.location.href = "/products/" + String(index);
}

const timer = document.getElementsByClassName("row-1")[0];
if (timer) {
    timer.addEventListener("click", redirect);
}

function redirect() {
    window.location.href = "/";
}

function updateCountdown() {
    const now = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Dhaka" })).getTime();
    const distance = countDownDate - now;

    if (distance < 0) {
        document.getElementsByClassName("row-1")[0].innerHTML = `<p class="timer">Auction is live!</p>`;
        return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("hours").innerHTML = hours;
    document.getElementById("minutes").innerHTML = minutes;
    document.getElementById("seconds").innerHTML = seconds;
    document.getElementById("days").innerHTML = days;
}

// Initial call
updateCountdown();

// Update every second
const interval = setInterval(() => {
    const now = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Dhaka" })).getTime();
    const distance = countDownDate - now;

    if (distance < 0) {
        clearInterval(interval);
        document.getElementsByClassName("row-1")[0].innerHTML = `<p class="timer">Auction has started!</p>`;
        return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("hours").innerHTML = hours;
    document.getElementById("minutes").innerHTML = minutes;
    document.getElementById("seconds").innerHTML = seconds;
    document.getElementById("days").innerHTML = days;
}, 1000);
