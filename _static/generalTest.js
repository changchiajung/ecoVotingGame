let inputbox = document.getElementById('inputbox');

function liveRecv(data) {
    console.log(data)
    if(data == "NULL"){
        $("#question_image").remove()
        $("#inputbox").val('')

    }else{
        $("#question_image").attr("src", data)
        $("#inputbox").val('')
    }
}

function sendValue() {
    liveSend(inputbox.value);
}
$(document).ready(function () {
    $(".debug-info").css('display', 'none');
})
