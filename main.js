

function man(e){
    let version = e.parentElement.parentElement.parentElement.className.split(" ")[1]
    if(version == "two"){
        version ="one"
    }else{
        version = "two"
    }

    let type = e.className.split[" "][1];
    console.log(type)
    document.querySelector(".one .T").remove()
}