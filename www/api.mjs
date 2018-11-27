export async function getPositionRobot() {
    const result = await fetch("/robot/pose");
    
    if(!result.ok){
        throw(result.Error);
    }
    return result.json();
}

export async function postPositionRobot(server){
    const json = JSON.stringify(server);
    const result = await fetch("/robot/pose", {
        method: 'POST',
        body: json,
        headers:{'Content-Type': 'application/json'}
    });
    if(!result.ok){
        throw(result.Error);
    }

    return result.json();
}

export async function postKillRobot(){
    const result = await fetch("/robot/action", {
        method: 'POST',
        body: JSON.stringify({action: "kill"}),
        headers:{'Content-Type': 'application/json'}
    });
    if(!result.ok){
        throw(result.Error);
    }

    return result.json();
}

export async function postMoveHome(){
    const result = await fetch("/robot/action", {
        method: 'POST',
        body: JSON.stringify({action: "home"}),
        headers:{'Content-Type': 'application/json'}
    });
    if(!result.ok){
        throw(result.Error);
    }

    return result.json();
}