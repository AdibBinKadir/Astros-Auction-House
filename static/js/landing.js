function showProd() {
    window.location.href = `/products/${index}`;
}

function redirect() {
    window.location.href = "/";
}

function load() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("main").style.display = "block";
}

function updateCountdown() {
    const now = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Dhaka" })).getTime();
    const distance = countDownDate - now;

    const timerRow = document.querySelector(".row-1");

    if (distance < -30 * 60 * 1000) {
        clearInterval(timerInterval);
        timerRow.innerHTML = `<p class="timer">Auction has ended!</p>`;
        return;
    }

    if (distance < 0) {
        timerRow.innerHTML = `<p class="timer">Auction has started!</p>`;
        return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("days").textContent = days;
    document.getElementById("hours").textContent = hours;
    document.getElementById("minutes").textContent = minutes;
    document.getElementById("seconds").textContent = seconds;
}

function setupNavigation() {
    const right = document.getElementById("right");
    const left = document.getElementById("left");

    if (right) {
        right.onclick = () => window.location.href = `/landing/${index + 1}`;
    }

    if (left) {
        const prevIndex = Math.max(index - 1, 0);
        left.onclick = () => window.location.href = `/landing/${prevIndex}`;
    }

    const timerRow = document.querySelector(".row-1");
    if (timerRow) {
        timerRow.addEventListener("click", redirect);
    }
}

let timerInterval;

document.addEventListener("DOMContentLoaded", () => {
    setupNavigation();
    updateCountdown(); // initial call
    timerInterval = setInterval(updateCountdown, 1000);
});
