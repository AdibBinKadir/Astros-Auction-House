document.addEventListener("DOMContentLoaded", function () {
  var logo = document.getElementsByClassName('navbar-img')[0];
  if (logo) {
    logo.addEventListener('click', function () {
      window.location.href = "/";
    });
  }

  var log1 = document.getElementById('login');
  var log2 = document.getElementById('logout');

  if (log2) {
    log2.addEventListener('click', function () {
      window.location.href = "/login/logout_user";
    });
  } else if (log1) {
    log1.addEventListener('click', function () {
      window.location.href = "/login";
    });
  }
});
