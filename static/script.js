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

    function processAudio() {
        // Show loading text 
        document.getElementById("loading").classList.remove("hidden");
        document.getElementById("output").classList.add("hidden");
      
        // Simulate an async process (replace this with your actual API call or logic)
        setTimeout(() => {
          // Your actual processing logic here
      
          // Hide loading text and show output when done
          document.getElementById("loading").classList.add("hidden");
          document.getElementById("output").classList.remove("hidden");
      
          // Display some results
          document.getElementById("output").textContent = "Processing Complete!";
        }, 2000); // Simulating a 2-second process for demonstration
      }

    if (data.error) {
      document.getElementById("output").innerText = "❌ " + data.error;
    } else {
      document.getElementById("output").innerText =
        "✅ Transcription:\n" + data.transcript + "\n\n📋 \n" +
        "✅Summary:\n" + data.summary + "\n\n📋 \n";
    }
  }
  