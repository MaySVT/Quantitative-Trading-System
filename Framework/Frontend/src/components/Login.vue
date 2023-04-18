<template>
    <!--login-->
    <div id="login">
        <div class="box" id="box">
            <span class="Registeredfont">Login</span>
            <form method="post" action="#">
                <table>
                    <br>
                    <tr>
                        <td width="200"><input type="text" class="input" placeholder="帐号"></td>
                    </tr>
                    <tr>
                        <td><input type="password" class="input" placeholder="密码"></td>
                    </tr>
                    <br>
                    <tr>
                        <td><button type="submit" id="login-button">登入</button></td>
                    </tr>
                </table>
            </form>
        </div>
        <div class="Loginboxbg"></div>
        <div class="boxbackground"></div>
    </div>

<br /> 
</template>
<style scoped>
#login{
    position:absolute;
    top:20%;
    left:45%;
}
#login-button{
    position:relative;
    left:60px;
}
.Registeredfont{
    position:relative;
    left:50px;
    text-align: center;
    font-size:large;
    font-weight: bold;
}
</style>