// 基本回调函数示例
function doSomething(callback) {
    console.log('执行主要任务...');
    // 模拟异步操作
    setTimeout(() => {
        callback('任务完成！');
    }, 2000);
}

// 回调函数
function handleResult(result) {
    console.log('回调结果:', result);
}

// 使用回调
console.log('开始执行...');
doSomething(handleResult);

// 使用箭头函数的回调
doSomething((result) => {
    console.log('使用箭头函数的回调结果:', result);
});

// 带参数的回调示例
function calculate(a, b, callback) {
    const result = a + b;
    callback(result);
}

calculate(5, 3, (sum) => {
    console.log('计算结果:', sum);
});

// 错误处理回调示例
function fetchData(successCallback, errorCallback) {
    // 模拟API调用
    const random = Math.random();
    if (random > 0.5) {
        successCallback({ data: '成功获取数据' });
    } else {
        errorCallback(new Error('获取数据失败'));
    }
}

fetchData(
    (data) => console.log('成功:', data),
    (error) => console.error('错误:', error.message)
); 