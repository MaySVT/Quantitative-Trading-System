<template>
<link href="css/index.css" type="text/css" rel="stylesheet"/>
<link href="css/Registered.css" type="text/css" rel="stylesheet"/>
<!--Registered-->
        <div id="Registered">
            <div class="box" id="box">
                <span class="Registeredfont">Registered</span>
                <form method="post" action="#">
                    <table>
                        <br>
                        <tr>
                            <td width="300"><input type="text" class="input" placeholder="用户名"></td>
                        </tr>
                        <tr>
                            <td><input type="password" class="input" placeholder="密码"></td>
                        </tr>
                        <tr>
                            <td><input type="password" class="input" placeholder="再次输入密码"></td>
                        </tr>
                        <tr>
                            <td width="300"><input type="text" class="input" placeholder="电子邮箱"></td>
                        </tr>
                        <br>
                        <tr>
                            <td><button type="submit" id="login-button">立即注册</button></td>
                        </tr>
                    </table>
                </form>
            </div>
            <div class="Registeredboxbg"></div>
            <div class="boxbackground"></div>
        </div>
</template>
<style scoped>
#Registered{
    position:absolute;
    top:20%;
    left:45%;
}
#login-button{
    position:relative;
    left:50px;
}
.Registeredfont{
    position:relative;
    left:40px;
    text-align: center;
    font-size:large;
    font-weight: bold;
}
</style>