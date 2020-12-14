// para marcar la versión del proyect
$(".version").text(Django.version);
$(".site_name").text(Django.site_name);
$(".date").text(Django.fecha);
$(".username").text(Django.username);

titlePage = (title) =>{
    // Cambia el titulo de la página
    $(".titlePage").text(title);
}


dtLanguage = (palabraClave) => {
    return {
        "decimal": "",
        "emptyTable": "No hay información",
        "info": "Mostrando _START_ a _END_ de _TOTAL_ " + palabraClave,
        "infoEmpty": "Mostrando 0 to 0 of 0 " + palabraClave,
        "infoFiltered": "(Filtrado de _MAX_ total ) " + palabraClave,
        "infoPostFix": "",
        "thousands": ",",
        "lengthMenu": "Mostrar _MENU_ " + palabraClave,
        "loadingRecords": "Cargando...",
        "processing": "Procesando...",
        "search": "Buscar:",
        "zeroRecords": "Sin resultados encontrados",
        "paginate": {
            "first": "Primero",
            "last": "Ultimo",
            "next": "Siguiente",
            "previous": "Anterior"
        }
    }
}

// PLANTILLAS DE JAVASCRIPT

inputJs = (inputId,label,type,disabled="",value=null) =>{
    return(`<div class="form-group">
                <label for="${inputId}">${label}</label>
                <input 
                  ${disabled}
                  value="${value?value:''}"
                  type="${type}" class="form-control" id="${inputId}" name="${inputId}" placeholder="${label}">
            </div>`)
}

fileInputJs = (inputId,label) =>{
    return(`<form enctype="multipart/form-data"><div class="form-group">
                <label for="${inputId}">${label}</label>
                <div class="input-group">
                <div class="custom-file">
                    <input type="file" class="custom-file-input" id="${inputId}" name="${inputId}">
                    <label class="custom-file-label" for="${inputId}"><span class="textFile">Selecciona un archivo</span></label>
                </div>
                </div>
            </div></form>`)
}

select2InputJs = (label,inputId) => {
    return(`<div class="form-group">
                <label>${label}</label>
                <select class="form-control select2bs4" id="${inputId}" name="${inputId}" style="width: 100%;">
                    <option>${label}</option>
                </select>
            </div>`)
}

select2Ajax = (inputId,url,value=null) =>{

    $(`#${inputId}`).select2({
        theme:'bootstrap4',
        
        ajax: {
            url: url,
            data: function (params) {
              var query = {
                q: params.term,
                type: 'public'
              }
        
              // Query parameters will be ?search=[term]&type=public
              return query;
            }
          }
    })
    if(value){
      console.log(value)
      var newOption = new Option(value.text, value.id, true, true);
      $(`#${inputId}`).append(newOption).trigger('change');
    }

}

dateRange = () =>{
  return(`
  <div class="input-group" id="advance-daterange">
    <input type="text" name="advance-daterange" class="form-control" value="" placeholder="Seleccione un rango de fecha" />
    <span class="input-group-append">
        <span class="input-group-text"><i class="fa fa-calendar"></i></span>
    </span>
  </div><br>
 `)
}

modalBody = (obj) =>{

    return(`<div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-${obj.btnColor}">
                        <h4 class="modal-title">${obj.title}</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        ${obj.content}
                    </div>
                    <div class="modal-footer justify-content-between">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Cerrar</button>
                        <button type="button" class="btn btn-${obj.btnColor}" onclick="${obj.funcion}(${obj.argumento})">${obj.btnLabel}</button>
                    </div>
                </div>
            </div>`)


}





// ==========================================================================

//* localStorage *//
var HDD = {
    get: function(key) {
        return localStorage.getItem(key);
    },
    get_default: function(key, value_default) {
    	try{
    		return localStorage.getItem(key);
    	}
    	catch(err){
    		return value_default;
    	}
    },
    set: function(key, val) {
        return localStorage.setItem(key, val);
    },
    unset: function(key) {
        return localStorage.removeItem(key);
    },
    setJ:function(key,val)
    {
        return localStorage.setItem(key, JSON.stringify(val));
    },
    getJ:function(key)
    {
        return JSON.parse(localStorage.getItem(key));
    }
};

var HSD = {
    get: function(key) {
        return sessionStorage.getItem(key);
    },
    get_default: function(key, value_default) {
      try{
        return sessionStorage.getItem(key);
      }
      catch(err){
        return value_default;
      }
    },
    set: function(key, val) {
        return sessionStorage.setItem(key, val);
    },
    unset: function(key) {
        return sessionStorage.removeItem(key);
    },
    setJ:function(key,val)
    {
        return sessionStorage.setItem(key, JSON.stringify(val));
    },
    getJ:function(key)
    {
        return JSON.parse(sessionStorage.getItem(key));
    }
};



function DjangoURL(url, id='', version='v1') {
  return Django[url].replace(':val:',id).replace('v1',version);
}


//* session *//
function sessionExit(redirect=true) {

    HDD.unset('username');
    HDD.unset(Django.name_jwt);
    
/*    for (var i = 0; i < localStorage.length; i++) {
        HDD.unset(localStorage.key(i)); 
    }

    for(var x = 0; x <= localStorage.length; x++) {
        localStorage.removeItem(localStorage.key(x))
    }*/

    Cookies.remove(Django.name_jwt)

	if (redirect)
	{
		setTimeout(function(){ location.href = '/'; }, 40);
	}
};

