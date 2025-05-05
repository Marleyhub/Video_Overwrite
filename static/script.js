async function processAudio() {
    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("output").innerText = "";

    const url = document.getElementById("url").value;
    const name = document.getElementById("name").value;

    const response = await fetch("http://localhost:5000/process", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, name })
    });

    const data = await response.json();
    document.getElementById("loading").classList.add("hidden");

    if (data.error) {
      document.getElementById("output").innerText = "❌ " + data.error;
    } else {
      document.getElementById("output").innerText =
        "✅ Transcription:\n" + data.transcript + "\n\n📋 \n" +
        "✅Summary:\n" + data.summary + "\n\n📋 \n";
    }
  }
  