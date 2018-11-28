export class Input {
    constructor(){
        this.inputs = [0,0,0,0,0,0];
        this.gamepadIndex = -1;
    }
    
    getInputs() {
        let inputs = this.inputs.slice();
        if(this.gamepadIndex >= 0){
            var gamepad = navigator.getGamepads()[this.gamepadIndex];
            inputs[0] = axisOrDefault(gamepad.axes[1], inputs[0]);
            inputs[1] = axisOrDefault(gamepad.axes[0], inputs[1]);
            inputs[2] = axisOrDefault(gamepad.axes[5], inputs[2]);
            inputs[3] = axisOrDefault(gamepad.axes[2], inputs[3]);
            inputs[4] = buttonsOrDefault(gamepad.buttons[0], gamepad.buttons[2], inputs[4]);
            inputs[5] = buttonsOrDefault(gamepad.buttons[1], gamepad.buttons[3], inputs[5]);
        }

        return inputs
    }

    setup() {
        this.setupButtons();
        this.setupGamepad();
    }
    
    reset() {
        this.inputs = [0,0,0,0,0,0];
    }
    setupButtons(){
        this._setupButtonRow("#add_button_row button", 1);
        this._setupButtonRow("#sub_button_row button", -1);
    }

    _setupButtonRow(selector, value){
        let buttons = document.querySelectorAll(selector);
        var index = 0;
        buttons.forEach(button => {
            var i = index;
            button.addEventListener("mousedown", () => {
                this.inputs[i] = value;
            });
            button.addEventListener("mouseup", () => {
                this.inputs[i] = 0;
            });
            index += 1;
        });
    }

    setupGamepad() {
        let self = this;
        window.addEventListener("gamepadconnected", function(e) {
            console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
              e.gamepad.index, e.gamepad.id,
              e.gamepad.buttons.length, e.gamepad.axes.length);
            if(e.gamepad.id.includes("Generic")){
                self.gamepadIndex = e.gamepad.index;
            }
          });
    }
}

function axisOrDefault(axis, defaultValue){
    if(Math.abs(axis) < 0.01 || isNaN(axis)){
        return defaultValue;
    }
    return axis;
}

function buttonsOrDefault(posetive, negtive, defaultValue){
    var axis = posetive.value + negtive.value * -1;
    return axisOrDefault(axis,defaultValue);
}