var dom = document.getElementById("container");
var myChart = echarts.init(dom);
var app = {};
option = null;
var upColor = '#ec0000';
var upBorderColor = '#8A0000';
var downColor = '#00da3c';
var downBorderColor = '#008F28';
var next_server_stock_daily_list = null;
var next_server_stock_daily_list_answer = null;
var data0 = null;
var is_alert_user_id = 0
// 数据意义：开盘(open)，收盘(close)，最低(lowest)，最高(highest)
option = get_option(server_stock_daily_list)

function splitData(rawData) {
    var categoryData = [];
    var values = []
    for (var i = 0; i < rawData.length; i++) {
        //categoryData.push(rawData[i].splice(0, 1)[0]);
        categoryData.push(rawData[i][0]);
        values.push(rawData[i].slice(1,5))
    }
    return {
        categoryData: categoryData,
        values: values
    };
}

function calculateMA(dayCount) {
    var result = [];
    for (var i = 0, len = data0.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data0.values[i - j][1];
        }
        result.push(sum / dayCount);
    }
    return result;
}

function createUserId(){
        // 检查用户名
    input_user_id = document.getElementById("user_id").value
    if(input_user_id == ""){
        alert("请输入用户名后开始"); 
        return;
    }
    var data = {
            user_id:document.getElementById("user_id").value,
    };
    jQuery.post("/create_admin_skill_id",data,function(rtval){
            if (rtval.err_code == 1){
                document.getElementById("id_create_user_result").innerHTML="创建ID成功"
            }
            else if(rtval.err_code == 2){
                document.getElementById("id_create_user_result").innerHTML="继续之前答题"+rtval.process
            }
            else if(rtval.err_code == 3){
                 document.getElementById("id_create_user_result").innerHTML="userId 冲突，改为新的userId"
                 document.getElementById("user_id").value = rtval.user_id
            }
        },"json");
    document.getElementById("id_create_user_id_button").setAttribute("hidden",true);
    document.getElementById("user_id").setAttribute("disabled",false);
    document.getElementById("id_input_button").removeAttribute("hidden");

}

function submitAnswer(user_answer){
    var result = 0;
    var result_answer = "错误❌"
    if(user_answer == server_params_object.fact){
        result = 1;
        result_answer = "正确⭕️"
    }


    jQuery.ajaxSettings.async = false;
    data = {
            user_id:document.getElementById("user_id").value,
            ts_code:server_params_object.ts_code,
            start_trade_date:server_params_object.start_trade_date,
            end_trade_date:server_params_object.end_trade_date,
            predict_trade_date:server_params_object.predict_trade_date,
            fact:server_params_object.fact,
            user_answer:user_answer,
            result:result,
            detail:""
    };
    jQuery.post("/submit_admin_skill_answer",data,function(rtval){
        // // # 1:表示新的userId，2：表示旧userId 3：表示新生成的userId
        // if (rtval.err_code == 1){
        // }
        // else if (rtval.err_code == 2 && is_alert_user_id == 0) {
        //     alert("继续上次过程. 当天进度"+rtval.process)
        //     is_alert_user_id +=1
        // }
        // else if (rtval.err_code == 3 && is_alert_user_id == 0 ) {
        //     alert("用户名冲突，创建新的userId"+rtval.user_id)
        //     is_alert_user_id +=1
        //     document.getElementById("user_id").value = rtval.user_id
        // }
        // else{
        //     // next_server_stock_daily_list = rtval.stock_daily_list;
        //     // next_server_stock_daily_list_answer = rtval.result_list;
        //     // server_params_object =  rtval.params ;
        //     // var msg = "添加失败，userId 冲突";
        //     // alert(msg);
        // }
        document.getElementById("user_id").value = rtval.user_id
        document.getElementById("id_create_user_result").innerHTML="继续之前答题"+rtval.process
    },"json");

    document.getElementById("id_input_button").setAttribute("hidden",true);
    answer()
    document.getElementById("result_score").innerHTML= result_answer
    document.getElementById("id_next_question").removeAttribute("hidden")

}

