import { Input } from "./input.mjs";

const input = new Input();
input.setup();

function showUiPos(inputs){
    for (let i = 0; i < inputs.length; i++) {
        let elem = document.getElementById("ui"+ (i + 1))
        elem.textContent = inputs[i].toFixed(3);
    }
}

function step(timestamp){
    showUiPos(input.getInputs());
    window.requestAnimationFrame(step);
}

window.requestAnimationFrame(step);
