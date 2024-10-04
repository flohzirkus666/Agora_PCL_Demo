// Event listener for form submit
submitBtn.addEventListener("click", (e) => createShare(e));

let createShare = async (e) => {
    // Unicorn dust - narf!
    e.preventDefault();
    buttonModifier("disable");

    let response = await fetch("/create", {
        method: "POST",
        body: new FormData(smb_order_form)
    });

    const alertBox = document.getElementById("alert_box");
    const alertText = document.getElementById("alert_text");

    switch (response.status) {
        case 200:
            alertBox.classList.remove("visually-hidden", "alert-danger");
            alertBox.classList.add("alert-success");
            alertText.innerHTML = "Share has been created!";
            break;
        default:
            alertBox.classList.remove("visually-hidden", "alert-success");
            alertBox.classList.add("alert-danger");
            alertText.innerHTML = "Oops, something went wrong!";
            break;
    };

    buttonModifier("enable");
    sleep(5000).then(() => { alertBox.classList.add("visually-hidden"); })
};

let sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

let buttonModifier = (param) => {
    // Enable / disable submit button
    const button = document.getElementById("submitBtn");

    switch (param) {
        case "disable":
            button.classList.add("disabled");
            button.innerText = "Processing..."
            break;
        case "enable":
            button.classList.remove("disabled");
            button.innerText = "Make me happy!"
            break;
        default:
            alert("Narf!");
    }
}