function answer(){
    option = get_option(server_stock_daily_list_answer)
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}

function nextQuestion(){
    data = {
            user_id:document.getElementById("user_id").value,
            ts_code:server_params_object.ts_code,
            start_trade_date:server_params_object.start_trade_date,
            end_trade_date:server_params_object.end_trade_date,
            predict_trade_date:server_params_object.predict_trade_date,
            fact:server_params_object.fact,
            detail:""
    };
    jQuery.post("/next_admin_skill_question",data,function(rtval){
        if (rtval.err_code == 0){
            var msg = "添加失败，userId 冲突";
            alert(msg);
        }
        else{
            next_server_stock_daily_list = rtval.stock_daily_list;
            next_server_stock_daily_list_answer = rtval.result_list;
            server_params_object =  rtval.params ;
        }
    },"json");

    option = get_option(next_server_stock_daily_list)
    if (option && typeof option === "object") {
        myChart.clear();
        myChart.setOption(option, true);
    }
    server_stock_daily_list_answer = next_server_stock_daily_list_answer
    // 下一题 按钮 隐藏
    // 涨跌 按钮 展示
    document.getElementById("id_next_question").setAttribute("hidden",true);
    document.getElementById("id_input_button").removeAttribute("hidden")
    document.getElementById("result_score").innerHTML= ""
}



if (option && typeof option === "object") {
    myChart.clear();
    myChart.setOption(option, true);
}

function get_option(data_str_object){
    data0 = splitData(data_str_object);
    option = {
        title: {
            text: '上证指数',
            left: 0
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
        legend: {
            data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
        xAxis: {
            type: 'category',
            data: data0.categoryData,
            scale: true,
            boundaryGap: false,
            axisLine: {onZero: false},
            splitLine: {show: false},
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            scale: true,
            splitArea: {
                show: true
            }
        },
        dataZoom: [
            {
                type: 'inside',
                start: 50,
                end: 100
            },
            {
                show: true,
                type: 'slider',
                top: '90%',
                start: 50,
                end: 100
            }
        ],
        series: [
            {
                name: '日K',
                type: 'candlestick',
                data: data0.values,
                itemStyle: {
                    color: upColor,
                    color0: downColor,
                    borderColor: upBorderColor,
                    borderColor0: downBorderColor
                },
                markPoint: {
                    label: {
                        normal: {
                            formatter: function (param) {
                                return param != null ? Math.round(param.value) : '';
                            }
                        }
                    },
                    data: [
                        {
                            name: 'XX标点',
                            coord: ['2013/5/31', 2300],
                            value: 2300,
                            itemStyle: {
                                color: 'rgb(41,60,85)'
                            }
                        },
                        {
                            name: 'highest value',
                            type: 'max',
                            valueDim: 'highest'
                        },
                        {
                            name: 'lowest value',
                            type: 'min',
                            valueDim: 'lowest'
                        },
                        {
                            name: 'average value on close',
                            type: 'average',
                            valueDim: 'close'
                        }
                    ],
                    tooltip: {
                        formatter: function (param) {
                            return param.name + '<br>' + (param.data.coord || '');
                        }
                    }
                },
                markLine: {
                    symbol: ['none', 'none'],
                    data: [
                        [
                            {
                                name: 'from lowest to highest',
                                type: 'min',
                                valueDim: 'lowest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: false
                                },
                                emphasis: {
                                    label: {
                                        show: false
                                    }
                                }
                            },
                            {
                                type: 'max',
                                valueDim: 'highest',
                                symbol: 'circle',
                                symbolSize: 10,
                                label: {
                                    show: false
                                },
                                emphasis: {
                                    label: {
                                        show: false
                                    }
                                }
                            }
                        ],
                        {
                            name: 'min line on close',
                            type: 'min',
                            valueDim: 'close'
                        },
                        {
                            name: 'max line on close',
                            type: 'max',
                            valueDim: 'close'
                        }
                    ]
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: calculateMA(5),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: calculateMA(10),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: calculateMA(20),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: calculateMA(30),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                }
            },

        ]
    };
    return option;
}

