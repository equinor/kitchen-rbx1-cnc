import { Input } from "./input.mjs";
import { Server } from "./server.mjs";
import { postKillRobot, postMoveHome } from "./api.mjs";
const input = new Input();
input.setup();

const server = new Server();
setupSpecialButtons();

function showValues(values, prefix){
    for (let i = 0; i < 6; i++) {
        let elem = document.getElementById(prefix+ (i + 1))
        elem.textContent = values[i].toFixed(2);
    } 
}

function setupSpecialButtons() {
    const toggleButton = document.getElementById("toggle-image");
    toggleButton.addEventListener("mousedown", () => {
        const image = document.getElementById("camera-image-1");
        const vis = image.style.visibility === "hidden" ? "visible" : "hidden";
        image.style.visibility = vis;
    });

    const killButton = document.getElementById("kill");
    killButton.addEventListener("mousedown", () => {
        postKillRobot();
    });

    const moveButton = document.getElementById("home");
    moveButton.addEventListener("mousedown", () => {
        postMoveHome();
    });

}

let uiPos = [0,0,0,0,0,0,-1];
const SPEED = 1/15;
function updateUIPos(inputs, time){
    uiPos = uiPos.map((v,i) =>{
        v += inputs[i] * time * SPEED;
        if(v > 1) return 1;
        if(v < -1) return -1;
        return v;
    })
}

let last = null;

function step(timestamp){
    if (!last) last = timestamp;
    let time = (timestamp - last) / 1000;
    last = timestamp

    updateUIPos(input.getInputs(), time);
    server.updateUi(uiPos);

    showValues(uiPos, "ui");
    showValues(server.server, "s");
    showValues(server.robot, "r");
    window.requestAnimationFrame(step);
}

window.requestAnimationFrame(step);
