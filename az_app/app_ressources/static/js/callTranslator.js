$(document).ready(function(){

    // This script is called on the click of the button "Translate of the translation page (plateform)

    $('#translate').on('click', function(){

        // Here we get the primary language and the secondary language
        var main_lang = $("#main").val()
        var translate_lang = $("#trans").val()


        $.ajax({

            // With the Ajax request we pass this values to the view "/ocr/traduct/" in file "az_app/views/admin_views_route.py" and on success of the request we
            // put the answer (the translation) to the textarea of the secondary language

            url: "/ocr/traduct/",
            type: "POST",
            data: {phrase: $("#given").val(), prem_langu: main_lang, secon_langu: translate_lang},
            success: function(result,status,xhr){
                $("#translated").val(result);

            }
            

        });

    });


});