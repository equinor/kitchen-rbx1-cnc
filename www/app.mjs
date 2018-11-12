let plussButtons = [false,false,false,false,false,false];
let minusButtons = [false,false,false,false,false,false];
let uiPos = [0,0,0,0,0,0];
let serverPos = [0,0,0,0,0,0];
let robotPos = [0,0,0,0,0,0];

// setup buttons
function setupButtons() {
    let buttons = document.querySelectorAll("#add_button_row button");
    var index = 0;
    buttons.forEach(button => {
        var i = index;
        button.addEventListener("mousedown", e => plussButtons[i] = true);
        button.addEventListener("mouseup", e => plussButtons[i] = false);
        index += 1;
    });

    buttons = document.querySelectorAll("#sub_button_row button");
    index = 0;
    buttons.forEach(button => {
        var i = index;
        button.addEventListener("mousedown", e => minusButtons[i] = true);
        button.addEventListener("mouseup", e => minusButtons[i] = false);
        index += 1;
    });
}
setupButtons();

function updateUiPos(){
    let pluss = plussButtons.map(p => p ? 1 : 0);
    let minus = minusButtons.map(m => m ? -1 : 0);
    uiPos = pluss.map((v, i) => v + minus[i]);
}

function showUiPos(){
    for (let i = 0; i < uiPos.length; i++) {
        let elem = document.getElementById("ui"+ (i + 1))
        elem.textContent = uiPos[i].toString();
    }
}

function step(timestamp){
    updateUiPos();
    showUiPos();
    window.requestAnimationFrame(step);
}

window.requestAnimationFrame(step);
