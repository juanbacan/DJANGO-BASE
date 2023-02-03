async function fetchRequest(url, params, csrf_token) {
    
    const resp = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify(params),
        credentials: 'same-origin',
    });

    if (resp.status !== 200) {
        return {
            result: false,
            message: 'Error al realizar la petición'
        }
    }
    const data = await resp.json();
    return data;
}

// Main *****************************************
function ready(callback){
    // in case the document is already rendered
    if (document.readyState!='loading') callback();
    // modern browsers
    else if (document.addEventListener) document.addEventListener('DOMContentLoaded', callback);
    // IE <= 8
    else document.attachEvent('onreadystatechange', function(){
        if (document.readyState=='complete') callback();
    });
}

function bloqueoInterfaz() {
    // console.log("Bloqueando Interfaz");
    document.getElementById( 'loading-static' ).style.display = 'flex';
}
function desbloqueoInterfaz() {
    // console.log("Desbloqueando Interfaz");
    document.getElementById( 'loading-static' ).style.display = 'none';
}

function showErrorMessage(mensaje="Ha ocurrido un error inesperado en el servidor", titulo="Error") {
    document.getElementById('error-title').innerHTML = titulo;
    document.getElementById('error-message').innerHTML = mensaje;
    document.getElementById( 'error-static' ).style.display = 'flex';
}

function hideErrorMessage() {
    document.getElementById( 'error-static' ).style.display = 'none';
}

// const modalEdicion = document.getElementById('modalEdicion');
const modals = document.getElementsByClassName('formmodal');
for (let i = 0; i < modals.length; i++) {
    modals[i].addEventListener('click', async function(e) {
        try {
            e.preventDefault()
            const nhref = modals[i].getAttribute('nhref');
            if (!nhref) return;

            bloqueoInterfaz();
            const resp = await fetch(nhref);
            
            desbloqueoInterfaz();

            if (resp.ok){
                const data = await resp.text();
                // from data get the all the content of the tag "script"
                const scripts = data.match(/<script[^>]*>([\s\S]*?)<\/script>/gi);
                // Remove all the scripts from the data
                const dataClean = data.replace(scripts, '');
                const modalEdicion = document.getElementById('modalEdicion');
                modalEdicion.innerHTML = dataClean;
                const myModal = new bootstrap.Modal(modalEdicion);
                myModal.show()
                // Put the scripts in the body of the page
                scripts.forEach(script => {
                    // If script contain src
                    if (script.includes('src')) {
                        // Get the src
                        const src = script.match(/src="([^"]*)"/)[1];
                        // Create a new script tag
                        const newScript = document.createElement('script');
                        // Set the src of the new script tag
                        newScript.src = src;
                        // Append the new script tag to the body
                        document.body.appendChild(newScript);
                    } else {
                        const scriptClean = script.replace(/<script[^>]*>|<\/script>/gi, '');
                        // Create a new script tag
                        const newScript = document.createElement('script');
                        // Set the innerHTML of the new script tag
                        newScript.innerHTML = scriptClean;
                        // Append the new script tag to the body
                        document.body.appendChild(newScript);
                    }
                } );
            } else{
                // console.log('Error al cargar el formulario');
                desbloqueoInterfaz();
            }
        } catch{
            // console.log('Error al cargar el formulario')
            desbloqueoInterfaz();
        }
    })
}

// Función para enviar un formulario dinámico en modal
const submitModalForm1 = async () => {
    const form = document.getElementById('modalForm1');
    //if (!form.reportValidity()) return;
    form.classList.add('was-validated')
    
    if (!form.checkValidity()) return;

    bloqueoInterfaz();
    const resp = await fetch(form.getAttribute('action'), {
        method: 'POST',
        body: new FormData(form)
    })

    // Error en el servidor 
    if (resp.status !== 200) {
        // TODO handle error 500
        desbloqueoInterfaz();
        showErrorMessage();
        return;
    }

    const data = await resp.json();
    
    if (data.result == "ok") {
        if (data.redirected) {
            window.location.replace(data.url);
        } else {
            const myModal = bootstrap.Modal.getInstance(document.getElementById('modalEdicion'));
            myModal.hide();
            desbloqueoInterfaz();
            return;
        }

    } else if (data.result == "bad") {
        desbloqueoInterfaz();
        showErrorMessage(data.mensaje);
    }
}