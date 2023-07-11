const pdf = require('html-pdf')
const fs = require('fs')
const ubicacionPlantilla = require.resolve('./template.html')

const creatorTests = async (path) => {

    let sucesos = await fs.promises.readFile(path, 'utf-8')
    sucesos = JSON.parse(sucesos).sucesos

    let contenidoHTML = fs.readFileSync(ubicacionPlantilla, 'utf-8')
    
    // console.log(contenidoHTML)

    sucesos=sucesos.map(e=>e[0])

    // console.log(sucesos)

    sucesos.map((e) => {
        let tipoDeTest = e.tipoDeTest
        let indice = e.indice
        let mensajesEsperados = e.mensajeEsperado
        let action = e.action
        // let typeTarget = action.target.detail
        let target = action.target.location
        let typeTarget = action.target.detail

        contenidoHTML = contenidoHTML.replace("{{tipoDeTest}}", tipoDeTest)
        contenidoHTML = contenidoHTML.replace('{{indice}}', indice)
        contenidoHTML = contenidoHTML.replace('{{mensajesEsperados}}', mensajesEsperados)
        contenidoHTML = contenidoHTML.replace('{{target}}', target)
        contenidoHTML = contenidoHTML.replace('{{typeTarget}}', typeTarget)
        contenidoHTML = contenidoHTML.replace('{{value}}', action.value)
                    //  .replace("{{indice}}", indice)
                    //  .replace('{{mensajesEsperados}}', mensajesEsperados)
                    //  .replace("{{tipoDeAccion}}", action.command)
                    //  .replace("{{target}}", target)
                    //  .replace("{{typeTarget}}". typeTarget)
                    //  .replace('{{value}}',action.value)

        console.log(contenidoHTML.includes('{{tipoDeTest}}'))

        pdf.create(contenidoHTML).toFile('salida.pdf', (e) => {
            if (e) {
                console.log("Error encontrado")
            } else {
                console.log('PDF Creado correctamente')
            }
        })
    })


}

creatorTests('./data.json')