function invalidToken() {
    HDD.set('last_url', window.location.pathname);
    sessionExit(true);
};


function handleErrorAxios(error) {
    // console.info(error);
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        // console.log(error.response.data);

        if (error.response.status == 400)
        {
          if (error.response.data.error){
            _error(""+ error.response.data.error).then(function(){});
          }else{
            _error("Por favor verifique los datos ingresados.");
          }
        }
        else if (error.response.status == 401)
        {
          handleUnauthorizedAxios();
        }
        else if (error.response.status == 404)
        {
          console.log("error 404 ", error.request.responseURL)
        }
        else if(error.response.status == 500){
            _error('Hubo un error en el sistema. Contacte al administrador.')
            .then(function() {});
        }        
        else{
          console.info("Response:");
          console.log(error.response);
          // console.log(error.response.headers);
        }

    } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.info("Request");
        console.log(error.request);
        console.log(error)
    } else {
        // Something happened in setting up the request that triggered an Error
        console.log('Error message: ', error.message);
        console.log('Error stack: ', error.stack);
    }
    //console.log(error.config);
}

function handleUnauthorizedAxios() {
  _error_redirect("Se vencio su session, porfavor ingrese nuevamente",
  '/','Sesion expirada');
}

function handleTooManyRequestsAxios()
{
  console.log("Too many requests ");
}

function verifyJwtToken() {
  axios.post('/api/v1/auth/verify_jwt_token/', {token: HDD.get(Django.name_jwt)})
  .then(function(response){
    if (response.status != 200)
    {
      sessionExit(true);
    }
  })
  .catch(function(error) {
      sessionExit(true);
  });    
}

function refreshJwtToken() {
    var conf = {
        headers: { Authorization: 'jwt '+ HDD.get(Django.name_jwt)}
    };

    axios.post('/api/v1/auth/refresh_token/', {token: HDD.get(Django.name_jwt)}, conf)
    .then(function(response){
      if (response.status == 200)
      {
        HDD.set(Django.name_jwt,response.data.token);
        Cookies.set(Django.name_jwt, response.data.token);
      }
    })
    .catch(function(error) {
        sessionExit(true);
    });

}

function userInSession(redirect=true) {

    if (HDD.get(Django.name_jwt) == null)
    {
      sessionExit(redirect);
      return;
    }
    unmark_li();
    if (HDD.get('username') == null)
    {
      var conf = {
          headers: { Authorization: 'jwt '+ HDD.get(Django.name_jwt)}
      };
  
      axios.get(Django.api_user, conf)
      .then(function(response){
        if (response.status == 200)
        {
          HDD.set('username', response.data.username);
          $(".text_username").text(HDD.get('username'));
        }
      })
      .catch(function(error) {
          handleErrorAxios(error);
      });

    }
    else
    {
      $(".text_username").text(HDD.get('username'));
    }
    refreshJwtToken();
}


//* alerts sweetalert *//
function _info(textMessage) {
    swal({
        title: "",
        text: textMessage,
        icon: "info",
        buttons: false,
    });
};

function _error(textMessage) {
    noti = swal({
        title: "Error",
        text: textMessage,
        icon: "error",
        buttons: false,
    });
    return noti
};

function _error_redirect(textMessage,redirect,title='Error') {
    swal({  
        title: title,
        text: textMessage,
        icon: "error",
        showCancelButton: false,
        confirmButtonColor: "#23c6c8",
        confirmButtonText: "Cerrar",
        closeOnConfirm: false
    })
    .then(function() {
        location.href = redirect;
    });
};

function _exito(textMessage) {
	swal({
	title: "Información",
		text: textMessage,
		icon: "success",
    buttons: false
	});
};

function _exito_redirect(textMessage,dire) {
	swal({
	title: "Información",
		text: textMessage,
		icon: "success",
    buttons: false
	}).then(function() {
		location.href = dire;
	});
};

function _confirma(textMessage, yes, not) {

  swal({
      title: "Información",
      text: textMessage,
      icon: "warning",
      buttons: [
        'No',
        'Si'
      ],
      dangerMode: true,
    }).then(function(isConfirm) {
      if (isConfirm) {
        yes()
      } else {
        not()
      }
    })

}


function getUrlLastParameter(excludeParams=true) {
  var parts = location.href.split('/');
  var lastSegment = parts.pop() || parts.pop();

  if (excludeParams)
  {
    if (lastSegment.startsWith('?')){
      return parts.pop();
    }
    else
    {
      return lastSegment;
    }

  }
  else
  {
    return lastSegment;  
  }
}

function getParameterUrl(name, url) {
  if (!url) url = location.href;
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( url );
  return results == null ? null : results[1];
};


function updateDatatable(selector=null) {
  var target = selector ? selector : '.table';
  if ( $.fn.dataTable.isDataTable(target) ) {
    var table = $(target).DataTable();
    table.ajax.reload();
    //temp_table.ajax.url( temp_table.ajax.url() ).load();
  }
}



function appendScript(url){
   let script = document.createElement("script");
   script.src = url;
   script.async = false; //IMPORTANT
   document.getElementById("insert_script_here").appendChild(script);
}


function unmark_li(){
  $('ul li').each(function(i)
    {
      $(this).removeClass('active');
    });
}

//* events *//
$("#btn_log_out").on('click',function(){
    sessionExit(true);
})

