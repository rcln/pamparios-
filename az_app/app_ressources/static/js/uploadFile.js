
$(document).ready(function(){


    $('.opt_doc').on('click', function(){


//        alert('ETAPE 1 BIEN!!!');

        location.href = '/extracted/'+$(this).val()+'/';


    });

    $('.opt').on('click', function(){

//        var split_text = location.href.split('http://localhost:5000/extracted/');
//        var split_result = split_text[1]
//        alert(split_text[1]);
        location.href = '/extracted/' + $('#hidden_name').text() + '/' + $(this).text()+'/'


    });


});

