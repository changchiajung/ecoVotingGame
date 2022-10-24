let inputbox = document.getElementById('inputbox');

function liveRecv(data) {
    console.log(data)
    if (data["image_link"] == "NULL") {
        $("#question_image").attr("src", "/static/generalQuestion/end.png")
        $("#inputbox").remove()
        $("#sendButton").remove()
        $(".btn-primary").css('display', 'inline-block')
        $("._otree-content").append('<button class="otree-btn-next btn btn-primary">下一步</button>')
    } else {
        $("#question_image").attr("src", data["image_link"])
        $("#inputbox").val('')
    }
    setProgress(data["progress"])
    setScore(data["score"], data["total_score"])
    setOptions(data["options"])
}

function setProgress(progressVal) {
    $("#progressbar").css({"width": progressVal + "%"})
    $("#progressbar").html(progressVal + "%")
    $("#progressbar").attr("aria-valuenow", progressVal)
}

function setScore(scoreVal, totalScore) {
    $("#current_score").html(scoreVal + " / " + (totalScore - 1))
}

function setOptions(options) {
    $("#options_area").empty()
    for (let i = 0; i < options.length; i++) {
        let op = options[i]
        $("#options_area").append(
            '<div class="form-check form-check-inline">\n' +
            '        <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio'+op+'" value="'+op+'">\n' +
            '        <label class="form-check-label" for="inlineRadio'+op+'">' + op + '</label>\n' +
            '    </div>'
        )
    }
}

function sendValue() {
    if($('input[name=inlineRadioOptions]:checked').val() != null){
        liveSend($('input[name=inlineRadioOptions]:checked').val());
    }
}

$(document).ready(function () {
    $(".debug-info").css('display', 'none');
    $(".btn-primary").css('display', 'none')
    if ($("#question_image").attr("src") == "/static/generalQuestion/end.png") {
        $("#inputbox").remove()
        $("#sendButton").remove()
        $(".btn-primary").css('display', 'inline-block')
        $("._otree-content").append('<button class="otree-btn-next btn btn-primary">下一步</button>')
        document.getElementsByTagName("html")[0].style.visibility = "visible";
    } else {
        $("#sendButton").css('display', 'inline-block')
        document.getElementsByTagName("html")[0].style.visibility = "visible";
    }
})

function debugFunction(){
    for(let i=0; i<30; i++){
        setTimeout(function () {
            var len = $(".form-check-input").length
            var selectIndex = Math.floor(Math.random(len - 1) * (len - 1));
            $(".form-check-input")[selectIndex].click()
            $("#sendButton").click()
        }, 300)
    }
}