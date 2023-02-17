current_value = ""
index = 0
const button = document.getElementById('next_button');
$(document).on("click", "input", function () {
    if ($(this).val() == answersList[index]) {
        if (current_value != $(this).val()) {
            $("#alert_info").css("display", "none")
            $("#explanation_info").css("display", "block")
            $("#explanation_info").html(explanationList[index])
            button.disabled = false;
            if (index == questionList.length - 1){
                $("#next_button").removeAttr("type")
            }

        }
        current_value = $(this).val()
    } else {
        if (current_value != $(this).val()) {
            $("#alert_info").css("display", "block")
            $("#explanation_info").css("display", "none")
            button.disabled = true;
        }
        current_value = $(this).val()
        $("#next_button").attr("type", "button")
    }
})

$(document).on("click", "#next_button", function () {
    console.log($(this).attr("type"))
    if ($(this).attr("type") == "button") {
        // $("#alert_info").css("display", "block")
        index += 1;
        updateQuestion()
    }
})

function updateQuestion() {
    $("#explanation_info").css("display", "none")
    $("input:radio").prop("checked", false)
    current_value = ""
    $("#image_desc_1").html(descList[index][0])
    $("#image_desc_2").html(descList[index][1])
    $("#image_desc_3").html(descList[index][2])
    $("#question").html(questionList[index])
    $("#left_button_label").html(optionsList[index][0])
    $("#right_button_label").html(optionsList[index][1])
    $("#image_1").attr("src", imageList[index][0])
    $("#image_2").attr("src", imageList[index][1])
    if (imageList[index][1] != "") {
        $("#image_2").css("display", "block")
    }
    if (index == questionList.length - 2){
        $("#next_button").html("下一步")
    }
}