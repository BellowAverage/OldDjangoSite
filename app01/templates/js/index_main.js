// window.onload = function() {
//   // 获取页面上的所有组件（这里假设所有组件都有 class="component"）
//   var components = document.querySelectorAll('.component');
//
//   // 遍历所有组件并添加淡入效果
//   components.forEach(function(element) {
//     element.style.opacity = '0'; // 初始设置透明度为0
//
//     var fadeEffect = setInterval(function () {
//       if (element.style.opacity < 1) {
//         element.style.opacity = (parseFloat(element.style.opacity) + 0.1).toString();
//       } else {
//         clearInterval(fadeEffect);
//       }
//     }, 50); // 将时间间隔设置为200毫秒（2秒除以10步骤）
//   });
// }