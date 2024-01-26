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
                    opcode: 'loadAIModule',
                    blockType: BlockType.COMMAND,
                    text: 'load AI Module'
                },
                {
                    opcode: 'getRight',
                    blockType: BlockType.BOOLEAN,
                    text: '识别人脸右转'
                },
                {
                    opcode: 'turnLeft',
                    blockType: BlockType.COMMAND,
                    text: '机器狗左转'
                },
                {
                    opcode: 'turnRight',
                    blockType: BlockType.COMMAND,
                    text: '机器狗右转'
                }
            ],
            menus: {
				devices: {
                    acceptReporters: true,
                    items: [{ text: "机器人舵机", value: "uart"}, {text: "摄像头", value: "camera"}]
                }
            }
        };
    }
    writeLog (args) {
        const text = Cast.toString(args.TEXT);
        log.log(text);
    }
	runPython (args){
		sendData("hello");
	}
}

module.exports = Scratch3EERobot;
