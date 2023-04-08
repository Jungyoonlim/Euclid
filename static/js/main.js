document.getElementById("math-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const user_input = document.getElementById("user_input").value;
    const response = await fetch("/", {
        method: "POST",
        body: new FormData(e.target),
    });
    const data = await response.json();
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = JSON.stringify(data, null, 2);
});
