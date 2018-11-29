import { getPositionRobot, postPositionRobot } from "./api.mjs";

export class Server{
    constructor() {
        this._ui = [0,0,0,0,0,0,0];
        this._server = [0,0,0,0,0,0,0];
        this._robot = [0,0,0,0,0,0,0];
        this._newPose = false;
        this._serverLoop();
    }

    updateUi(ui){
        if (this._isEqual(this._ui, ui)) return;
        this._ui = ui.slice();
        this._newPose = true;
    }

    get server() {
        return this._server.slice();
    }

    get robot() {
        return this._robot.slice();
    }

    _serverLoop() {
        let self = this;
        async function loop(){
            while(true){
                try{
                    let json = await getPositionRobot();
                    if (self._newPose) {
                        await postPositionRobot(self._ui);
                    }
                    self._server = json.targetPos;
                    self._robot = json.currentPos;
                    self._newPose = false;
                } catch (error){
                    console.error(error)
                }
                await delay();
            }
        }
        loop();
    }

    _isEqual(prevUi, ui) {
        return JSON.stringify(prevUi) === JSON.stringify(ui)
    }
}


function delay(){
    return new Promise(function(resolve) {
        setTimeout(resolve, 500);
    });
}