import { Input } from "./input.mjs";

const input = new Input();
input.setup();

function showUiPos(inputs){
    for (let i = 0; i < inputs.length; i++) {
        let elem = document.getElementById("ui"+ (i + 1))
        elem.textContent = inputs[i].toFixed(3);
    }
}

let uiPos = [0,0,0,0,0,0];
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

    showUiPos(uiPos);
    window.requestAnimationFrame(step);
}

window.requestAnimationFrame(step);
