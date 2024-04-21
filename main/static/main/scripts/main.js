const context = canvas.getContext("2d");
const video = document.getElementById("video");
const img = document.getElementById("client");
const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const uuid = generateUUID();
let mode = true;

video.width = 640;
video.height = 360;

// generate a uuid for each client so that they can establish their own websocket connection
function generateUUID() {
  const getRandomHex = () => {
    return Math.floor(Math.random() * 16).toString(16);
  };

  const sections = [8, 4, 4, 4, 12];

  const uuid = sections
    .map((section) => {
      return Array.from({ length: section }, getRandomHex).join("");
    })
    .join("-");

  return uuid;
}

function Mode() {
  if (mode) {
    // changing the button text
    document.getElementById("modeButton").textContent = "Stop";

    mode = false;
    const selectedModel = document.getElementById("optionsDropdown").value;
    const ws = new WebSocket(
      `${ws_scheme}://${window.location.host}/ws/stream/${uuid}/?mode=${selectedModel}`
    );
    ws.onopen = (event) => {
      console.log("WebSocket connected!!!");
    };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      frameUpdate = data["image"];
      img.src = "data:image/jpeg;base64," + frameUpdate;
    };
    ws.onclose = (event) => {
      console.log("WebSocket closed");
    };

    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
          video.srcObject = stream;
          video.play();
          const width = video.width;
          const height = video.height;
          const delay = 100;

          setInterval(function () {
            context.drawImage(video, 0, 0, width, height);
            canvas.toBlob(function (blob) {
              if (ws.readyState == WebSocket.OPEN) {
                if (mode) {
                  ws.send(new Uint8Array([]));
                } else {
                  ws.send(blob);
                }
              }
            }, "image/jpeg");
          }, delay);
        });
    }
  } else {
    // changing the button text
    document.getElementById("modeButton").textContent = "Start";

    mode = true;
    video.pause();
    video.srcObject.getVideoTracks()[0].stop();
    video.srcObject = null;
  }
}
