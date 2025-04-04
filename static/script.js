async function startRecognition() {
    const response = await fetch("/recognize-audio", { method: "POST" });
    const data = await response.json();
    document.getElementById("result").innerText = "You said: " + data.recognized_text;
}

async function textToSpeech() {
    const text = document.getElementById("result").innerText.replace("You said: ", "");
    const response = await fetch("/speak-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    });
    const data = await response.json();
    console.log(data.message);
}
