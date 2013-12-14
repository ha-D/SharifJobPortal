fadeSpeed = 200;

$(document).ready(relaxRegister);

function relaxRegister() {
    companyRelax();
    personRelax();
    finalRelax();
}

function personRelax(){
    $("#personStep").click("person", stepClicked);
    personinfoValidation();
}

function companyRelax(){
    $("#companyStep").click("company", stepClicked);
    companyinfoValidation();
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

function companyinfoValidation() {
    $('.ui.form.company')
        .form({
            name:{
                identifier:'name',
                rules:[
                    {
                        type:'empty',
                        prompt:'لطفا نام شرکت را وارد کنید.'
                    }
                ]
            },
            address:{
                identifier:'address',
                rules:[
                    {
                        type:'empty',
                        prompt:'لطفا آدرس شرکت را وارد کنید.'
                    }
                ]
            },
            phone:{
                identifier:'phone',
                rules:[
                    {
                        type:'empty',
                        prompt:'لطفا شماره تماس شرکت وارد کنید.'
                    }
                ]
            },
            number:{
                identifier:'registerNumber',
                rules:[
                    {
                        type:'empty',
                        prompt:'لطفا شماره ثبت شرکت را وارد کنید.'
                    }
                ]
            },
            since:{
                identifier:'since',
                rules:[
                    {
                        type:'empty',
                        prompt:'سال تاسیس شرکت را وارد کنید.'
                    }
                ]
            }
        },
        {
            inline:true,
            on:'blur',
            onSuccess: proceedToPerson
        }
    );
}


function personinfoValidation() {
    $('.ui.form.person')
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
            onSuccess: proceedToFinal
        }
    );
}

function proceedToPerson(){
    $("#personStep").removeClass("disabled");
    stepClicked({data: "person"});
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
    $("#finalStep").removeClass("disabled");
    stepClicked({data: "final"});
}
