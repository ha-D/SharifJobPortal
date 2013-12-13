fadeSpeed = 200;

$(document).ready(relaxRegister);

function relaxRegister() {
    basicInfoRelax();
    skillsRelax();
    finalRelax();
}

function basicInfoRelax(){
    $("#basicinfoStep").click("basicinfo", stepClicked);
    basicInfoValidation();
}

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
    alert('hey');
}
function basicInfoValidation() {
    $('.ui.form.basicinfo')
        .form({
            firstName:{
                identifier:'firstname',
                rules:[
                    {
                        type:'empty',
                        prompt:'لطفا نام خود را وارد کنید.'
                    }
                ]
            },
            lastName:{
                identifier:'lastname',
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
            on:'blur',
            onSuccess: proceedToSkills
        }
    );
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
        $(".ui.form.visible").removeClass("visible").addClass("hidden");
        $(formClass).removeClass("hidden").addClass("visible");
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