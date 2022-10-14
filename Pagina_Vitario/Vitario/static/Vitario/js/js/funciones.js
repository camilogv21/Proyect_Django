function confirmarEliminar(url){


    if (confirm("Estas seguro que quieres eliminar este contenido?")){
        location.href = url;
    }
        
    
}

function buscarA(url){
    console.log(url);
    b = $('#buscar').val();
    r = $('#res');
    t = $('input[name="csrfmiddlewaretoken"]').val();
    console.log(t)
    // buscar = document.getElementById("buscar").value;
    // console.log(buscar);
    // console.log( buscar.val() );
    $.ajax({

        url: url,
        type: 'post',
        data: {"buscar": b, "csrfmiddlewaretoken": t },
        success: function(res){
            //console.log(res);
            r.html(res);
            //r.innerhtml = res
        },
        error: function(error){
            console.log("El error es: "+ error);
        }

    });



}