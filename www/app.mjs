import { Input } from "./input.mjs";
import { Server } from "./server.mjs";

const input = new Input();
input.setup();

const server = new Server();

function showValues(values, prefix){
    for (let i = 0; i < 6; i++) {
        let elem = document.getElementById(prefix+ (i + 1))
        elem.textContent = values[i].toFixed(2);
    } 
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
