async function userLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("access_token", data.access_token);
        document.getElementById("responseMessage").innerText = "Login successful!";
    } else {
        document.getElementById("responseMessage").innerText = data.message;
    }
}

async function registerUser() {
    const username = document.getElementById("registerusername").value;
    const password = document.getElementById("registerpassword").value;
    const repassword= document.getElementById("reregisterpassword").value;

    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password,
            repassword: repassword
        })
    });

    const data = await response.json();

    document.getElementById("responseMessage").innerText = data.message;
}


