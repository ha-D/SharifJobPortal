function applyJob(jobid){
    $.ajax({
        url : '/jobs/apply/' + jobid,
        type : 'get',
        dataType : 'json',
        success: function(data, status, error){
            $("#applyButton" + jobid).fadeOut(FADE_SPEED, function(){
                $("#refuseButton" + jobid).fadeIn(FADE_SPEED);
            });

        },

        error: function(xhr, status, error){
        }
    });
}

function refuseJob(jobid){
    $.ajax({
        url : '/jobs/refuse/' + jobid,
        type : 'get',
        dataType : 'json',
        success: function(data, status, error){
            $("#refuseButton" + jobid).fadeOut(FADE_SPEED, function(){
                $("#applyButton" + jobid).fadeIn(FADE_SPEED);
            });

        },

        error: function(xhr, status, error){
        }
    });
}