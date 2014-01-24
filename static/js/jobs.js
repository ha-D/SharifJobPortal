FADE_SPEED = 400
function applyJob(jobid) {
    $.ajax({
        url:'/jobs/apply/' + jobid,
        type:'get',
        dataType:'json',
        success:function (data, status, error) {
            if (data['done']) {
                $("#applyButton" + jobid).fadeOut(FADE_SPEED, function () {
                    $("#refuseButton" + jobid).fadeIn(FADE_SPEED);
                });
            }

        },

        error:function (xhr, status, error) {
        }
    });
}

function refuseJob(jobid) {
    $.ajax({
        url:'/jobs/refuse/' + jobid,
        type:'get',
        dataType:'json',
        success:function (data, status, error) {
            if (date['done']) {
                $("#refuseButton" + jobid).fadeOut(FADE_SPEED, function () {
                    $("#applyButton" + jobid).fadeIn(FADE_SPEED);
                });
            }

        },

        error:function (xhr, status, error) {
        }
    });
}


function acceptOffer(offerid) {
    $.ajax({
        url:'/jobs/offers/accept/' + offerid,
        type:'get',
        dataType:'json',
        success:function (data, status, error) {
            $("#bothButtons" + offerid).fadeOut(FADE_SPEED, function () {
                $("#acceptText" + offerid).fadeIn(FADE_SPEED);
            });

        },

        error:function (xhr, status, error) {
        }
    });
}

function rejectOffer(offerid) {
    $.ajax({
        url:'/jobs/offers/reject/' + offerid,
        type:'get',
        dataType:'json',
        success:function (data, status, error) {
            $("#bothButtons" + offerid).fadeOut(FADE_SPEED, function () {
                $("#rejectText" + offerid).fadeIn(FADE_SPEED);
            });

        },

        error:function (xhr, status, error) {
        }
    });
}