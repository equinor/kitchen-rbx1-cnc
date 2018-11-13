export class Server{
    constructor() {
        this._ui = [0,0,0,0,0,0];
        this._server = [0,0,0,0,0,0];
        this._robot = [0,0,0,0,0,0];
        this._busy = true;
        this._serverLoop();
    }

    updateUi(ui){
        this._ui = ui.slice();
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
                console.log("step");
                try{
                    let json;
                    if(self._busy){
                        json = await getRobot();
                    }else{
                        json = await postRobot(self._ui);
                    }
                    self._server = json.targetPos;
                    self._robot = json.currentPos;
                    self._busy = json.busy;
                } catch (error){
                    console.error(error)
                }
                await delay();
            }
        }
        loop();
    }
}

async function getRobot() {
    const result = await fetch("/robot");
    
    if(!result.ok){
        throw(result.Error);
    }
    return await result.json();
}

async function postRobot(server){
    const json = JSON.stringify(server);
    const result = await fetch("/robot", {
        method: 'POST',
        body: json,
        headers:{'Content-Type': 'application/json'}
    });
    if(!result.ok){
        throw(result.Error);
    }

    return await result.json();
}

function delay(){
    return new Promise(function(resolve) {
        setTimeout(resolve, 250);
    });
}