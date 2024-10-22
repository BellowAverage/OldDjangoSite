// 现在，我们可以检查 userIP 是否在 trustedIPs 中
if (trustedIPs.includes(userIP)) {
    // IP 地址是受信任的，不需要密码验证
    password_necessity = 0;
    var encrypted_blog_elements = document.getElementsByClassName("encrypted_blog");
    for (var i = 0; i < encrypted_blog_elements.length; i++) {
        encrypted_blog_elements[i].style.display = "none"; // 隐藏链接
    }

    var encrypted_unlock_elements = document.getElementsByClassName("encrypted_unlock");
    for (var i = 0; i < encrypted_unlock_elements.length; i++) {
        encrypted_unlock_elements[i].style.display = "inline-block"; // 显示链接
    }
    document.getElementById("password_verify").style.display = "none";

    // 显示成功消息并触发动画
    var successMessage = document.getElementById("success_message");
    successMessage.classList.remove("hidden");

    // 清除动画以便下次再次触发
    successMessage.addEventListener("animationend", function () {
        successMessage.style.animation = "none";
    });
} else {
    // IP 地址不受信任，需要密码验证
    var password_necessity = 1;
}

document.addEventListener("DOMContentLoaded", function () {
    // 获取所有的博客项
    var blogItems = document.querySelectorAll(".blog-box");

    // 获取筛选按钮
    var techFilterBtn = document.getElementById("techFilter");
    var showAllBtn = document.getElementById("showAll");
    var busFilterBtn = document.getElementById("busFilter");

    // 添加筛选按钮的点击事件处理程序
    techFilterBtn.addEventListener("click", function () {
        // 隐藏所有博客项
        blogItems.forEach(function (item) {
            item.style.display = "none";
        });

        // 显示符合条件的博客项
        blogItems.forEach(function (item) {
            if (item.classList.contains("tech")) {
                item.style.display = "block";
            }
        });

        var filterButtons = document.querySelectorAll("#filterBtn li");

        filterButtons.forEach(function (btn) {
            btn.classList.remove("active");
        });

        techFilterBtn.classList.add("active")
    });

    busFilterBtn.addEventListener("click", function () {
        // 隐藏所有博客项
        blogItems.forEach(function (item) {
            item.style.display = "none";
        });

        // 显示符合条件的博客项
        blogItems.forEach(function (item) {
            if (item.classList.contains("bus")) {
                item.style.display = "block";
            }
        });

        var filterButtons = document.querySelectorAll("#filterBtn li");

        filterButtons.forEach(function (btn) {
            btn.classList.remove("active");
        });

        busFilterBtn.classList.add("active")
    });

    // 添加"Show All"按钮的点击事件处理程序
    showAllBtn.addEventListener("click", function () {
        // 显示所有博客项
        blogItems.forEach(function (item) {
            item.style.display = "block";
        });
        var filterButtons = document.querySelectorAll("#filterBtn li");

        filterButtons.forEach(function (btn) {
            btn.classList.remove("active");
        });

        showAllBtn.classList.add("active")
    });
});


function checkPassword() {
    var passwordInput = document.getElementById("password").value;
    // 在这里进行密码验证，这里只是一个示例，你需要替换成你自己的验证逻辑
    if (passwordInput === "123") {
        // 使用 document.getElementsByClassName 得到的是一个 HTMLCollection，需要遍历设置样式
        var encrypted_blog_elements = document.getElementsByClassName("encrypted_blog");
        for (var i = 0; i < encrypted_blog_elements.length; i++) {
            encrypted_blog_elements[i].style.display = "none"; // 隐藏链接
        }

        var encrypted_unlock_elements = document.getElementsByClassName("encrypted_unlock");
        for (var i = 0; i < encrypted_unlock_elements.length; i++) {
            encrypted_unlock_elements[i].style.display = "inline-block"; // 显示链接
        }
        document.getElementById("password_verify").style.display = "none";

        // 显示成功消息并触发动画
        var successMessage = document.getElementById("success_message");
        successMessage.classList.remove("hidden");

        // 清除动画以便下次再次触发
        successMessage.addEventListener("animationend", function () {
            successMessage.style.animation = "none";
        });

        fetch('call_backend_function', {
            method: 'GET', // 或 'POST'，具体取决于后端的需求
            headers: {
                'Content-Type': 'application/json', // 根据后端要求设置请求头
            },
        })
    } else {
        alert("密码不正确，请重试！");
    }
}

