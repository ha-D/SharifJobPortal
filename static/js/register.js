
// $(document).ready(relaxRegister);

// function relaxRegister() {
//     basicInfoRelax();
//     skillsRelax();
//     finalRelax();
// }
var register = {}

var fadeSpeed = 200;

register.baseURL = '/register/';
register.baseAjaxURL = register.baseURL + 'ajax/';
register.step = 0;

register.init = function(){
    function init(){
        $.ajax({
            url: register.baseURL + 'steps',
            dataType: 'json',
            success: function(data){
                register.steps = data.steps;
                initSammy();
            }
        })
    }
    
    function initSammy(){
        Sammy(function() {
            this.get('#:step', function() {
                if(register.steps.indexOf(this.params.step) != -1) {
                    register.loadForm(this.params.step);
                }
            });
            this.get('', function() { 
                location.hash = register.steps[0];
            });
        }).run();
    }

    $('.register').on('click', '.step', function(){
        if($(this).hasClass('disabled'))
            return;
        var step = $(this).attr('id').slice(0, -5);
        location.hash = step;
    })

    init();
}

register.loadForm = function(param){
    console.log("Loading form " + param);
    $("#dimmer").dimmer("show");
    param = param || 'user-info';
    $.ajax({
        url: register.baseAjaxURL + "?step=" + param,
        type: 'get',
        dataType: 'json',
        success: function(data){
            $("#register-form").html(data.data);
            register.step = register.steps.indexOf(param);

            $('.ui.step').removeClass('active');
            for(var i = 0; i < register.steps.length; i++){
                $("#" + register.steps[i] + "_step").removeClass("disabled");
                $("#" + register.steps[i] + "_step").addClass("active");
                if(register.steps[i] == param)
                    break;
            }

            register.initForm();
        },
        error: function(err){
            console.log(err);
        },
        complete: function(){
            $("#dimmer").dimmer("hide");
        }
    });
}


register.submitForm = function(){
    var param = register.steps[register.step];
    $("#dimmer").dimmer("show");
    $("#register-form").ajaxSubmit({
        url: register.baseAjaxURL + "?step=" + param,
        type: 'post',
        dataType: 'json',
        success: function(data){
            console.log("WHAT THE FUCK?!")
            if(data.result == 1) {
                console.log("SUBMIT ReSULT 1")
                location.hash = register.steps[register.step + 1];
                console.log("CHanging hash to");
                console.log(location.hash);
            }else{
                console.log("ERROR IN FORM")
                $("#register-form").html(data.data);
                register.initForm();
                $("#dimmer").dimmer("hide");
            }
        },
        error: function(err){
            console.log(err);
            console.log("FUUCJ ERROR")
            $("#dimmer").dimmer("hide");
        },
        complete: function(){
            console.log("FUUUUCK  COMPLETE");
        }
    })
}

register.initForm = function(){
    $(".next.button").click(register.submitForm);
    $('.ui.checkbox').checkbox();
}

register.initUserInfo = function(){
    function basicInfoRelax(){
        basicInfoValidation();
    }

    function basicInfoValidation() {
        $('.ui.form.basicinfo')
            .form({
                firstName:{
                    identifier:'first_name',
                    rules:[
                        {
                            type:'empty',
                            prompt:'لطفا نام خود را وارد کنید.'
                        }
                    ]
                },
                lastName:{
                    identifier:'last_name',
                    rules:[
                        {
                            type:'empty',
                            prompt:'لطفا نام خانوادگی خود را وارد کنید.'
                        }
                    ]
                },
                username:{
                    identifier:'username',
                    rules:[
                        {
                            type:'empty',
                            prompt:'لطفا یک نام کاربری وارد کنید.'
                        }
                    ]
                },
                password:{
                    identifier:'password',
                    rules:[
                        {
                            type:'length[6]',
                            prompt:'رمز عبور شما باید حداقل ۶ حرف داشته باشد.'
                        }
                    ]
                },
                email:{
                    identifier:'email',
                    rules:[
                        {
                            type:'email',
                            prompt:'لطفا یک آدرس الکترونیکی معتبر وارد کنید.'
                        }
                    ]
                },
                emailrepeat:{
                    identifier:'password-repeat',
                    rules:[
                        {
                            type:'match[password]',
                            prompt:'دو رمزعبور وارد شده یکسان نیستند.'
                        }
                    ]
                }
            },
            {
                inline:true,
                // onSuccess: register.submitForm,
                on:'blur'
            }
        );
    }

    basicInfoRelax();
}


register.initSkills = function(){
    $(".next.button").click(register.submitForm);
    $('.ui.checkbox').checkbox();
}


$(function(){


    

  

    

  

    function skillsRelax(){
        $("#skillsStep").click("skills", stepClicked);
        $("#searchPossibleSkills").change(updatePossibleSkillsList);
        $("#searchCurrentSkills").change(updateCurrentSkillsList);
        $(".ui.form.skills .button.proceed").click( proceedToFinal );
        $(".ui.form.skills .button.skip").click( skipToFinal );
    }

    function finalRelax(){
        $("#finalStep").click("final", stepClicked);
        finalValidation();
        $("#terms").click( function(){
            $("#termsModal").modal("show");
        });
    }

    function finalValidation(){
        $('.ui.form.final')
            .form({
               terms:{
                   identifier:'terms',
                   rules:[
                       {
                           type:'checked',
                           prompt:'برای ثبت‌نام تایید قوانین لازم است.'
                       }
                   ]
               }
            },
            {
                inline: true,
                onSuccess: accountCreate
            });
    }

    function accountCreate(){
    }
    

    function proceedToSkills() {
        $("#skillsStep").removeClass("disabled");
        stepClicked({data: "skills"});
    }

    function stepClicked(step){
        stepID = "#" + step.data + "Step";
        if ($(stepID).hasClass("active") ||
            $(stepID).hasClass("disabled"))
            return;
        formClass = ".ui.form." + step.data;
        $(".ui.form.visible").fadeOut(fadeSpeed, function(){
            $(".ui.form.visible").removeClass("visible").addClass("hide");
            $(formClass).removeClass("hide").addClass("visible");
            $(formClass).fadeIn(fadeSpeed);
            $(".ui.step").removeClass("active");
            $(stepID).addClass("active");
        });
    }

    function updatePossibleSkillsList(){
        $("#loadingPossibleSkills").addClass("active");
        setTimeout("$('#loadingPossibleSkills').removeClass('active')", 1500);
    }
    function updateCurrentSkillsList(){
        $("#loadingCurrentSkills").addClass("active");
        setTimeout("$('#loadingCurrentSkills').removeClass('active')", 1500);
    }

    function proceedToFinal(){
        skipToFinal();
    }

    function skipToFinal(){
        $("#finalStep").removeClass("disabled");
        stepClicked({data: "final"});
    }
});

$(function(){
    register.init();
});