$(document).ready(relaxLogin);

function relaxLogin() {
    loginValidation();
}

function loginValidation() {
    $('.ui.form.login')
        .form({
            username:{
                identifier:'username',
                rules:[
                    {
                        type:'empty',
                        prompt:'لطفا نام کاربری را وارد کنید.'
                    }
                ]
            },
            password:{
                identifier:'password',
                rules:[
                    {
                        type:'empty',
                        prompt:'لطفا رمزعبور را وارد کنید.'
                    }
                ]
            }
        },
        {
            inline:true,
            onSuccess: submitLogin
        }
    );
}

function submitLogin(){
    $("#login-form").submit();
}