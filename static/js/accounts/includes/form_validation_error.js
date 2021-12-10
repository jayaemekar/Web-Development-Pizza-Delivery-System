var error_div = document.querySelector("#errorDiv");
var close_btn = document.querySelector("#outer");

close_btn.addEventListener("click", (e) => {
    error_div.remove();
});