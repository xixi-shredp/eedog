const ArgumentType = require('../../extension-support/argument-type');
const BlockType = require('../../extension-support/block-type');
const Cast = require('../../util/cast');
const log = require('../../util/log');

var websocket = new WebSocket('ws://localhost:3000');

websocket.onmessage = function(event) {
    console.log("收到服务器的消息: ", event.data);
};

websocket.onopen = function(event) {
    console.log("与服务器建立连接成功.");
    websocket.send('你好，服务器!');
};
websocket.onclose = function(event) {
    console.log("与服务器断开连接.");
};

websocket.onerror = function(event) {
    console.log("发生错误: ", event);
};

var maxReconnectAttempts = 3;
var reconnectAttempts = 0;
var reconnectInterval = 2000; // 2秒

function wsConnect() {
    websocket.onopen = function () {
        console.log('与服务器连接成功');
        reconnectAttempts = 0;
    };

    websocket.onclose = function (event) {
        console.log('与服务器的连接关闭');
        if(reconnectAttempts < maxReconnectAttempts) {
            console.log('尝试重新连接...');
            setTimeout(connect, reconnectInterval);
            reconnectAttempts++;
        } else {
            console.log('已达到最大重连次数，停止尝试重新连接');
        }
    };
	websocket.onerror = function(event) {
	    console.log("发生错误: ", event);
	};
	websocket.onmessage = function(event) {
	    console.log("收到服务器的消息: ", event.data);
	};
};

// 定义发送数据的函数
function sendData(data) {
    if (websocket.readyState === WebSocket.OPEN) {
        websocket.send(data);
    } else {
        console.log("与服务器的连接没有开启. ");
		wsConnect();
    }
}

class Scratch3EERobot {
    constructor (runtime) {
        this.runtime = runtime;
    }

    getInfo () {
        return {
            id: 'eerobot',
            name: 'EE Robot',
            blocks: [
                {
                    opcode: 'writeLog',
                    blockType: BlockType.COMMAND,
                    text: 'run [cmd]',
                    arguments: {
                        cmd: {
                            type: ArgumentType.STRING,
                            defaultValue: "print('hello world!!!')"
                        }
                    }
                },
                {
                    opcode: 'runPython',
                    blockType: BlockType.COMMAND,
                    text: '打开 [device]',
                    arguments: {
                        device: {
                            type: ArgumentType.STRING,
                            defaultValue: "机器人舵机",
			    menu:"devices"
                        }
                    }
                },
		{
                    opcode: 'move',
                    blockType: BlockType.COMMAND,
                    text: '模式[state] 速度[speed]',
                    arguments: {
                        state: {
                            type: ArgumentType.STRING,
                            defaultValue: '0',
			    menu:'state'
                        },
			speed: {
                            type: ArgumentType.STRING,
                            defaultValue: '0',
			    menu:'speed'
                        }
                    }
                },
		{
                    opcode: 'height',
                    blockType: BlockType.COMMAND,
                    text: '高度[height]mm',
                    arguments: {
                        height: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '110'
                        }
                    }
                },
		{
                    opcode: 'gesture',
                    blockType: BlockType.COMMAND,
                    text: '俯仰角[PIT]° 滚转角[POL]° 后前平移[X]mm',
                    arguments: {
                        PIT: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
			POL: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        },
			X: {
                            type: ArgumentType.NUMBER,
                            defaultValue: '0'
                        }
                    }
                },
		{
                    opcode: 'gait',
                    blockType: BlockType.COMMAND,
                    text: '姿态[gait]模式',
                    arguments: {
                        gait: {
                            type: ArgumentType.STRING,
                            defaultValue: '0',
			    menu:'gait'
                        }
                    }
                }
	    ],
            menus: {
		    devices: {
                    acceptReporters: true,
                    items: [{ text: "机器人舵机", value: "uart"}, {text: "摄像头", value: "camera"}]
                },
		    state: {
                    acceptReporters: true,
                    items: [{ text: "停止", value: "0"}, {text: "左转", value: "1"}, {text: "右转", value: "2"}, {text: "前进", value: "3"}, {text: "后退", value: "4"}]
                },
		    speed: {
                    acceptReporters: true,
                    items: [{ text: "静止", value: "0"}, {text: "1档", value: "1"}, {text: "2档", value: "2"}, {text: "3档", value: "3"}, {text: "4档", value: "4"}, {text: "5档", value: "5"}, {text: "6档", value: "6"}]
                },
                    gait: {
                    acceptReporters: true,
                    items: [{ text: "奔跑", value: "0"}, {text: "行走", value: "1"}]
                }
            }
	};
    }
    writeLog (args) {
        const text = Cast.toString(args.TEXT);
        log.log(text);
    }
    runPython (args) {sendData("Hello!");}
    move (args) {sendData("m,"+args.state+","+args.speed);}
    height (args) {sendData("h,"+args.height);}
    gesture (args) {sendData("g,"+args.PIT+','+args.POL+','+args.X);}
    gait (args) {sendData("a,"+args.gait);}


}

module.exports = Scratch3EERobot;
